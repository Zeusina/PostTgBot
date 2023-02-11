from aiogram import Dispatcher, Bot
import os
from handlers import register_user_commands
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=os.getenv("TOKEN"))

    register_user_commands(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.info("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
