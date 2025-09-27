from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from app.db import async_session_maker
from app.models.users import User
from app.models.locations import Location

router = Router()


@router.message(Command("location"))
async def request_location(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📍 Send location",
                                  request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Please share your location:", reply_markup=keyboard)


@router.message(lambda message: message.location is not None)
async def save_location(message: types.Message):
    async with async_session_maker() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            await message.answer("You need to start the bot first with /start")
            return

        # Check if location already exists for this user
        stmt = select(Location).where(Location.user_id == user.id)
        result = await session.execute(stmt)
        existing_location = result.scalar_one_or_none()

        if existing_location:
            # Update existing location
            existing_location.latitude = message.location.latitude
            existing_location.longitude = message.location.longitude
            existing_location.updated_at = datetime.utcnow()
            await session.commit()
            action_text = "Location updated!"
        else:
            # Create new location
            loc = Location(
                user_id=user.id,
                latitude=message.location.latitude,
                longitude=message.location.longitude
            )
            session.add(loc)
            await session.commit()
            action_text = "Location saved!"
            existing_location = loc

        await message.answer(
            f"{action_text} 🌍\nLatitude: {existing_location.latitude}\nLongitude: {existing_location.longitude}",
            reply_markup=types.ReplyKeyboardRemove()
        )
