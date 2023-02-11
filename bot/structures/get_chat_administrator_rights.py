from aiogram.types import ChatAdministratorRights


def get_adminstrator_rigts(is_anonymous: bool = False, can_manage_chat: bool = False, can_change_info: bool = False,
                           can_post_messages: bool = False, can_edit_messages: bool = False,
                           can_delete_messages: bool = False,
                           can_manage_voice_chats: bool = False, can_invite_users: bool = False,
                           can_restrict_members: bool = False, can_pin_messages: bool = False,
                           can_promote_members: bool = False, can_manage_video_chats: bool = False):
    return ChatAdministratorRights(is_anonymous=is_anonymous, can_manage_chat=can_manage_chat,
                                   can_change_info=can_change_info, can_post_messages=can_post_messages,
                                   can_edit_messages=can_edit_messages, can_delete_messages=can_delete_messages,
                                   can_manage_voice_chats=can_manage_voice_chats, can_invite_users=can_invite_users,
                                   can_restrict_members=can_restrict_members, can_pin_messages=can_pin_messages,
                                   can_promote_members=can_promote_members,
                                   can_manage_video_chats=can_manage_video_chats)
