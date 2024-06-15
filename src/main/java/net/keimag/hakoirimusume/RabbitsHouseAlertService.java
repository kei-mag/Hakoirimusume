package net.keimag.hakoirimusume;

import com.linecorp.bot.messaging.client.MessagingApiClient;
import com.linecorp.bot.messaging.model.PushMessageRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.UUID;

@Service
public class RabbitsHouseAlertService {
    private static final Logger log = LoggerFactory.getLogger(RabbitsHouseAlertService.class);
    private final HakoirimusumeProperties.AlertProperties alertProperties;
    private final RabbitsHouseReportSupplier rabbitsHouseReportSupplier;
    private final SensorService sensorService;
    private Calendar disableAlertPeriod = null;
    private final MessagingApiClient messagingApiClient;
    private int alertCount = 0;

    @Autowired
    public RabbitsHouseAlertService(HakoirimusumeProperties hakoirimusumeProperties, SensorService sensorService, RabbitsHouseReportSupplier rabbitsHouseReportSupplier, MessagingApiClient messagingApiClient) {
        this.alertProperties = hakoirimusumeProperties.getAlert();
        this.rabbitsHouseReportSupplier = rabbitsHouseReportSupplier;
        this.sensorService = sensorService;
        this.messagingApiClient = messagingApiClient;
    }

    @Scheduled(fixedDelayString = "${hakoirimusume.alert.polling-interval-sec}000", initialDelay = 300000)
    public void alert() {
        var data = sensorService.getSensorData();
        if (data.temperature() == 0.0 && data.humidity() == 0.0 && data.pressure() == 0.0) {
            log.warn("Sensor data is not available.");
        } else {
            var condition = alertProperties.getCondition();
            double triggerTemp = 1000;
            double triggerHum = 1000;
            if (condition.getTemperature() != null) {
                triggerTemp = condition.getTemperature();
            }
            if (condition.getHumidity() != null) {
                triggerHum = condition.getHumidity();
            }
            if (data.temperature() >= triggerTemp && data.humidity() >= triggerHum) {
                // Alert condition is satisfied.
                var triggerLimit = alertProperties.getTriggerLimit();
                if ((disableAlertPeriod == null || Calendar.getInstance().after(disableAlertPeriod)) && (triggerLimit.getDailyLimit() < 0 || alertCount < triggerLimit.getDailyLimit())){
                    // Send alert message.
                    try {
                        var message = rabbitsHouseReportSupplier.alert();
                        alertProperties.getTo().forEach(to -> {
                            messagingApiClient.pushMessage(UUID.randomUUID(), new PushMessageRequest(
                                    to,
                                    List.of(message),
                                    false,
                                    null
                            ));

                        });
                    } catch (IOException | InterruptedException e) {
                        log.warn("Failed to send alert message: {}", e.getMessage());
                    }
                    if (triggerLimit.getInterval() > 0) {
                        disableAlertPeriod = Calendar.getInstance();
                        disableAlertPeriod.add(Calendar.HOUR, triggerLimit.getInterval());
                    }
                    alertCount++;
                }
            }
        }
    }


}
