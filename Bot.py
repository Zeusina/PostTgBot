from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from handlers import client
from utils import ConfigUtils, LoggingUtils, TranslationUtils


# Инициализация конфига
Config_Utils = ConfigUtils()
config = Config_Utils.config_parse()

# Настройка логов
logger = LoggingUtils().log

# Инициализация бота
bot = Bot(token=getenv("TOKEN"))

# Инициализация диспетчера
dp = Dispatcher(bot)


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
