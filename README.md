# 🎓 信州大学講義支援 AI Bot (Shinshu Univ. Lecture Support AI)

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.6.4-5865F2.svg)](https://discordpy.readthedocs.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-00A67E.svg)](https://platform.openai.com/)
[![uv](https://img.shields.io/badge/uv-Astral-purple.svg)](https://github.com/astral-sh/uv)

大学の講義データ（シラバス）を学習したAIが、Discord上で学生の質問に答えてくれるチャットボットです。
OpenAIの `GPT-4o-mini` を活用し、単なるキーワード検索ではなく、文脈を理解した柔軟な対話が可能です。

---

## 💡 開発のきっかけ (Background)
**「大学のポータルサイトはスマホで見づらく、知りたい情報に即座にアクセスできない」**  
私自身が感じていたこの不便さを解消するために開発しました。

当初は単純なルールベースの検索botを想定していましたが、「どの授業を取ればいいか相談したい」「関連する授業を知りたい」という複雑なニーズに応えるため、生成AI（LLM）を統合。「頼れる先輩にLINEで聞くような感覚」で使える学習支援ツールを目指しました。

---

## 🌟 特徴・機能一覧 (Features)

- **🤖 AIによる自然言語対応**
  「月曜の1限なに？」といった事実確認から、「ロードマップつくって」「AI系の授業はある？」といった相談まで柔軟に対応します。

- **📚 大学独自の知識ベース (簡易RAGの実装)**
  一般的なChatGPTとは異なり、大学の講義データ（CSV）をシステムプロンプトとして組み込んでいるため、信州大学の実際のカリキュラムに即した回答を生成します。

- **💰 高コストパフォーマンス**
  モデルには `gpt-4o-mini` を採用。高い応答精度を維持しつつ、個人開発でも運用可能なコストに抑えています。

---

## 💻 デモ画面 (Demo)

| 抽象的な相談にも対応 | 用語の解説や一般的な質問にも対応 |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/92c69b3f-15a4-4763-b190-7da477aaaf07" width="100%"> | <img src="https://github.com/user-attachments/assets/ad36cd9a-1fbc-42e0-8f2c-7adddf60f177" width="100%"> |

*例：「3年後期からAIについて学ぶロードマップを作って」といった質問に対し、シラバスデータに基づいて回答しています。*

---

## 🚀 実行環境の構築 (Setup & Installation)

Rust製の高速パッケージマネージャー `uv` を使用した環境構築手順です。

### 1. リポジトリのクローン
```bash
git clone https://github.com/shun1415/University-Lecture-Support-Bot-Discord-.git
cd University-Lecture-Support-Bot-Discord-
```

### 2. 環境変数の設定
`.env.example` をコピーして `.env` ファイルを作成し、各種APIキーを設定します。
```bash
cp .env.example .env
```
`.env` ファイルの中身をエディタで開き、取得したトークン等を書き換えてください。
```env
BOT_TOKEN=your_discord_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. パッケージのインストールと実行
```bash
# uv環境で依存関係を同期
uv sync

# Botの起動
uv run python src/discord_agent.py
```

※ 起動に成功すると、コンソールに `ボット [Bot名]#xxxx としてログインしました。` と表示されます。

---

## 🛠 工夫した点・苦労した点 (Challenges & Solutions)

1. **ドメイン知識の注入（簡易RAGの実装）**
   AIにただ質問を投げるだけでは一般的な回答しか返ってきません。そこで、講義情報を構造化データ（CSV）として読み込み、それを「コンテキスト（前提知識）」としてAIに渡すロジックを実装しました。これにより、「信州大学のAI」 としての振る舞いを実現しています。現在、起動時に1度だけCSVをメモリにキャッシュし、レスポンスの高速化を図っています。

2. **Python環境構築と依存関係の解決**
   最新のPython 3.13を使用したため、ライブラリ間のバージョン競合に直面しました。解決策として、Rust製の高速パッケージマネージャー `uv` を導入。仮想環境（`.venv`）をクリーンに再構築し、`pyproject.toml` や `uv.lock` で依存関係を厳密に管理することで安定稼働させました。

3. **セキュリティと構成管理**
   APIキーなどの機密情報はコードにハードコードせず、`.env` ファイルで管理し `python-dotenv` で読み込む設計にしています。Gitへの誤プッシュを防ぐため `.gitignore` の設定も徹底し、セキュアなリポジトリ運用を心がけています。

---

## ⚙️ 使用技術 (Tech Stack)

- **Language:** Python 3.13
- **AI / LLM:** OpenAI API (`gpt-4o-mini`)
- **Framework:** discord.py
- **Package Manager:** uv (Astral)
- **Data Source:** CSV (将来的にDBへの移行を検討中)
- **Tools:** VS Code, Git/GitHub

