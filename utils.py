import json
import logging
import configparser as configparser
from aiogram import types, Dispatcher
from aiogram.contrib.middlewares.i18n import I18nMiddleware



class LoggingUtils:
    def __init__(self, name: str = "Bot"):
        Config_Utils = ConfigUtils()
        config = Config_Utils.config_parse()
        self.log = logging.getLogger(name)
        self.log.setLevel(config["LOG"]["level"])

    def log(self):
        return self.log


log = LoggingUtils("Utils").log


class TelegramUtils:
    def __init__(self):
        logging.info("Telegram utils initialized!")

    async def get_user_locale(self, message: types.Message):
        return message.from_user.locale


class ParseUtils:
    def __init__(self):
        log.info("Parse utils initialized!")

    async def get_locale(self, locale):
        with open(f"local/{locale}.json", "r", encoding="utf-8") as f:
            return json.load(f)[f"{locale}"]


class ConfigUtils:
    def config_parse(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config


class TranslationUtils:
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        log.info("Translation utils initialized!")
        self.i18n = I18nMiddleware("Bot", "locales", default="ru")
        dp.middleware.setup(self.i18n)

    def return_gettext(self):
        return self.i18n.gettext

