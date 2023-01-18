import logging
from aiogram import types
from utils import Telegram_utils, Parse_utils

Tg_utils = Telegram_utils()
Parse_utils = Parse_utils()


async def start(message: types.Message):
    locale = await Tg_utils.get_user_locale(message)
    locale = await Parse_utils.get_locale(locale)
    await message.answer(locale["messages"]["start"].replace("%username%", message.from_user.username))
    logging.info(f"Bot started by {message.from_user.username} with locale {message.from_user.locale}")
