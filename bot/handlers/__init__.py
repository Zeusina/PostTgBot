import logging

from aiogram import Router
from aiogram.filters.command import CommandStart, Command

from bot.handlers.add_post import (cancel_add_post, add_post_command, add_post_number, add_post_name,
                                   add_post_words_count, add_post_file, add_post_check, add_post_send)
from bot.handlers.start import start_command
from bot.handlers.bot_commands import bot_commands
from bot.structures.fsm_groups import AddPostStates

__all__ = ["start_command", "bot_commands", ]

logger = logging.getLogger('commands/__init__.py')


def register_user_commands(router: Router) -> None:
    router.message.register(start_command, CommandStart())
    router.message.register(cancel_add_post, Command(commands=['cancel']))
    router.message.register(add_post_command, Command(commands=['add']))
    router.message.register(add_post_number, AddPostStates.waiting_for_number)
    router.message.register(add_post_name, AddPostStates.waiting_for_name)
    router.message.register(add_post_words_count, AddPostStates.waiting_for_words_count)
    router.message.register(add_post_file, AddPostStates.waiting_for_file)
    router.message.register(add_post_check, AddPostStates.waiting_for_channel)
    router.message.register(add_post_send, AddPostStates.waiting_for_send, Command(commands=['send']))
    logger.info("User commands registered")
