from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from botrequests import apsched

import sqlite3

router = Router()

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    connection = sqlite3.connect('database/users_requests.db')
    cursor = connection.cursor()

    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS User_{message.from_user.id} (
            id INTEGER PRIMARY KEY,
            joiningDate timestamp,
            market TEXT,
            url TEXT,
            title TEXT,
            current_price INTEGER,
            desired_price INTEGER,
            img TEXT
            )
            ''')

    connection.commit()
    connection.close()

    if not scheduler.get_jobs():
        scheduler.add_job(apsched.send_message_cron, trigger='cron', hour='21', jitter=3600, kwargs={'message': message})
        scheduler.start()

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="\U0001F4E5 Создать запрос", callback_data="create_request"))
    builder.add(types.InlineKeyboardButton(text="\U0001F4DA Архив отслеживаний", callback_data="archive"))
    builder.add(types.InlineKeyboardButton(text="\U00002753 О боте", callback_data="about"))
    builder.adjust(2)
    await message.answer('\U0001F44B Привет, {}!\n\n\U0001F50D Начнём охоту на лучшие цены!'.format(message.from_user.first_name),
                         reply_markup=builder.as_markup())
