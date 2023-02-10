from aiogram import types


async def start_command(message: types.Message) -> None:
    await message.answer(
        "Привет, %username%!\nВы запустили бота для создания постов в каналах.".replace("%username%",
                                                                                        message.from_user.username))
