from aiogram import types
from aiogram.fsm.context import FSMContext

from ..structures.fsm_groups import AddPostStates
from bot.structures.keyboards import add_post_keyboard


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
        keyboard = add_post_keyboard
        await message.answer("Пожалуйста отправьте канал для публикации", reply_markup=keyboard)
        await state.set_state(AddPostStates.waiting_for_channel)
        await state.update_data(file_id=message.audio.file_unique_id)
    else:
        await message.answer("Пожалуйста отправьте музыкальный файл изложения")


async def add_post_check(message: types.Message, state: FSMContext) -> None:
    await message.answer("Пожалуйста проверьте получившийся пост.")
    await state.set_state(AddPostStates.waiting_for_send)


async def add_post_send(message: types.Message, state: FSMContext) -> None:
    await message.answer("Пост отправлен.")
    await state.clear()


async def cancel_add_post(message: types.Message, state: FSMContext) -> None:
    await message.answer("Отменено")
    await state.clear()
