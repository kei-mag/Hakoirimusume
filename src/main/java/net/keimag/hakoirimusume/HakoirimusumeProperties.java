package net.keimag.hakoirimusume;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.hibernate.validator.constraints.URL;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;
import jakarta.validation.constraints.Pattern;

import java.util.ArrayList;
import java.util.List;

@Data
@Component
@ConfigurationProperties("hakoirimusume")
public class HakoirimusumeProperties {
    private RichmenuProperties richmenu = new RichmenuProperties();
    private SensorServerProperties sensorServer = new SensorServerProperties();
    private AlertProperties alert = new AlertProperties();
    private AikotobaProperties aikotoba = new AikotobaProperties();
    private InfoProperties info = new InfoProperties();
    private RemoteShutdownProperties remoteShutdown = new RemoteShutdownProperties();
    private RequestProperties request = new RequestProperties();

    @Data
    @SpringBootConfiguration
    public static class RichmenuProperties {
        private String forAuthorizedUser = null;
    }

    @Data
    @SpringBootConfiguration
    public static class SensorServerProperties {
        @URL(protocol = "http")
        private String endpoint = "localhost";
        @URL(protocol = "http")
        private String cameraEndpoint = "localhost?noCamera=true";
    }

    @Data
    @SpringBootConfiguration
    public static class AlertProperties {
        private List<String> to = new ArrayList<>();
        @Min(10)
        private int pollingIntervalSec = 600;
        private TriggerLimitProperties triggerLimit = new TriggerLimitProperties();
        private ConditionProperties condition = new ConditionProperties();
        private ActionProperties action = new ActionProperties();

        @Data
        @SpringBootConfiguration
        public static class TriggerLimitProperties {
            @Min(0)
            private int interval = 3;
            private int dailyLimit = -1;
        }

        @Data
        @SpringBootConfiguration
        public static class ConditionProperties {
            private Double temperature = null;
            private Double humidity = null;
        }

        @Data
        @SpringBootConfiguration
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
    @SpringBootConfiguration
    public static class AikotobaProperties {
        @NotNull
        private List<List<String>> seeds = new ArrayList<>();
        @Min(0)
        private int timeoutSec = 0;
    }

    @Data
    @SpringBootConfiguration
    public static class InfoProperties {
        private boolean showPrivateIp = true;
    }

    @Data
    @SpringBootConfiguration
    public static class RemoteShutdownProperties {
        private boolean enable = false;
        @Pattern(regexp = "admin|user", message ="Please specify a valid role")
        private String availableRole = "admin";
        private String command = "shutdown -h now";
        private String successMessage = "Shutdown command was sent.";
        private String failureMessage = "Failed to send shutdown command.";
    }

    @Data
    @SpringBootConfiguration
    public static class RequestProperties {
        @Min(0)
        private int timeoutSec = 0;
    }
}
