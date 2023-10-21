import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import common, create_request, archive, about


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.token)

    dp.include_router(common.router)
    dp.include_router(create_request.router)
    dp.include_router(archive.router)
    dp.include_router(about.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
