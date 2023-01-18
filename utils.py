import json
import logging
import configparser as configparser
from aiogram import types


class Telegram_utils():
    def __init__(self):
        logging.info("Telegram utils initialized!")

    async def get_user_locale(self, message: types.Message):
        return message.from_user.locale


class Parse_utils():
    def __init__(self):
        logging.info("Parse utils initialized!")

    async def get_locale(self, locale):
        with open(f"local/{locale}.json", "r", encoding="utf-8") as f:
            return json.load(f)[f"{locale}"]


class ConfigUtils:
    def config_parse(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config


class LoggingUtils:
    def __init__(self, name: str = "Bot"):
        Config_Utils = ConfigUtils()
        config = Config_Utils.config_parse()
        self.log = logging.getLogger(name)
        self.log.setLevel(config["LOG"]["level"])

    def log(self):
        return self.log

