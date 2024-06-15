package net.keimag.hakoirimusume;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.client.ResourceAccessException;

import java.io.IOException;
import java.util.Map;

@Component
public class SensorService {
    private static final Logger log = LoggerFactory.getLogger(SensorService.class);
    private final ApplicationIntegration applicationIntegration;
    private final HakoirimusumeProperties.SensorServerProperties sensorServerProperties;

    @Autowired
    public SensorService(ApplicationIntegration applicationIntegration, HakoirimusumeProperties hakoirimusumeProperties) {
        this.applicationIntegration = applicationIntegration;
        this.sensorServerProperties = hakoirimusumeProperties.getSensorServer();
    }

    public SensorData getSensorData() {
        return getData(sensorServerProperties.getNoCameraEndpoint());
    }

    public SensorData getSensorCameraData() {
        return getData(sensorServerProperties.getEndpoint());
    }

    private SensorData getData(String endpoint) {
        ApplicationIntegration.Result result;
        try {
            result = applicationIntegration.get(endpoint);
        } catch (ResourceAccessException e) {
            log.warn("Failed to get sensor data: {}", e.getMessage());
            return null;
        }
        if (result.statusCode() == 200 && !result.contents().isBlank()) {
            // Convert result.contents() (This is JSON String) to Map.
            try {
                String cameraUri = null;
                String deleteHash = null;
                double temperature = 0.0;
                double humidity = 0.0;
                double pressure = 0.0;
                var sensorData = new ObjectMapper().readValue(result.contents(), Map.class);
                if (sensorData.get("temp") != null && sensorData.get("humid") != null && sensorData.get("press") != null) {
                    temperature = (double) sensorData.get("temp");
                    humidity = (double) sensorData.get("humid");
                    pressure = (double) sensorData.get("press");
                }
                var photoData = sensorData.get("photo");
                if (photoData != null) {
                    cameraUri = (String) ((Map<String, String>) photoData).get("uri");
                    deleteHash = (String) ((Map<String, String>) photoData).get("deletehash");
                }
                return new SensorData(cameraUri, deleteHash, temperature, humidity, pressure);
            } catch (IOException e) {
                log.warn("Failed to parse sensor data: {}", e.getMessage());
                return null;
            }
        } else {
            return null;
        }
    }

    public record SensorData(String cameraUrl, String deleteHash, double temperature, double humidity, double pressure) {
    }
}
