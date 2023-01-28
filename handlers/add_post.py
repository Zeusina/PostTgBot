from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from utils import SampleUtils, ConfigUtils
from utils import LoggingUtils
from os import getenv

log = LoggingUtils("handlers.add_post").log
config = ConfigUtils().config_parse()


class AddPost(StatesGroup):
    def __init__(self):
        log.info("FSM states initialized!")

    waiting_for_number = State()
    waiting_for_name = State()
    waiting_for_words_count = State()
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


async def add_channel(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(words=msg.text)
        await types.ChatActions.upload_audio()
        await msg.answer("Пожалуйста отправьте изложение", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddPost.checking)
    else:
        await msg.answer("Пожалуйста отправьте число")


async def add_music_file(msg: types.Message, state: FSMContext):
    await state.update_data(getenv("CHAT_ID"))
    await types.ChatActions.upload_audio()
    await msg.answer("Пожалуйста отправьте музыкальный файл")
    await state.set_state(AddPost.checking)



async def check(msg: types.Message, state: FSMContext):
    await state.update_data(audio=msg.audio.file_id)
    data = await state.get_data()
    sample = SampleUtils().get_sample()
    message = ""
    message += (sample.get('name').replace('%name%', data.get('name')) + "\n")
    message += (sample.get('number').replace('%number%', data.get('number')) + "\n")
    message += (sample.get('words').replace('%words%', data.get('words')) + "\n")

    await msg.answer("Проверьте получившийся пост:")
    await msg.answer_audio(data.get("audio"), caption=message, parse_mode='HTML')
    await msg.answer("Если все верно, то отправьте /send, иначе /cancel")
    await state.update_data(ms=message)
    await state.set_state(AddPost.waiting_for_send)


async def send(msg: types.Message, state: FSMContext):
    if msg.from_user.id == int(getenv("ADMIN_ID")):
        if msg.text == "/send":
            data = await state.get_data()
            await msg.bot.send_audio(-int(getenv("CHAT_ID")), data.get("audio"), caption=data.get("ms"), parse_mode='HTML')
            await msg.answer("Пост успешно отправлен!")
            await state.finish()
        else:
            await msg.answer("Пожалуйста отправьте /send, или /cancel")
    else:
        await msg.answer("Вы не администратор!")


async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())
