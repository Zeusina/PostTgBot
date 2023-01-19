from aiogram import types

from Bot import dp
from utils import LoggingUtils, TranslationUtils

log = LoggingUtils("Client_handlers").log
_ = TranslationUtils(dp).return_gettext()


async def start(message: types.Message):
    await message.answer(_("Привет, %username%!\nВы запустили бота для создания постов в каналах.").replace("%username%", message.from_user.username))
    log.info(f"User {message.from_user.username} with locale {message.from_user.locale} started bot!")