from aiogram import Bot
from aiogram.types import Message, User
import pyrogram

async def check_user_can_message(user_id: int, bot: Bot):
    try:
        await bot.send_chat_action(user_id, action="typing")
        return True
    except:
        return False

async def is_bot_allowed_to_write_every_group_user(users_list: set, bot: Bot):
    try:
        print(users_list)
        all_have_access = []
        for member in users_list:
            if not await check_user_can_message(member, bot):
                all_have_access.append(member)
            else:
                continue
        return all_have_access
    except Exception as e:
        print('uh')

async def get_username_by_id(bot: Bot, user_id: int, chat_id: int) -> str:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        user: User = member.user
        return user.username if user.username else "Username not set"
    except Exception as e:
        return str(e)