from aiogram.types import BotCommand

main_menu_command = [
    BotCommand(command='/start', description='Перезапустить'),
    BotCommand(command='/help', description='Помощь'),
    BotCommand(command='/show', description='Данные')
]
