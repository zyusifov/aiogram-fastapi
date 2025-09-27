from fastapi import FastAPI, Request
from aiogram import types
from app.admin import init_admin
from app.bot.dispatcher import bot, dp
from app.bot.handlers import routers
from app.config import WEBHOOK_URL
from app.db import init_db

app = FastAPI()

for r in routers:
    dp.include_router(r)


@app.on_event("startup")
async def on_startup():
    await init_db()
    init_admin(app)
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
