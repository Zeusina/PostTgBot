from aiogram import executor, types
from handlers import client, add_post
from utils import ConfigUtils, LoggingUtils
from init import dp

# Инициализация конфига
Config_Utils = ConfigUtils()
config = Config_Utils.config_parse()

# Настройка логов
logger = LoggingUtils().log


def on_startup():
    logger.info("Bot started!")


def register_client_handlers():
    dp.register_message_handler(client.start, commands=["start"])


def register_add_post_handlers():
    dp.register_message_handler(add_post.start_add, commands=["add"], state="*")
    dp.register_message_handler(add_post.cancel, commands=["cancel"], state="*")
    dp.register_message_handler(add_post.add_name, state=add_post.AddPost.waiting_for_number)
    dp.register_message_handler(add_post.add_words_count, state=add_post.AddPost.waiting_for_name)
    dp.register_message_handler(add_post.add_file, state=add_post.AddPost.waiting_for_words_count)
    dp.register_message_handler(add_post.add_channel, state=add_post.AddPost.waiting_for_file,
                                content_types=types.ContentTypes.AUDIO)
    dp.register_message_handler(add_post.check, state=add_post.AddPost.checking, content_types=types.ContentTypes.CHAT_SHARED)
    dp.register_message_handler(add_post.send, state=add_post.AddPost.waiting_for_send, commands=["send"])

    logger.info("Add post handlers registered!")


def register_handlers():
    register_client_handlers()
    register_add_post_handlers()


register_handlers()

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup())
