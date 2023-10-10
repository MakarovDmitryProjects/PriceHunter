from aiogram import F, Router, types

router = Router()


@router.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    await callback.message.answer(text='Бот ежедневно, в период с 20 до 22 часов, проверяет запросы пользователя и, '
                                       'если цена достигла указанного значения, сообщает об этом.\n\n'
                                       'Кнопка <b>Создать запрос</b>: Запускает процесс создания запроса. '
                                       'Необходимо передать ссылку на интересующий товар и желаемую максимальную цену\n\n'
                                       'Кнопка <b>Архив отслеживаний</b>: Выводит все имеющиеся незавершенные запросы',
                                  parse_mode='HTML')
