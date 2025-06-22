from io import BytesIO
from uuid import uuid4
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile, Message
from aiogram.filters import Command


from modules.helpers import getenv
from modules.bot.telegram.chat import Chat

import logging

TELEGRAM_BOT_API_KEY = getenv("TELEGRAM_BOT_API_KEY")
OWNER_USER_ID = getenv("OWNER_ID")

dp = Dispatcher()
bot = Bot(token=TELEGRAM_BOT_API_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
log = logging.getLogger(__name__)
chat = Chat()

async def run_telegram_bot():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        log.error("run_telegram_bot_error", e)
        
async def send_file(buffer: BytesIO, filename: str | None):
    try:
        buffer.seek(0)
        input_file = BufferedInputFile(
            buffer.read(), filename=filename if filename is not None else str(uuid4())
        )
        await bot.send_document(chat_id=OWNER_USER_ID, document=input_file)
    except Exception as e:
        log.error("send_file_error", e)
        
async def send_message(text: str):
    try:
        await bot.send_message(chat_id=OWNER_USER_ID, text=text)
    except Exception as e:
        log.error("send_message_error", e)
        raise e
    
@dp.message(Command("health"))
async def health_check(message: Message):
    try:
        await message.reply("Bot is running smoothly!")
    except Exception as e:
        log.error("health_check_error", e)
        await message.answer("An error occurred while checking health.")
        
        
@dp.message()
async def handle_message(message: Message):
    try:
        log.info(f"Received message: {message.text}")
        await chat.emit_message(message.text)
    except Exception as e:
        log.error("handle_message_error", e)
        await message.answer("An error occurred while processing your message.")