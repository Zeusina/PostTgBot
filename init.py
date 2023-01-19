from aiogram import Bot, Dispatcher
from os import getenv
from utils import LoggingUtils

# Инициализация логов
log = LoggingUtils("Init").log

# Инициализация бота
bot = Bot(token=getenv("TOKEN"))
log.info("Bot initialized!")
# Инициализация диспетчера
dp = Dispatcher(bot)
log.info("Dispatcher initialized!")