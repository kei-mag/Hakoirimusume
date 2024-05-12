# 箱入り娘仕様

## 機能
- Rabbit's House Reportによるカメラ・センサ情報提供（ユーザーリクエスト）
- Rabbit's House Alertによるカメラ・センサ情報通知（自動）
- 既存ユーザーの招待コードによる新規ユーザー登録
- ユーザーによるログアウト
- ユーザー遠隔ログアウト
- ユーザー遠隔バン
- サーバーのプライベートIPアドレス表示
- Messaging API当月送信可能メッセージ残数表示
- サーバー遠隔シャットダウン

## データベース設計
### Usersテーブル
| user_id                           | role              | state | request_time       |
| --------------------------------- | ----------------- | ----- | ------------------ |
| U8189cf6745fc0d808977bdb0b9f22995 | 1              | 1     | 2020-01-01 0:00:00 |
| U8189cf6745fc0d808977bdb0b9f22996 | 2             | 2     | 2020-01-01 0:00:00 |
| U8189cf6745fc0d808977bdb0b9f22997 | 0 | 0     | 2020-01-01 0:00:00 |
- user_id : (STRING, PRIMARY_KEY) LINE APIから提供されるユーザーID [参考](https://developers.line.biz/ja/docs/messaging-api/getting-user-ids/#what-is-user-id)
- role : (INTEGER, NOT NULL) -1 <= role <= 2
  - -1 : BANNED_USER
  - 0 : UNAUTHORIZED_USER
  - 1 : USER
  - 2 : ADMIN
- state : (INTEGER, NOT NULL) メッセージによるリクエストの状態管理
  - デフォルトは`0`
  - サーバー起動時に全ユーザーのstateが`0`にリセットされる
- request_time : (STRING) 前回リクエスト時間
  - デフォルトは`NULL`
  - サーバー起動時に全ユーザーのrequest_timeが`NULL`にリセットされる

#### SQLiteのテーブル初期化
```sql
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    role INTEGER DEFAULT 0 NOT NULL,
    state INTEGER DEFAULT 0 NOT NULL,
    request_time TEXT DEFAULT NULL,
    CHECK (role >= -1 AND role <= 2),
);
```

#### SQLiteのサーバー起動時の初期化処理
```sql
UPDATE users SET state = 0, request_time = NULL;
```

#### SQLiteのユーザー追加処理
```sql
INSERT INTO users (id) VALUES (?);
```

#### SQLiteのユーザー削除処理
```sql
DELETE FROM users WHERE id = ?;
```

## 合言葉によるユーザー認証
