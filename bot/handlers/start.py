from aiogram import types
import logging

logger = logging.getLogger('commands/start.py')


async def start_command(message: types.Message) -> None:
    await message.answer(
        "Привет, %username%!\nВы запустили бота для создания постов в каналах.".replace("%username%",
                                                                                        message.from_user.username))
    logger.info("User %username% started bot".replace("%username%", message.from_user.username))
