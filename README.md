Discord 自販機Bot (チケット制)
このBotは、Discordサーバー内で商品一覧を表示し、ユーザーが「購入手続きへ」ボタンを押すことで、管理者とユーザー専用のプライベートなチケットチャンネルを自動的に作成します。

PayPayなどの手動決済と商品の手動受け渡しを想定しており、複雑な決済連携なしに、シンプルかつ安全な取引をサポートします。

機能一覧
	•	商品パネル表示: `/panel` コマンドで、商品一覧と「購入手続きへ」ボタンを表示します。
	•	チケットチャンネル作成: 「購入手続きへ」ボタンを押すと、ユーザーと管理者のみがアクセスできる専用のテキストチャンネルが作成されます。
	•	管理者通知: 新しいチケットチャンネルが作成された際、指定された管理用チャンネルに通知が送信されます。
	•	チケットチャンネル削除: チケットチャンネル内で「取引完了（チャンネル削除）」ボタンを押すことで、チャンネルを安全に削除できます。

導入手順
1. Discord Botの準備
	1.	Discord Developer Portal にアクセスし、新しいアプリケーションを作成します。
	2.	作成したアプリケーションの「Bot」タブに移動し、「Add Bot」をクリックしてBotを作成します。
	3.	「Privileged Gateway Intents」セクションで、`MESSAGE CONTENT INTENT` と `PRESENCE INTENT`、`SERVER MEMBERS INTENT` を有効にします。
	4.	「Bot」タブで表示される「TOKEN」をコピーします。これは後で必要になります。
	5.	「OAuth2」タブの「URL Generator」で、`bot` スコープと `applications.commands` スコープを選択し、必要な権限（例: `Manage Channels`, `Send Messages`, `Read Message History` など）を選択して、生成されたURLでBotをサーバーに招待します。

2. 環境変数の設定
Botを安全に実行するため、以下の情報を環境変数として設定する必要があります。これらの情報は、GitHubには直接コミットせず、デプロイ先のサービス（Renderなど）で設定してください。

	•	`DISCORD_BOT_TOKEN`: Discord Developer Portalで取得したBotのトークン。
	•	`DISCORD_GUILD_ID`: Botを導入するDiscordサーバーのID。
	◦	Discordの設定で「開発者モード」を有効にし、サーバー名を右クリックして「IDをコピー」で取得できます。
	•	`DISCORD_ADMIN_CHANNEL_ID`: 新しいチケットが作成された際に通知を受け取る管理用チャンネルのID。
	◦	チャンネル名を右クリックして「IDをコピー」で取得できます。
	•	`DISCORD_TICKET_CATEGORY_ID`: チケットチャンネルを作成するカテゴリのID。
	◦	カテゴリ名を右クリックして「IDをコピー」で取得できます。

3. コードのデプロイ (Renderを利用する場合)
	1.	このリポジトリのコードをGitHubにアップロードします。
	◦	`main.py`、`requirements.txt`、`README.md` をリポジトリのルートに配置します。
	2.	Render にアクセスし、アカウントを作成またはログインします。
	3.	ダッシュボードで「New」→「Web Service」を選択します。
	4.	GitHubリポジトリを接続し、このBotのリポジトリを選択します。
	5.	以下の設定を行います。
	◦	Name: 任意のサービス名 (例: `vending-machine-bot`)
	◦	Region: 任意のリージョン (例: `Oregon (US West)`)
	◦	Branch: `main` (またはコードがあるブランチ)
	◦	Root Directory: 空白 (リポジトリのルート)
	◦	Runtime: `Python 3`
	◦	Build Command: `pip install -r requirements.txt`
	◦	Start Command: `python main.py`
	◦	Instance Type: `Free` (無料プラン)
	6.	「Advanced」セクションを展開し、「Add Environment Variable」をクリックして、上記「2. 環境変数の設定」でリストアップした環境変数を追加します。
	7.	「Create Web Service」をクリックしてデプロイを開始します。

デプロイが完了すると、Botが24時間稼働を開始します。

使い方
	1.	Botが導入されたDiscordサーバーで、管理者権限を持つユーザーがテキストチャンネルで `/panel` と入力し、Enterキーを押します。
	2.	商品パネルが表示され、「購入手続きへ」ボタンが設置されます。
	3.	ユーザーが「購入手続きへ」ボタンを押すと、新しいチケットチャンネルが作成され、管理者とユーザーに通知が届きます。
	4.	チケットチャンネル内で、ユーザーは希望商品とPayPayの送金リンクを送信します。
	5.	管理者はPayPayでの支払いを確認し、商品をユーザーに手動で提供します。
	6.	取引が完了したら、チケットチャンネル内の「取引完了（チャンネル削除）」ボタンを押してチャンネルを閉じます。

商品リストのカスタマイズ
`main.py` ファイル内の `PRODUCTS` 辞書を編集することで、商品名、価格、説明を自由に変更できます。


￼
変更を適用するには、GitHubのリポジトリを更新し、Renderで再デプロイ（または自動デプロイ）を行う必要があります。

ライセンス
MIT License

Copyright (c) [現在の年] [あなたの名前または組織名]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
