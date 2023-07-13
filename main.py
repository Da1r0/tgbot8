import asyncio  # Работа с асинхронностью

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config  # Config
from handlers.common import common_router
from handlers.fill_form import fill_form_router
from keyboards.menu import menu


def register_all_routers(dp: Dispatcher):
    dp.include_router(common_router)
    dp.include_router(fill_form_router)


async def main():
    bot = Bot(token=config.token)
    dp = Dispatcher(storage=MemoryStorage())  # Менеджер бота

    register_all_routers(dp)

    try:
        print('Bot Started')
        await bot.set_my_commands(menu)
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == '__main__':  # Если мы запускаем конкретно этот файл.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
