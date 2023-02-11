from aiogram.types import KeyboardButton, KeyboardButtonRequestChat
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.structures.get_chat_administrator_rights import get_adminstrator_rigts

add_post_keyboard = ReplyKeyboardBuilder().add(KeyboardButton(text="Добавить пост",
                                                              request_chat=KeyboardButtonRequestChat(
                                                                  chat_is_channel=True,
                                                                  bot_is_member=True,
                                                                  bot_administrator_rights=get_adminstrator_rigts(
                                                                      can_post_messages=True),
                                                                  user_administrator_rights=get_adminstrator_rigts(
                                                                      can_post_messages=True),
                                                                  request_id=1)
                                                              )).as_markup()
