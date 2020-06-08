from src.utils.data_fetch_utils import getNewMessages, deleteOldMessages
import asyncio
from flask import Flask, make_response
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

async def main_start(days, hours): # reomve
    await getNewMessages(days, hours)

async def main_clean(days, hours):
    await deleteOldMessages(days, hours)

loop = asyncio.get_event_loop()

def start(days, hours):
    loop.run_until_complete(main_start(days, hours))
    return "OK"

def clean(days, hours):
    loop.run_until_complete(main_clean(days, hours))
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
