import discord
from dotenv import load_dotenv
import os
from agents import Agent, Runner, ModelSettings
import asyncio
import nest_asyncio
import csv
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nest_asyncio.apply()    

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("環境変数 'BOT_TOKEN' が設定されていません。")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# グローバルに講義データを保持しておく
GLOBAL_LECTURE_DATA = []

# CSVを読み込む関数
async def load_lecture_data(file_path: str):
    data = []
    if not os.path.exists(file_path):
        logger.error(f"講義データ({file_path})が見つかりません。")
        return data
        
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

async def main():
    # スクリプトのディレクトリを基準にCSVパスを設定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "shinshu_summary.csv")
    
    # 起動時に一度だけCSVを読み込む
    global GLOBAL_LECTURE_DATA
    GLOBAL_LECTURE_DATA = await load_lecture_data(csv_path)
    logger.info(f"{len(GLOBAL_LECTURE_DATA)}件の講義データを読み込みました。")

    # シンプルなRAG構築のため、MCPサーバーは介さずに構成
    client.agent = Agent(
        name="Assistant",
        model="gpt-4o-mini",
        model_settings=ModelSettings(temperature=0),
        instructions="あなたは親しみのあるdiscord botです。信大の講師みたいに、学生に寄り添って簡潔に応答してください。",
    )

    @client.event
    async def on_ready():
        logger.info(f"ボット {client.user} としてログインしました。")

    @client.event
    async def on_message(message):
        # 自分が送信したメッセージには反応しない
        if message.author == client.user:
            return
        # 自分にメンションされた時しか反応しない
        if client.user not in message.mentions:
            return

        # タイピングインジケーターを表示しつつAPI処理
        async with message.channel.typing():
            try:
                # メッセージ内容を抽出（メンション部分を取り除く）
                content = message.content.replace(f'<@{client.user.id}>', '').strip()
                
                # 講義データとユーザー入力からプロンプトを構築
                prompt = (
                    f"以下は信州大学の講義データセットの一部です。\n"
                    f"{GLOBAL_LECTURE_DATA[:100]}...\n\n" # 全件渡すとトークン超過の恐れがあるため適宜調整。必要に応じて全文でも可。
                    f"ユーザーの質問に基づいて、上記の講義情報から最適な答えを導き出して回答してください。\n"
                    f"質問: {content}"
                )

                # AI応答を生成
                result = await Runner.run(client.agent, prompt)
                response_text = result.final_output
                
                logger.info(f"回答生成完了: {message.author.name} の質問へ応答")
                await message.reply(response_text)

            except Exception as e:
                logger.error(f"エラーが発生しました: {e}")
                await message.reply("すみません、内部エラーが発生しました。時間をおいて再度お試しください。")

    client.run(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
