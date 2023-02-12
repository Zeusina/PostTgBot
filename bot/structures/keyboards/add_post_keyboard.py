from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestChat

from bot.structures.get_chat_administrator_rights import get_administrator_rights

ADD_POST_BOARD_CHANNEL = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text="Проверить", request_chat=KeyboardButtonRequestChat(
        request_id=1,
        chat_is_channel=True,
        user_administrator_rights=get_administrator_rights(can_post_messages=True, can_edit_messages=True,),
        bot_administrator_rights=get_administrator_rights(can_post_messages=True, can_edit_messages=True,)
    ))],
])
