from aiogram.fsm.state import StatesGroup, State
import logging

logger = logging.getLogger('structures/fsm_groups.py')


class AddPostStates(StatesGroup):
    """
    Class with states for add_post_command
    """
    def __init__(self):
        logger.info("PostStates created")

    waiting_for_number = State()
    waiting_for_name = State()
    waiting_for_words_count = State()
    waiting_for_file = State()
    waiting_for_channel = State()
    checking = State()
    waiting_for_send = State()
