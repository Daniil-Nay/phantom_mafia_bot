from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Router
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message
from aiogram.dispatcher.event.telegram import TelegramEventObserver

class CheckAdminPermissions(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message,Dict[str,Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    )->Any:
        chat_type = event.chat.type in ['group', 'supergroup']
        if chat_type:
            try:
                is_admin = (await event.bot.get_chat_member(event.chat.id,event.bot.id)).status == ChatMemberStatus.ADMINISTRATOR
                print(is_admin)
                if is_admin:
                    return await handler(event,data)
                else:
                    await event.answer("У бота нет административных прав в этом чате.")
            except Exception as e:
                await event.answer("Бот заблокирован в этом чате.",e)

        else:
            await event.answer("Эта команда доступна только в групповых чатах и супергруппах.")



