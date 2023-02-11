from aiogram import Router
from aiogram.filters.command import CommandStart

from bot.commands.start import start_command
import logging

logger = logging.getLogger('commands/__init__.py')


def register_user_commands(router: Router) -> None:
    router.message.register(start_command, CommandStart())
    logger.info("User commands registered")
