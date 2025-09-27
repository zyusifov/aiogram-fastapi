from aiogram import Router, types
from aiogram.filters import Command


router = Router()

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("ℹ️ Available commands:\n/start - Start bot\n/help - Show help\n/location - Add your location")
