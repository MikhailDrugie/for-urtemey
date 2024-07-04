import asyncio
from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config


def webapp_builder(config: Config) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text='Сюда тыкай да', web_app=WebAppInfo(url=config.HOST))
    return builder.as_markup()


async def start_bot(config: Config) -> None:
    bot = Bot(token=config.TOKEN, parse_mode=ParseMode.HTML)
    
    router = Router()
    @router.message(CommandStart())
    async def start(message: Message) -> None:
        await message.reply('Здарова заебал!', reply_markup=webapp_builder(config))
    
    dp = Dispatcher()
    print('[BOT]: including router...')
    dp.include_router(router)
    
    await bot.delete_webhook(True)
    print('[BOT]: starting polling...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    config = Config()
    try:
        asyncio.run(start_bot(config))
    except KeyboardInterrupt:
        print('[BOT]: stopped')