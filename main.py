import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from fastfood import router

load_dotenv()
TOKEN = os.getenv("bottoken")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("✅ Bot ishga tushdi...")
    asyncio.run(main())

