package net.keimag.hakoirimusume;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.linecorp.bot.messaging.model.FlexMessage;

public class FlexMessageBuilder {
    public FlexMessage build(String altText, String containerJson) {
        String json = """
                {
                  "type" : "flex",
                  "altText" : "{{AltText}}",
                  "contents" : {{Containers}}
                  }
                }
                """;
        json = json.replace("{{AltText}}", altText);
        json = json.replace("{{Containers}}", containerJson);

        ObjectMapper objectMapper = new ObjectMapper()
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        try {
            return objectMapper.readValue(json, FlexMessage.class);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}