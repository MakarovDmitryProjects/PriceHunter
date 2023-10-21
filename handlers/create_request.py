from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from botrequests import aliexpress
import sqlite3
import datetime

router = Router()


class RequestParameters(StatesGroup):
    market_link = State()
    desired_price = State()


@router.callback_query(F.data == 'create_request')
async def insert_link(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Укажите ссылку на интересующий товар \U0001F447')
    await state.set_state(RequestParameters.market_link)


@router.message(RequestParameters.market_link)
async def select_price(message: Message, state: FSMContext):
    if message.text.startswith('https://'):
        if 'aliexpress' in message.text:
            if aliexpress.request(message.text):
                await state.update_data(insert_link=message.text.lower())
                await message.answer(text='\U00002705 Спасибо. Теперь, пожалуйста, укажите желаемую цену \U0001F447')
                await state.set_state(RequestParameters.desired_price)
            else:
                await message.answer(text='\U0000274C Такой страницы не существует или превышен лимит запросов. Пожалуйста повторите попытку позже.')
        else:
            await message.answer(text='\U0000274C Не знаю такой магазин.\nУкажите ссылку на поддерживаемый магазин \U0001F447')
    else:
        await message.answer(text='\U0000274C Некорректная ссылка. Укажите корректную ссылку \U0001F447')


@router.message(RequestParameters.desired_price)
async def result(message: Message, state: FSMContext):
    try:
        if float(message.text):
            user_data = await state.get_data()

            title, img, current_price = aliexpress.request(user_data['insert_link'])

            connection = sqlite3.connect('database/users_requests.db')
            cursor = connection.cursor()

            cursor.execute(
                'INSERT INTO User_{user_id} (joiningDate, market, url, title, current_price, desired_price, '
                'img) VALUES (?, ?, ?, ?, ?, ?, ?)'.format(user_id=message.from_user.id),
                (datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S'), 'aliexpress', user_data['insert_link'],
                 title, current_price, message.text, img))

            connection.commit()
            connection.close()

            connection = sqlite3.connect('database/users_requests.db')
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM User_{user_id}'.format(user_id=message.from_user.id))
            results = cursor.fetchall()
            for row in results:
                market = row[2]
                url = row[3]
                title = row[4]
                current_price = row[5]
                desired_price = row[6]
                img = row[7]

            connection.close()

            text = '\U00002705 Вы добавили к отслеживанию следующий товар:\n\n' \
                   '\U0001F6D2 Магазин: {market}\n\n' \
                   '\U0001F4E6 Наименование товара:\n<a href="{url}">{title}</a>\n\n' \
                   '\U0001F3F7 Текущая цена: {current_price}\n\n' \
                   '\U0001F3F7 Желаемая цена: {desired_price}' \
                .format(market=market, title=title, url=url, current_price=current_price, desired_price=desired_price)

            await message.answer_photo(photo=img, caption=text, parse_mode='HTML')
            await message.answer(text='Хотите продолжить работу с ботом? /start')
            await state.clear()
    except:
        await message.answer(text='\U0000274C Некорректная цена.\n'
                                  'Цена должна быть числом (например 1234 или 1234.56)\n'
                                  'Укажите желаемую цену\U0001F447')
