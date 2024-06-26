# 箱入り娘センサーサーバー
箱入り娘センサーサーバーは、HTTPリクエストに応じてRaspberry Pi Camera Moduleで小屋の様子を撮影し、BME280センサーで温度・湿度・気圧を取得して返すサーバーです。

このプログラムが機能を提供するにはCamera ModuleとBME280センサーが必要となるため、Raspberry Pi上で動作することが想定されています。

## センサーサーバーの仕様
### エンドポイント
- `/` : 小屋の温度・湿度・気圧を表示するダッシュボードページ
- `/get` : APIリクエストのエンドポイント（箱入り娘LINEボットサーバーはこのエンドポイントにリクエストを送信して情報を取得します）

### ダッシュボード
センサーサーバーは、現在の小屋の気温・湿度・気圧の表示や、シャットダウンボタンを表示するダッシュボードページを提供します。
- ダッシュボードで使われているHTMLテンプレートは、`sensor_server/templates/dashboard.html`にあります。
- `dashboard.html`内では以下のプレースホルダーを実際の値に置き換えて表示します。
  - `{{INTERVAL}}` : ダッシュボードの更新間隔（秒），600秒に設定してあります。 
  - `{{DATETIME}}` : 取得した日時
  - `{{TEMP}}` : 現在の気温
  - `{{HUMID}}` : 現在の湿度
  - `{{PRESS}}` : 現在の気圧
- シャットダウンボタンを押すと、`/shutdown`にPOSTリクエストを送信してRaspberry Piをシャットダウンします。
- シャットダウンボタンが押された際の画面構成は、`sensor_server/templates/shuttingdown.html`にあります。
- ダッシュボードの画面構成は[Kindle Paper white 第6世代](https://www.amazon.co.jp/KindlePaperwhite-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D%E3%83%AA%E3%83%BC%E3%83%80%E3%83%BC/dp/B00CTUMMD2/ref=cm_cr_arp_d_product_top?ie=UTF8)の[SkipStone Browser](http://www.fabiszewski.net/kindle-browser/)で表示したときに最適になるようになっています。
  ![Kindleを使った温度計ダッシュボード](images/thermometer_dashboard_kindle.jpg)

### APIリクエスト
HTTP GETで`/get`にリクエストを送信すると、小屋の気温・湿度・気圧を取得してJSON形式で返します。

#### リクエストパラメーター
単に`/get`にリクエストを送信した場合には気温・温度・気圧の値を返します。  
`/get?withcamera`にリクエストを送信することで、カメラで撮影した画像のURLも返します。

#### レスポンス
JSON形式で返されるレスポンスは以下のような形式です。
```json
{
  "datetime": "2024-06-22T23:31:37+09:00",
  "temp": 25.717657079087802,
  "humid": 64.14656215454197,
  "press": 1001.6473936276144,
  "image": "http://imgur.com/xxxxxx.png",
  "deletehash": "xxxxxx"
}
```
| フィールド        | 説明               | 補足                                          |
|--------------|------------------|---------------------------------------------|
| `datetime`   | 取得した日時           | ISO 8601のオフセット形式のタイムスタンプ                    |
| `temp`       | 気温               | 単位：℃                                        |
| `humid`      | 湿度               | 単位：%                                        |
| `press`      | 気圧               | 単位：hPa                                      |
| `image`      | 小屋の画像のImgur URL  | `withcamera`パラメーターがない場合はnullまたはキー自体が含まれません。 |
| `deletehash` | Imgur画像の削除用ハッシュ値 | `withcamera`パラメーターがない場合はnullまたはキー自体が含まれません。 |
