from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButtonRequestChat, ChatAdministratorRights

from utils import LoggingUtils
from utils import SampleUtils, ConfigUtils

log = LoggingUtils("handlers.add_post").log
config = ConfigUtils().config_parse()
sample = SampleUtils().get_sample()


class AddPost(StatesGroup):
    """
    Class with a states for the post state machine
    """
    def __init__(self) -> None:
        """
        Initialize states
        :return: None
        """
        log.info("FSM states initialized!")

    waiting_for_number = State()
    waiting_for_name = State()
    waiting_for_words_count = State()
    waiting_for_file = State()
    waiting_for_channel = State()
    checking = State()
    waiting_for_send = State()


async def start_add(msg: types.Message, state: FSMContext) -> None:
    """
    Send request to add exposition number
    :param msg: Message
    :param state: FSMContext
    :return: None
    """
    await msg.answer("Пожалуйста отправьте номер изложения")
    await state.set_state(AddPost.waiting_for_number)


async def add_name(msg: types.Message, state: FSMContext) -> None:
    """
    Receive exposition number and send request to add exposition name
    :param msg: Message
    :param state: FSMContext
    :return: None
    """
    if msg.text.isdigit():
        await state.update_data(number=msg.text)
        await msg.answer("Пожалуйста отправьте название изложения")
        await state.set_state(AddPost.waiting_for_name)
    else:
        await msg.answer("Пожалуйста отправьте число")


async def add_words_count(msg: types.Message, state: FSMContext) -> None:
    """
    Receive exposition name and send request to add exposition words count
    :param msg: Message
    :param state: FSMContext
    :return: None
    """
    await state.update_data(name=msg.text)
    await msg.answer("Пожалуйста отправьте количество слов в исходном тексте")
    await state.set_state(AddPost.waiting_for_words_count)


async def add_file(msg: types.Message, state: FSMContext) -> None:
    """
    Receive exposition words count and send request to add exposition file
    :param msg: Message
    :param state: FSMContext
    :return: None
    """
    if msg.text.isdigit():
        await state.update_data(words=msg.text)
        await types.ChatActions.upload_audio()
        await msg.answer("Пожалуйста отправьте изложение", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddPost.waiting_for_file)
    else:
        await msg.answer("Пожалуйста отправьте число")


async def add_channel(msg: types.Message, state: FSMContext) -> None:
    """
    Receive exposition file and send request to add channel for sending post
    :param msg: Message
    :param state: FSMContext
    :return: None
    """
    await state.update_data(audio=msg.audio.file_id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    kb.add(types.KeyboardButton(text="Выбрать канал", callback_data="channel",
                                request_chat=KeyboardButtonRequestChat(
                                    chat_is_channel=True,
                                    bot_is_member=True,
                                    bot_administrator_rights=ChatAdministratorRights(can_post_messages=True),
                                    user_administrator_rights=ChatAdministratorRights(can_post_messages=True),
                                    request_id=0
                                )))
    await msg.answer("Выберите канал, на который будет отправлен пост", reply_markup=kb)
    await state.set_state(AddPost.checking)


async def check(msg: types.Message, state: FSMContext) -> None:
    """
    Receive exposition channel for post and send check message
    :param msg: Message
    :param state: FSMContext
    :return: None
    """
    chat = msg.chat_shared.to_python().get("chat_id")
    data = await state.get_data()
    message = ""
    message += (sample.get('name').replace('%name%', data.get('name')) + "\n")
    message += (sample.get('number').replace('%number%', data.get('number')) + "\n")
    message += (sample.get('words').replace('%words%', data.get('words')) + "\n")
    await msg.answer("Проверьте получившийся пост:", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer_audio(data.get("audio"), caption=message, parse_mode='HTML')
    await msg.answer("Если все верно, то отправьте /send, иначе /cancel")
    await state.update_data(channel=chat)
    await state.update_data(ms=message)
    await state.set_state(AddPost.waiting_for_send)


async def send(msg: types.Message, state: FSMContext) -> None:
    """
    Receive agree/disagree and send post or cancel
    :param msg: types.Message
    :param state: FsMContext
    :return: None
    """
    data = await state.get_data()
    await msg.bot.send_audio(data.get("channel"), data.get("audio"), caption=data.get("ms"),
                             parse_mode='HTML')
    await msg.answer("Пост успешно отправлен!")
    await state.finish()


async def cancel(msg: types.Message, state: FSMContext) -> None:
    """
    Canceling the state and cleaning the cache
    :param msg: Message
    :param state: FSMContext
    :return: None
    """
    await state.finish()
    await msg.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())
