import asyncio

import handlers
from config import load_config
from aiogram import Bot, Dispatcher

from middlewares import CheckAdminPermissions


# from middlewares import ChatTypeMiddleware


async def main():
    config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    handlers.start_handlers.local_router.message.filter(
        lambda message: message.chat.type in ['private'])

    handlers.group_handlers.group_router.message.filter(
        lambda message: message.chat.type in ['group','supergroup'])

    handlers.gameplay_router.message.middleware.register(CheckAdminPermissions())
    dp.include_routers(
        handlers.start_handlers.local_router,
        handlers.group_handlers.group_router,
        handlers.gameplay_handlers.gameplay_router
    )
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())
