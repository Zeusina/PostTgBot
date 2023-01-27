from aiogram import Bot, Dispatcher
from os import getenv
from utils import LoggingUtils
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Инициализация логов
log = LoggingUtils("init").log

# Инициализация бота
bot = Bot(token=getenv("TOKEN"))
log.info("Bot initialized!")
# Инициализация диспетчера
dp = Dispatcher(bot, storage=MemoryStorage())
log.info("Dispatcher initialized!")
