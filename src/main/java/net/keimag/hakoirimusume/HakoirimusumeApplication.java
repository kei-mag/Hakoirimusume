package net.keimag.hakoirimusume;

import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.ExecutionException;

import com.linecorp.bot.client.base.Result;
import com.linecorp.bot.messaging.model.*;
import org.slf4j.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.linecorp.bot.messaging.client.MessagingApiClient;
import com.linecorp.bot.spring.boot.handler.annotation.EventMapping;
import com.linecorp.bot.spring.boot.handler.annotation.LineMessageHandler;
import com.linecorp.bot.webhook.model.Event;
import com.linecorp.bot.webhook.model.MessageEvent;
import com.linecorp.bot.webhook.model.TextMessageContent;

@SpringBootApplication
@LineMessageHandler
public class HakoirimusumeApplication {
	private static final Logger log = org.slf4j.LoggerFactory.getLogger(HakoirimusumeApplication.class);
	private final MessagingApiClient messagingApiClient;
	private final RabbitsHouseReportSupplier rabbitsHouseReportSupplier;

	public static void main(String[] args) {
		SpringApplication.run(HakoirimusumeApplication.class, args);
	}

	public HakoirimusumeApplication(MessagingApiClient messagingApiClient) throws IOException{
		this.messagingApiClient = messagingApiClient;
		this.rabbitsHouseReportSupplier = new RabbitsHouseReportSupplier("src/main/resources/templates/report_template.json");
	}

	@EventMapping
	public void handleTextMessageEvent(MessageEvent event) throws IOException, InterruptedException {
		System.out.println("event: " + event);
		final String originalMessageText = ((TextMessageContent) event.message()).text();
		messagingApiClient.showLoadingAnimation(new ShowLoadingAnimationRequest(event.source().userId(), 30));
		switch (originalMessageText) {
			case "アラート":
				this.reply(event.replyToken(), List.of(rabbitsHouseReportSupplier.alert()), false);
				break;
			case "げんき？":
				this.reply(event.replyToken(), List.of(rabbitsHouseReportSupplier.get()), false);
				break;
			default:
				this.reply(event.replyToken(), List.of(new TextMessage(originalMessageText)), false);
				break;
		}
	}


	@EventMapping
	public void handleDefaultMessageEvent(Event event) {
		System.out.println("event: " + event);
	}

	private void reply(String replyToken,
					   List<Message> messages,
					   boolean notificationDisabled) {
		try {
			Objects.requireNonNull(replyToken, "replyToken");
			Objects.requireNonNull(messages, "messages");
			Result<ReplyMessageResponse> apiResponse = messagingApiClient
					.replyMessage(new ReplyMessageRequest(replyToken, messages, notificationDisabled))
					.get();
			log.info("Sent messages: {}", apiResponse);
		} catch (InterruptedException | ExecutionException e) {
			throw new RuntimeException(e);
		}
	}
}