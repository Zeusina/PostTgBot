import configparser
import json
import logging


class ConfigUtils:
    @staticmethod
    def config_parse():
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        return config


class LoggingUtils:
    def __init__(self, name: str = "Bot"):
        config = ConfigUtils().config_parse()
        logging.basicConfig(level=config["LOG"]["level"], format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        ll = logging.getLogger(name)
        ll.setLevel(config["LOG"]["level"])
        self.log = ll

    def log(self):
        return self.log


log = LoggingUtils("utils").log


class TelegramUtils:
    def __init__(self):
        log.info("Telegram utils initialized!")


class SampleUtils:
    def __init__(self):
        log.info("Sample utils initialized!")
        self.config = ConfigUtils().config_parse()

    def get_sample(self):
        with open(self.config['SAMPLE']['name'].strip() + self.config['SAMPLE']['ext'].strip(), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data['post_text']
