# import os
# import sys
# from datetime import datetime

# import yaml
# from flask import Flask, abort, request
# from linebot.v3 import WebhookHandler
# from linebot.v3.exceptions import InvalidSignatureError
# from linebot.v3.messaging import ApiClient, Configuration, MessagingApi, ReplyMessageRequest, TextMessage
# from linebot.v3.webhooks import MessageEvent, TextMessageContent


# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY="dev",  ## os.urandom(24)
#         DATABASE=os.path.join(app.instance_path, "hakoirimusume.sqlite"),
#     )

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_file(filename="hakoirimusume.yml", load=yaml.safe_load)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     from . import db

#     db.init_app(app)

#     try:
#         configuration = Configuration(access_token=app.config["CHANNEL_ACCESS_TOKEN"])
#         handler = WebhookHandler(channel_secret=app.config["CHANNEL_SECRET"])
#     except KeyError:
#         print(
#             """
#               Tokens for LINE Messaging API were not found in Flask config file.\n
#               Please add \n
#                 `CHANNEL_ACCESS_TOKEN = <YOUR CHANNEL ACCESS TOKEN>`
#                 `CHANNEL_SECRET = <YOUR CHANNEL SECRET>`
#               to Flask config file.
#               """,
#             file=sys.stderr,
#         )
#         exit()
#     launch_time = datetime.now()

#     @app.route("/check")
#     def response_status():
#         cur_time = datetime.now()
#         contents = f"""
#             Status: OK\n
#             Launch Time: {launch_time} ({cur_time - launch_time} before)
#         """
#         return contents

#     @app.route("/endpoint", methods=["POST"])
#     def callback():
#         # get X-Line-Signature header value
#         signature = request.headers["X-Line-Signature"]

#         # get request body as text
#         body = request.get_data(as_text=True)
#         app.logger.info("Request body: " + body)

#         # handle webhook body
#         try:
#             handler.handle(body, signature)
#         except InvalidSignatureError:
#             app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
#             abort(400)

#         return "OK"

#     @handler.add(MessageEvent, message=TextMessageContent)
#     def handle_message(event):
#         with ApiClient(configuration) as api_client:
#             line_bot_api = MessagingApi(api_client)
#             line_bot_api.reply_message_with_http_info(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[TextMessage(text=event.message.text, quickReply=None)],
#                     notificationDisabled=False,
#                 )
#             )

#     return app
