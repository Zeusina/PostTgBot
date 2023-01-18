from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from handlers import client
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=getenv("TOKEN"))

# Инициализация диспетчера
dp = Dispatcher(bot)


def on_startup():
    # Регистрация хэндлеров
    logging.info("Бот запущен!")


dp.register_message_handler(client.start, commands="start")


# эхо-бот
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup())
