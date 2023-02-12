from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendAudio
from aiogram.types import ReplyKeyboardRemove

from ..structures.fsm_groups import AddPostStates
from bot.structures.keyboards.add_post_keyboard import ADD_POST_BOARD_CHANNEL


async def add_post_command(message: types.Message, state: FSMContext) -> None:
    await message.answer("Пожалуйста отправьте номер изложения")
    await state.set_state(AddPostStates.waiting_for_number)


async def add_post_number(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await message.answer("Пожалуйста отправьте название изложения")
        await state.set_state(AddPostStates.waiting_for_name)
        await state.update_data(number=message.text)
    else:
        await message.answer("Пожалуйста отправьте число")


async def add_post_name(message: types.Message, state: FSMContext) -> None:
    await message.answer("Пожалуйста отправьте количество слов")
    await state.set_state(AddPostStates.waiting_for_words_count)
    await state.update_data(name=message.text)


async def add_post_words_count(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await message.answer("Пожалуйста отправьте файл изложения")
        await state.set_state(AddPostStates.waiting_for_file)
        await state.update_data(words_count=message.text)
    else:
        await message.answer("Пожалуйста отправьте число")


async def add_post_file(message: types.Message, state: FSMContext) -> None:
    if message.audio:
        await message.answer("Пожалуйста отправьте канал для публикации", reply_markup=ADD_POST_BOARD_CHANNEL)
        await state.set_state(AddPostStates.waiting_for_channel)
        await state.update_data(file_id=message.audio.file_id)
    else:
        await message.answer("Пожалуйста отправьте музыкальный файл изложения")


async def add_post_check(message: types.Message, state: FSMContext) -> None:
    chat = message.chat_shared.chat_id
    data = await state.get_data()
    await state.update_data(channel=chat)
    msg = "Название изложения: <code>%name%</code>\n".replace("%name%", data.get("name"))
    msg += "Номер изложения: <code>%number%</code>\n".replace("%number%", data.get("number"))
    msg += "Количество слов: <code>%words_count%</code>".replace("%words_count%", data.get("words_count"))
    await message.answer("Пожалуйста проверьте получившийся пост.", reply_markup=ReplyKeyboardRemove())
    await message.answer_audio(caption=msg, parse_mode="HTML", audio=data.get("file_id"))
    await message.answer("Если все верно, то отправьте /send, иначе /cancel")
    await state.set_state(AddPostStates.waiting_for_send)
    await state.update_data(msg=msg)


async def add_post_send(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await SendAudio(chat_id=data.get("channel"), caption=data.get("msg"), parse_mode="HTML",
                    audio=data.get("file_id"))
    await message.answer("Пост отправлен.")
    await state.clear()


async def cancel_add_post(message: types.Message, state: FSMContext) -> None:
    await message.answer("Отменено", reply_markup=ReplyKeyboardRemove())
    await state.clear()
