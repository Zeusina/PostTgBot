from aiogram import Dispatcher, Bot
import os
from commands import register_user_commands
import asyncio
import logging


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=os.getenv("TOKEN"))

    register_user_commands(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
