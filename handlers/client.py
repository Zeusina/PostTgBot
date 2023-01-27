from aiogram import types
from utils import LoggingUtils

log = LoggingUtils("handlers.client").log



async def start(message: types.Message):
    await message.answer(
        "Привет, %username%!\nВы запустили бота для создания постов в каналах.".replace("%username%",
                                                                                           message.from_user.username))
    log.info(f"User {message.from_user.username} started bot!")
