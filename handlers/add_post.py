from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButtonRequestChat, ChatAdministratorRights

from utils import LoggingUtils
from utils import SampleUtils, ConfigUtils, SecretsUtils

log = LoggingUtils("handlers.add_post").log
config = ConfigUtils().config_parse()
secrets = SecretsUtils()


class AddPost(StatesGroup):
    def __init__(self):
        log.info("FSM states initialized!")

    waiting_for_number = State()
    waiting_for_name = State()
    waiting_for_words_count = State()
    waiting_for_file = State()
    waiting_for_channel = State()
    checking = State()
    waiting_for_send = State()


async def start_add(msg: types.Message, state: FSMContext):
    await msg.answer("Пожалуйста отправьте номер изложения")
    await state.set_state(AddPost.waiting_for_number)


async def add_name(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(number=msg.text)
        await msg.answer("Пожалуйста отправьте название изложения")
        await state.set_state(AddPost.waiting_for_name)
    else:
        await msg.answer("Пожалуйста отправьте число")


async def add_words_count(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Пожалуйста отправьте количество слов в исходном тексте")
    await state.set_state(AddPost.waiting_for_words_count)


async def add_file(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(words=msg.text)
        await types.ChatActions.upload_audio()
        await msg.answer("Пожалуйста отправьте изложение", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddPost.waiting_for_file)
    else:
        await msg.answer("Пожалуйста отправьте число")


async def add_channel(msg: types.Message, state: FSMContext):
    await state.update_data(audio=msg.audio.file_id)
    kb = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    kb.add(types.InlineKeyboardButton(text="Выбрать канал", callback_data="channel", reply_markup=types.KeyboardButton(
        text="Выбрать канал",
        request_chat=KeyboardButtonRequestChat(
            chat_is_channel=True,
            bot_is_member=True,
            bot_administrator_rights=ChatAdministratorRights(can_post_messages=True),
            user_administrator_rights=ChatAdministratorRights(can_post_messages=True),
            request_id=msg.from_user.id
        ))))
    await msg.answer("Выберите канал, на который будет отправлен пост", reply_markup=kb)
    await state.set_state(AddPost.checking)


async def check(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sample = SampleUtils().get_sample()
    message = ""
    message += (sample.get('name').replace('%name%', data.get('name')) + "\n")
    message += (sample.get('number').replace('%number%', data.get('number')) + "\n")
    message += (sample.get('words').replace('%words%', data.get('words')) + "\n")
    await call.answer()
    await call.message.answer("Проверьте получившийся пост:", reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer_audio(data.get("audio"), caption=message, parse_mode='HTML')
    await call.message.answer("Если все верно, то отправьте /send, иначе /cancel")
    await state.update_data(ms=message)
    await state.set_state(AddPost.waiting_for_send)


async def send(msg: types.Message, state: FSMContext):
    admins = secrets.get_admins()
    if msg.from_user.id in admins:
        if msg.text == "/send":
            data = await state.get_data()
            await msg.bot.send_audio(secrets.get_channel()[0], data.get("audio"), caption=data.get("ms"),
                                     parse_mode='HTML')
            await msg.answer("Пост успешно отправлен!")
            await state.finish()
        else:
            await msg.answer("Пожалуйста отправьте /send, или /cancel")
    else:
        await msg.answer("Вы не администратор!")


async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())
