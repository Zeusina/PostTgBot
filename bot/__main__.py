from aiogram import Dispatcher, Bot
import os

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.handlers import bot_commands
import handlers
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def main() -> None:
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    bot = Bot(token=os.getenv("TOKEN"))
    handlers.register_user_commands(dp)
    await bot.set_my_commands(commands=commands_for_bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.info("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
