from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.config import BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode="HTML",
        protect_content=True
    )
)
dp = Dispatcher()
