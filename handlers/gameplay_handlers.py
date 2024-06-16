import asyncio
import random
import string

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.methods import GetChatMemberCount
from aiogram.types import ChatMemberUpdated, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from handlers.async_defs import is_bot_allowed_to_write_every_group_user, get_username_by_id
from handlers.distribution_of_roles import RolesDistribution

gameplay_router: Router = Router()
game_active = False

participants = set()
global sent_message
@gameplay_router.message(
    Command('play'),
)


async def generate_room_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
async def start_game_welcoming_button(message: Message, bot: Bot):
    global sent_message, game_active
    participate_btn = create_participate_button(0)
    if game_active:
        await message.answer(
            text = 'игра уже начата'
        )
    else:
        game_active = True
        sent_message = await message.answer(
                text = "Игра началась! Нажмите кнопку ниже, чтобы принять участие.",
                reply_markup=participate_btn)
        await asyncio.sleep(10)

        users_with_no_int = await is_bot_allowed_to_write_every_group_user(
            users_list = participants,
            bot = bot
        )
        cons = [await get_username_by_id(bot = bot,user_id = user__id,chat_id = sent_message.chat.id,) for user__id in users_with_no_int]
        con = ', '.join(cons)
        con = '@' + con if con else ""
        is_con_empty = len(con)==0
        room_id = generate_room_id
        ## нужно еще рассмотреть мин колво участников
        if is_con_empty:
            text = (f'Успешно. Начинается процесс распределения ролей.\n'
                    f'Просьба всех участников проверить ЛС\n'
                    f'Participants {participants}')
        else:
            text = (f'Ошибка. Следующие участники не запустили бота:\n'
                    f'Участники без доступа {con}\n'
                    f'Без доступа к боту нет возможности выдать роли в ЛС.\n'
                    f'Запустите бота @phantom_mafia_players_bot')
        await bot.edit_message_text(
            chat_id = sent_message.chat.id,
            message_id = sent_message.message_id,
            text = text
        )

        # obj = RolesDistribution(participants, room_id)
        # obj.get_info()
        # await obj._distribute_roles(
        #     bot = bot)

def create_participate_button(count: int):
    button = [
        [
            InlineKeyboardButton(
                text= f"Принять участие? {count} чел",
                callback_data="join_game"
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard


@gameplay_router.callback_query(F.data=='join_game')
async def join_game(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id

    if user_id not in participants:
        participants.add(user_id)
        await callback_query.answer("Вы приняли участие в игре!")
        await update_participants_count(callback_query.message.chat.id, callback_query)
    else:
        await callback_query.answer("Вы уже принимаете участие в игре.")

async def update_participants_count(chat_id, callback_query):
    global sent_message
    count = len(participants)
    participate_btn = create_participate_button(count)
    await callback_query.bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=sent_message.message_id,
        reply_markup=participate_btn
    )
# async def check():
#     try:
#         text = ''
#         member_count = await bot.get_chat_member_count(message.chat.id)
#         min_needed_to_begin: int = 5
#         users: list  = await is_bot_allowed_to_write_every_group_user(message, bot)
#         if (member_count < min_needed_to_begin) and users:
#             text = (f'Для начала игры нужно минимальное количество игроков - 6 ч.\n'
#                     f'На данный момент {member_count}')
#         elif (member_count >= min_needed_to_begin) and users:
#             text = (f'Отлично. Начинаем игру по стандартным настройкам.'
#                     f'Идет процесс распределения ролей. '
#                     f'Зайдите, пожалуйста, в ЛС с телеграм ботом')
#         elif users==False:
#             text = 'Ошибка'
#
#         await message.answer(
#         text=text
#         )
#     except Exception as e:
#         await message.answer(f"Не удалось получить количество участников: {e}")