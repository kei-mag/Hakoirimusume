package net.keimag.hakoirimusume;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.Map;
import java.util.Objects;

@Component
public class ApplicationIntegration {

    private final RestTemplate restTemplate;
    private final String projectRootDir;

    public ApplicationIntegration(RestTemplate restTemplate, Environment environment) {
        this.restTemplate = restTemplate;
        this.projectRootDir = new File(Objects.requireNonNull(environment.getProperty("user.dir"))).getAbsolutePath();
    }

    public Result get(String url) {
        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, null, String.class);
        return new Result(response.getStatusCode().value(), response.getBody());
    }

    public Result post(String url, Map<String, Object> header, Map<String, Object> body) {
        HttpHeaders headers = new HttpHeaders();
        if (header != null) {
            header.forEach((key, value) -> headers.add(key, value.toString()));
        }
        headers.add("Content-Type", "application/json");

        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        ResponseEntity<String> response = restTemplate.postForEntity(url, requestEntity, String.class);
        return new Result(response.getStatusCode().value(), response.getBody());
    }

    public Result exec(String command) {
        if (command == null || command.isBlank()) {
            throw new IllegalArgumentException("Command must not be null or blank");
        }

        StringBuilder output = new StringBuilder();
        int exitCode;
        try {
            Process process = Runtime.getRuntime().exec(command, null, new File(projectRootDir));
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append("\n");
                }
            }
            exitCode = process.waitFor();
        } catch (Exception e) {
            throw new RuntimeException("Failed to execute command: " + command, e);
        }
        return new Result(exitCode, output.toString().trim());
    }

    public record Result(int statusCode, String contents) {

    }
}

@Configuration
class RestTemplateConfig {
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}