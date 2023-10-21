from aiogram import F, Router, types
import sqlite3

router = Router()


@router.callback_query(F.data == "archive")
async def history(callback: types.CallbackQuery):
    connection = sqlite3.connect('database/users_requests.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM User_{user_id}'.format(user_id=callback.from_user.id))
    results = cursor.fetchall()
    connection.close()

    if results:
        await callback.message.answer(text='Сейчас отслеживаются:')
        for row in results:
            date = row[1]
            market = row[2]
            url = row[3]
            title = row[4]
            current_price = row[5]
            desired_price = row[6]
            img = row[7]

            text = '\U0001F550 Дата начала отслеживания\n{date}\n\n' \
                   '\U0001F6D2 Магазин: {market}\n\n' \
                   '\U0001F4E6 Наименование товара:\n<a href="{url}">{title}</a>\n\n' \
                   '\U0001F3F7 Текущая цена: {current_price}\n\n' \
                   '\U0001F3F7 Желаемая цена: {desired_price}' \
                .format(date=date, market=market, title=title, url=url,
                        current_price=current_price, desired_price=desired_price)

            await callback.message.answer_photo(photo=img, caption=text, parse_mode='HTML')
        await callback.message.answer(text='Хотите продолжить работу с ботом? /start')

    else:
        await callback.message.answer(text='\U0000274C Ваша история поиска пуста! \U0000274C')
        await callback.message.answer(text='Хотите продолжить работу с ботом? /start')

