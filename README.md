# 信州大学講義支援 AI Bot (Shinshu Univ. Lecture Support AI)
## 大学の講義データ（シラバス）を学習したAIが、Discord上で学生の質問に答えてくれるチャットボットです。 OpenAIの GPT-4o-mini を活用し、単なるキーワード検索ではなく、文脈を理解した対話が可能です。

**デモ画面 (Demo)**
例：「3年後期からAIについて学ぶロードマップを作って」といった抽象的な質問に対し、シラバスデータに基づいて回答します。
例：「データベースとは？」のような一般的な質問にも対応。
<img width="1041" height="393" alt="image" src="https://github.com/user-attachments/assets/92c69b3f-15a4-4763-b190-7da477aaaf07" />
<img width="1162" height="351" alt="image" src="https://github.com/user-attachments/assets/ad36cd9a-1fbc-42e0-8f2c-7adddf60f177" />

**開発のきっかけ (Background)**
「大学のポータルサイトはスマホで見づらく、知りたい情報に即座にアクセスできない」 私自身が感じていたこの不便さを解消するために開発しました。

当初は単純なルールベースの検索botを想定していましたが、「どの授業を取ればいいか相談したい」「関連する授業を知りたい」というニーズに応えるため、生成AI（LLM）を統合しました。「頼れる先輩にLINEで聞くような感覚」で使える学習支援ツールを目指しています。

**機能一覧 (Features)**
  *AIによる自然言語対応 (Generative AI)

「月曜の1限なに？」といった事実確認から、「ロードマップつくって」「AI系の授業はある？」といった相談まで柔軟に対応。

*大学独自の知識ベース (RAG - Retrieval-Augmented Generation)

一般的なChatGPTとは異なり、大学の講義データ（CSV）をシステムプロンプトとして組み込んでいるため、大学のカリキュラムに即した回答を生成します。

*高コストパフォーマンス

モデルには gpt-4o-mini を採用。高い応答精度を維持しつつ、個人開発でも運用可能なコストに抑えています。

使用技術 (Tech Stack)
Language: Python 3.13
AI / LLM: OpenAI API (GPT-4o-mini)
Framework: discord.py
Package Manager: uv (Astral) - 高速な環境構築のため採用
Data: CSV (将来的にDBへの移行を検討)
Tools: VS Code, Git/GitHub

**工夫した点・苦労した点 (Challenges)**
1. ドメイン知識の注入（簡易RAGの実装）
AIにただ質問を投げるだけでは一般的な回答しか返ってきません。そこで、講義情報を構造化データ（CSV）として読み込み、それを「コンテキスト（前提知識）」としてAIに渡すロジックを実装しました。これにより、「信州大学のAI」 としての振る舞いを実現しています。

2. Python環境構築と依存関係の解決
最新のPython 3.13を使用したため、ライブラリ（pydantic等）間のバージョン競合に直面しました。 解決策として、Rust製の高速パッケージマネージャー uv を導入。仮想環境（.venv）をクリーンに再構築し、依存関係を厳密に管理することで安定稼働させました。

3. セキュリティと構成管理
APIキーなどの機密情報はコードにハードコードせず、.env ファイルで管理し python-dotenv で読み込む設計にしました。Gitへの誤プッシュを防ぐため .gitignore の設定も徹底しています。


