# 箱入り娘 —— ペットを見守るLINE BOT
**LINEのトークからいつでもペットの様子と部屋の気温がわかります**  
- Raspberry Piに接続したカメラの映像と室温・湿度・気圧センサーからの情報を[LINE Messaging API](https://developers.line.biz/ja/services/messaging-api/)を通していつでも問い合わせることが出来ます。  
- 家族以外がBOTを友達追加しても機能にアクセスできないように、合言葉による認証機能を備えています。
- <s>Docker Containerを利用して簡単に環境を構築することも可能です。</s>

## 使い方
箱入り娘を使い始めるには、以下の2つの方法があります。
1. [最新のリリース](https://github.com/kei-mag/Hakoirimusume/releases/latest)からダウンロードしてインストールする方法
2. リポジトリをクローンしてビルドする方法

### 1. 最新のリリースからダウンロードしてインストールする方法
1. [最新のリリース](https://github.com/kei-mag/Hakoirimusume/releases/latest)から`hakoirimusume-vX.X.X.zip`をダウンロードします。
2. ダウンロードしたZIPファイルをインストールしたいディレクトリに展開します。
3. 箱入り娘LINEボットサーバーと、センサーサーバーの設定を確認し、必要に応じて設定を変更します。
   （詳細は[箱入り娘の設定について](docs/configuration.md)を参照）
4. 展開したフォルダ内の`setup.sh`を実行して、インストールと初回の設定を行います。
5. インストールが完了したら、`sudo systemctl start hakoirimusume.service hakoirimusume-sensor.service`を実行するか、
   サーバーを再起動して箱入り娘のサービスを起動します。

### 2. リポジトリをクローンしてビルドする方法
1. リポジトリをクローンします。
   ```bash
   git clone https://github.com/kei-mag/Hakoirimusume.git
   ```
2. Spring Bootアプリケーションをビルドします。
    ```bash
    cd Hakoirimusume
    ./gradlew build
    ```
3. [sampleディレクトリ](./sample)内のServiceファイルを参考に、箱入り娘LINEボットサーバーとセンサーサーバーの起動構成を記述します。
4. サービスファイルを`/etc/systemd/system/`に配置し、`sudo systemctl enable hakoirimusume.service hakoirimusume-sensor.service`を実行してサービスを有効化します。
5. `sudo systemctl start hakoirimusume.service hakoirimusume-sensor.service`を実行するか、サーバーを再起動して箱入り娘のサービスを起動します。

## 動作テスト環境
- Raspberry Pi 4 Model B Rev 1.4 (8GB RAM)  [↪](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/),  Raspberry Pi Zero WH  [↪](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)
- Raspberry Pi Camera Module 2  [↪](https://www.raspberrypi.com/products/camera-module-v2/)
- Raspberry Pi OS
  - Release date: March 15th 2024
  - System: 32-bit, 64-bit
  - Kernel version: 6.6
  - Debian version: 12 (bookworm)
  - Default Python: `Python 3.11.2 (main, Mar 13 2023, 12:18:29) [GCC 12.2.0] on linux`
- JAVA 17.0.1
  ```bash
  $ java --version
  openjdk 17.0.11 2024-04-16
  OpenJDK Runtime Environment (build 17.0.11+9-Raspbian-1deb12u1rpt1)
  OpenJDK Client VM (build 17.0.11+9-Raspbian-1deb12u1rpt1, mixed mode, emulated-client)
  ```

## ディレクトリ構成
```
Hakoirimusume
├─docs                            # ドキュメント
├─gradle                          # Gradle関連ファイル
│  └─wrapper
├─sample                          # サンプルファイル
├─sensor_server                   # 箱入り娘センサーサーバー
│  └─templates                    # センサーサーバーのHTMLテンプレート
├─src                             # 箱入り娘LINEボットサーバー
│  ├─main
│  │  ├─java
│  │  │  └─net
│  │  │      └─keimag
│  │  │          └─hakoirimusume  # メインファイル
│  │  └─resources
│  │      ├─static
│  │      └─templates
│  └─test
│      └─java
│          └─net
│              └─keimag
│                  └─hakoirimusume  # テストファイル
└─tools                             # ツールスクリプト
```

## ライセンス
このプロジェクトは、[MITライセンス](./LICENSE)の下で公開されています。