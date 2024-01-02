# org invite bot

github の organization に招待する discord bot です。

## 使い方

pipenv を用いています。

```bash
pipenv install
pipenv run python main.py
```

## 環境変数

-   OWNER_NAME: 招待を許可できるユーザー
-   INVITE_CHANNEL_NAME: 招待を許可するチャンネル
-   ORG_NAME: 招待する GitHub の Organization の名前
-   DISCORD_TOKEN: Discord の Bot のトークン
-   GITHUB_TOKEN: GitHub のトーク(need:`admin:org`)
