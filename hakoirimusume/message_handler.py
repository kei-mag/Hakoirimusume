from mailbox import Message
from operator import is_

from fastapi import FastAPI, HTTPException, Request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    ShowLoadingAnimationRequest,
    TextMessage,
    QuickReply,
    FlexMessage
)
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import GroupSource, MessageEvent, RoomSource, Source, TextMessageContent, UserSource

from .report_creater import ReportCreater

from .db import auth_manager, db


class TalkMessageHandler:
    def __init__(self, line_bot_api: AsyncMessagingApi) -> None:
        self.line_bot_api = line_bot_api
        self.report_creater = ReportCreater()

    async def handle_message(self, message: TextMessageContent, source: Source, reply_token: str):
        user_id = source.user_id
        if source.type == "group":
            group_id = source.group_id
        else:
            group_id = None
        if message.text == "げんき？":
            if auth_manager.can_access(user_id, 1):
                await self.line_bot_api.show_loading_animation(
                    ShowLoadingAnimationRequest(chatId=user_id, loadingSeconds=30), async_req=False
                )
                await self.line_bot_api.reply_message(
                    ReplyMessageRequest(replyToken=reply_token, messages=[self.report_creater.get_report()])
                )
                ...  # TODO: Implement Rabbit's House Report
            else:
                pass  # Ignore message from unauthorized user
        elif message.text == "新しいユーザーを招待":
            # TODO: Implement user invitation
            aikotoba = auth_manager.create_new_aikotoba(source.user_id)
            text = "新しい人を招待しよう！下の合言葉を招待したい人に伝えてね👇"
            await self.line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token, messages=[TextMessage(text=text), TextMessage(text=aikotoba)]
                )
            )
        elif message.text == "ユーザー認証":
            auth_manager.authorize_request(user_id)
            await self.line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[TextMessage(text="ユーザー認証を始めるよ！\n合言葉を入力してね👇\n(一字一句正確に！)", quickReply=QuickReply())],
                )
            )
        else:
            if auth_manager.is_wait_for_aikotoba(user_id):
                if auth_manager.authorize(user_id, message.text):
                    await self.line_bot_api.reply_message(
                        ReplyMessageRequest(
                            replyToken=reply_token,
                            messages=[TextMessage(text="ユーザー認証完了！\nこれからよろしくね✌")],
                        )
                    )
                else:
                    await self.line_bot_api.reply_message(
                        ReplyMessageRequest(
                            replyToken=reply_token,
                            messages=[TextMessage(text="認証失敗！\nもう一度新しい合言葉を発行してもらってね😣")],
                        )
                    )
                db.set_state(user_id, 0)
            else:
                pass  # Do nothing for normal message
        db.print_table()
        return
