import sqlite3
import os
from aiogram.types import Message
from botrequests import aliexpress


async def send_message_cron(message: Message):
    if os.path.exists('database/users_requests.db'):
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

            title1, img1, price = aliexpress.request(url)

            if price <= desired_price:
                text = '\U00002705Цена на товар достигла желаемого уровня:\U00002705\n\n' \
                       '\U0001F6D2 Магазин: {market}\n\n' \
                       '\U0001F4E6 Наименование товара:\n<a href="{url}">{title}</a>\n\n' \
                       '\U0001F3F7 Текущая цена: {current_price}\n\n' \
                       '\U0001F3F7 Желаемая цена: {desired_price}' \
                    .format(market=market, title=title, url=url, current_price=current_price,
                            desired_price=desired_price)

                await message.answer_photo(photo=img, caption=text, parse_mode='HTML')
                cursor.execute('DELETE FROM User_{user_id} WHERE id = ?'.format(user_id=message.from_user.id), ('{}'.format(row[0]),))
                connection.commit()
            else:
                await message.answer('<a href="{url}">{title}</a>\n\U0000274Cпока без изменений\U0000274C'.format(title=title, url=url), parse_mode='HTML')
        connection.close()
