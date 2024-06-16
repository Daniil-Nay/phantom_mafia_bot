from aiogram import Bot, exceptions, types
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.router import Router



local_router: Router = Router()


@local_router.message(Command('start'))
async def start_handler(message: Message):
    print(message.chat.type)
    await message.answer(
        text='Для начала добавьте бота в беседу'
    )

