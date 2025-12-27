import discord
from dotenv import load_dotenv
import os
from agents import Agent, Runner, ModelSettings, WebSearchTool
from agents.mcp import MCPServerStdio
import asyncio
import nest_asyncio
import csv
nest_asyncio.apply()    

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Drive上のCSVを読む関数（標準csvモジュール版）
async def load_lecture_data(file_path: str):
    # CSVをリストの辞書として読み込む
    data = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

async def main():
    async with MCPServerStdio(
        name="信大チャット",
        params={
            "command": "node",
            "args": [
                "C:\\Users\\socce\\mcp_server\\gdrive-mcp-server\\dist\\index.js"
            ],
            "env": {
            "GOOGLE_APPLICATION_CREDENTIALS": "C:\\Users\\socce\\mcp_server\\gdrive-mcp-server\\credentials\\gcp-oauth.keys.json",
            "MCP_GDRIVE_CREDENTIALS": "C:\\Users\\socce\\mcp_server\\gdrive-mcp-server\\credentials\\.gdrive-server-credentials.json"
            }
        },
    ) as server:
        client.agent = Agent(
            name="Assistant",
            model="gpt-5-mini",
            # model_settings=ModelSettings(temperature=0),
            instructions="あなたは親しみのあるdiscord botです。信大の講師みたいに簡潔に応答してください。",
            mcp_servers=[server],
            # tools=[
            #     WebSearchTool(),
            # ],
        )

        @client.event
        async def on_ready():
            print("botが起動しました")

        @client.event
        async def on_message(message):
            # 自分が送信したメッセージに対しては反応しない
            if message.author == client.user:
                return
            # 自分にメンションされた時しか反応しない
            if client.user not in message.mentions:
                return

            # CSVを読み込む（Drive内のファイルをローカルコピー済みと仮定）
            lecture_data = await load_lecture_data("C:\\Users\\socce\\mcp_server\\src\\shinshu_summary.csv")

            # メッセージに応じてAIに講義提案を生成
            prompt = (
                f"以下は信州大学の講義データです。\n"
                f"{lecture_data}\n\n"
                f"ユーザーの質問に基づいて、講義データから最適な答えを出して。\n"
                f"質問: {message.content}"
            )

            # AI応答を生成
            result = await Runner.run(client.agent, prompt)
            print(result.final_output)

            # メッセージが送信されたチャンネルに、AI応答を送信
            await message.channel.send(result.final_output)

        client.run(bot_token)

asyncio.run(main())
