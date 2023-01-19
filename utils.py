import logging
import configparser
from aiogram import Dispatcher
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from pathlib import Path



class ConfigUtils:
    def config_parse(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config


class LoggingUtils:
    def __init__(self, name: str = "Bot"):
        config = ConfigUtils().config_parse()
        logging.basicConfig(level=config["LOG"]["level"])
        ll = logging.getLogger(name)
        ll.setLevel(config["LOG"]["level"])
        self.log = ll

    def log(self):
        return self.log


log = LoggingUtils("Utils").log


class TelegramUtils:
    def __init__(self):
        log.info("Telegram utils initialized!")
