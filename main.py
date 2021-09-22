import os
from dotenv import load_dotenv

from Bot import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

if __name__ == "__main__":
    client = Bot(CHANNEL_NAME)
    client.run(TOKEN)