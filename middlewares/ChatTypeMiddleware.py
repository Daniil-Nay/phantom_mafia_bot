# from typing import Callable, Dict, Any, Awaitable
#
# from aiogram import BaseMiddleware, Router
# from aiogram.types import Message
# from aiogram.dispatcher.event.telegram import TelegramEventObserver
# from handlers import r
#
# class ChatTypeMiddleware(BaseMiddleware):
#     async def __call__(
#             self,
#             handler: Callable[[Message,Dict[str,Any]], Awaitable[Any]],
#             event: Message,
#             data: Dict[str, Any]
#     )->Any:
#         chat_type = event.chat.type
#         match chat_type:
#             case ['group', 'supergroup']
#                 data['is_group_chat'] = True
#             case _:
#                 data['is_group_chat'] = True
#         else:
#             return await handler(event, data)
