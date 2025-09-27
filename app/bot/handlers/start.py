from aiogram import Router, types
from aiogram.filters import Command

from app.db import async_session_maker
from app.models.users import User


router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):

    ref_code = None
    parts = message.text.split()
    if len(parts) > 1:
        ref_code = parts[1]

    async with async_session_maker() as session:
        result = await session.get(User, message.from_user.id)
        if not result:
            user = User(
                id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name,
                referral_code=ref_code
            )
            session.add(user)
            await session.commit()
            await message.answer("✅ You have been registered!")
        else:
            await message.answer("👋 Welcome back!")