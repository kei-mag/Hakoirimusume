package net.keimag.hakoirimusume;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import jakarta.validation.constraints.Pattern;

import java.util.ArrayList;
import java.util.List;

@Data
@Component
@ConfigurationProperties("hakoirimusume")
public class HakoirimusumeProperties {
    private SensorComponentProperties sensorComponent = new SensorComponentProperties();
    private AlertProperties alert = new AlertProperties();
    private AikotobaProperties aikotoba = new AikotobaProperties();
    private InfoProperties info = new InfoProperties();
    private String databasePath = "./hakoirimusume.db";

    @Data
    @Configuration
    public static class SensorComponentProperties {
        private String host = "localhost";
        @Min(1)
        private String port = "80";
    }
    
    @Data
    @Configuration
    public static class AlertProperties {
        private TriggerLimitProperties triggerLimit = new TriggerLimitProperties();
        private ConditionProperties condition = new ConditionProperties();
        private ActionProperties action = new ActionProperties();

        @Data
        @Configuration
        public static class TriggerLimitProperties {
            @Min(0)
            private int interval = 3;
            private int dailyLimit = -1;
        }
        
        @Data
        @Configuration
        public static class ConditionProperties {
            private double temperature = -1;
            private double humidity = -1;
        }

        @Data
        @Configuration
        public static class ActionProperties {
            @Pattern(regexp = "GET|POST|COMMAND", message ="type can be \"GET\", \"POST\", \"COMMAND\" or null.")
            private String type = null;
            private String target = null;
            private String header = null;
            private String body = null;
            private String successMessage = null;
            private String failureMessage = null;
        }
    }
    
    @Data
    @Configuration
    public static class AikotobaProperties {
        @NotNull
        private List<List<String>> seeds = new ArrayList<>();
        @Min(0)
        private int timeoutSec = 60;
    }

    @Data
    @Configuration
    public static class InfoProperties {
        private boolean showPrivateIp = true;
    }
}
