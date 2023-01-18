from aiogram import Bot, Dispatcher, executor, types
from os import getenv

# Инициализация бота
bot = Bot(token=getenv("TOKEN"))

# Инициализация диспетчера
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Запущен!")

# эхо-бот
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp)