# 箱入り娘 —— ペットを見守るLINE BOT
**LINEのトークからいつでもペットの様子と部屋の気温がわかります**  
- Raspberry Piに接続したカメラの映像と室温・湿度・気圧センサーからの情報を[LINE Messaging API](https://developers.line.biz/ja/services/messaging-api/)を通していつでも問い合わせることが出来ます。  
- 家族以外がBOTを友達追加しても機能にアクセスできないように、合言葉による認証機能を備えています。
- Docker Containerを利用して簡単に環境を構築することも可能です。

> [!Note]  
> 現在、プログラムを一から書き直したv2を開発中です。  
> このドキュメントに記載の事項は現在構想中または開発中のものとなります。  
> v1ブランチの制作物は3年前に開発した初期バージョンで一通りの機能が実装済みです。  

## 動作テスト環境
- [Raspberry Pi 4 Model B Rev 1.4 (8GB RAM)](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), [Raspberry Pi Zero WH](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)
- [Raspberry Pi Camera Module 2](https://www.raspberrypi.com/products/camera-module-v2/)
- Raspberry Pi OS Bookworm (32bit, 64bit)

## 使用SDK
- [LINE Messaging API SDK for Java](https://github.com/line/line-bot-sdk-java?tab=readme-ov-file#line-messaging-api-sdk-for-java)
- [Spring Boot](https://spring.io/projects/spring-boot)