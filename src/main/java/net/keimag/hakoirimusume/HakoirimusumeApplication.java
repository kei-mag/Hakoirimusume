package net.keimag.hakoirimusume;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.ExecutionException;

import com.linecorp.bot.client.base.Result;
import com.linecorp.bot.messaging.model.*;
import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.linecorp.bot.messaging.client.MessagingApiClient;
import com.linecorp.bot.spring.boot.handler.annotation.EventMapping;
import com.linecorp.bot.spring.boot.handler.annotation.LineMessageHandler;
import com.linecorp.bot.webhook.model.MessageEvent;
import com.linecorp.bot.webhook.model.TextMessageContent;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
@LineMessageHandler
public class HakoirimusumeApplication {
	private static final Logger log = org.slf4j.LoggerFactory.getLogger(HakoirimusumeApplication.class);
	private final MessagingApiClient messagingApiClient;
	private final RabbitsHouseReportSupplier rabbitsHouseReportSupplier;
	private final UserService userService;
	private final Authorizer authorizer;
	private final HakoirimusumeProperties hakoirimusumeProperties;
	private final String menuJson = Files.readString(Paths.get("src/main/resources/templates/menu.json"));

	public static void main(String[] args) {
		SpringApplication.run(HakoirimusumeApplication.class, args);
	}

	@Autowired
	public HakoirimusumeApplication(MessagingApiClient messagingApiClient, RabbitsHouseReportSupplier rabbitsHouseReportSupplier, UserService userService, Authorizer authorizer, HakoirimusumeProperties hakoirimusumeProperties) throws IOException {
		this.messagingApiClient = messagingApiClient;
		this.rabbitsHouseReportSupplier = rabbitsHouseReportSupplier;
		this.userService = userService;
        this.authorizer = authorizer;
        this.hakoirimusumeProperties = hakoirimusumeProperties;
        applyRichMenu();
    }

	@EventMapping
	public void handleTextMessageEvent(MessageEvent event) throws IOException, InterruptedException {
		log.info("event: {}", event);
		final String originalMessageText = ((TextMessageContent) event.message()).text();
		switch (originalMessageText) {
			case "ユーザー認証":
				if (userService.getRole(event.source().userId()) != null && userService.getRole(event.source().userId()) >= UserService.USER) {
					this.reply(event.replyToken(), List.of(new TextMessage("もう既にユーザーとして登録されてるよ！何か困ったことがあったら管理者に訊いてみてね🙇")), false);;
				} else {
					userService.addUser(event.source().userId());
					userService.setState(event.source().userId(), UserState.WAIT_FOR_AIKOTOBA.ordinal());
					this.reply(event.replyToken(), List.of(new TextMessage("ユーザー認証を始めるよ！\n合言葉を入力してね\uD83D\uDC47\n(一字一句正確に！)")), false);
				}
				break;
			case "新しいユーザーを招待":
				log.info("Detected.");
				String aikotoba = authorizer.generateNewAikotoba(event.source().userId());
				log.info("Aikotoba: {}", aikotoba);
				this.reply(event.replyToken(), List.of(
						new TextMessage("新しい人を招待しよう！\n下の合言葉を招待したい人に伝えてね\uD83D\uDC47"),
						new TextMessage(aikotoba)
				), false);
				log.info("Replied.");
				break;
			case "げんき？":
				doForUser(event.source().userId(), () -> {
					messagingApiClient.showLoadingAnimation(new ShowLoadingAnimationRequest(event.source().userId(), 30));
					this.reply(event.replyToken(), List.of(rabbitsHouseReportSupplier.get()), false);
				});
				break;
			case "メニューをひらいて":
				doForUser(event.source().userId(), () -> {
					this.reply(event.replyToken(), List.of(new FlexMessageBuilder().build("MENU", this.menuJson)), false);
				});
				break;
			default:
				if (userService.getRole(event.source().userId()) != null && userService.getState(event.source().userId()) == UserState.WAIT_FOR_AIKOTOBA.ordinal()) {
					var success = authorizer.authorize(originalMessageText);
					if (success && userService.getRole(event.source().userId()) != UserService.BANNED_USER) {
						userService.setRole(event.source().userId(), UserService.USER);
						this.reply(event.replyToken(), List.of(new TextMessage("ユーザー認証完了！\nこれからよろしくね✌")), false);
					} else {
						this.reply(event.replyToken(), List.of(new TextMessage("認証失敗！\nもう一度新しい合言葉を発行してもらってね\uD83D\uDE23")), false);
					}
					userService.setState(event.source().userId(), UserState.NONE.ordinal());
					applyRichMenu();
				}
				break;
		}
	}


//	@EventMapping
//	public void handleDefaultMessageEvent(Event event) {
//		System.out.println("event: " + event);
//	}

	private void reply(String replyToken,
					   List<Message> messages,
					   boolean notificationDisabled) {
		try {
			Objects.requireNonNull(replyToken, "replyToken");
			Objects.requireNonNull(messages, "messages");
			Result<ReplyMessageResponse> apiResponse = messagingApiClient
					.replyMessage(new ReplyMessageRequest(replyToken, messages, notificationDisabled))
					.get();
			log.info("Sent messages: {}", messages);
			log.info("Response: {}", apiResponse);
		} catch (InterruptedException | ExecutionException e) {
			throw new RuntimeException(e);
		}
	}

	private void doForUser(String userId, Runnable action) {
		if (userService.isSatisfiedRole(userId, UserService.USER)) {
			action.run();
		} else {
			this.reply(userId, List.of(new TextMessage("箱入り娘の機能を使うには最初にユーザー認証が必要です。\n使っている人に合言葉を教えてもらってから\n「ユーザー認証」\nと言ってみてね！🙏")), false);
		}
	}

	private void applyRichMenu() {
		HakoirimusumeProperties.RichmenuProperties richmenuProperties = hakoirimusumeProperties.getRichmenu();
		if (!userService.getUsers().isEmpty()) {
			messagingApiClient.linkRichMenuIdToUsers(new RichMenuBulkLinkRequest(richmenuProperties.getForAuthorizedUser(), userService.getUsers()));
		}
    }
}

enum UserState {
	NONE,
	WAIT_FOR_AIKOTOBA,
	WAIT_FOR_CONFIRMATION
}