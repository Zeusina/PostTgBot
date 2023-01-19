from aiogram import executor, types
from handlers import client
from utils import ConfigUtils, LoggingUtils
from init import dp

# Инициализация конфига
Config_Utils = ConfigUtils()
config = Config_Utils.config_parse()

# Настройка логов
logger = LoggingUtils().log


def on_startup():
    # Регистрация хэндлеров
    logger.info("Bot started!")


dp.register_message_handler(client.start, commands="start")


# эхо-бот
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup())
