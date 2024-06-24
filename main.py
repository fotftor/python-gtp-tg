import asyncio
import os

from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message,
)

router = Router()

STEP1_EXTEND_CB = "extend"
STEP1_COLLAPSE_CB = "collapse"
STEP1_SETTINGS_CB = "settings"

ADDITIONAL_TEXT = "Here is some additional text, which is visible only in extended mode"


@router.message(CommandStart())
async def step1(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="[ ] Extended mode",
                             callback_data=STEP1_EXTEND_CB),
        InlineKeyboardButton(text="Settings", callback_data=STEP1_SETTINGS_CB),
    ]])
    await message.answer(
        f"Hello, {message.from_user.username}. \n\n"
        "Extended mode is off.",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == STEP1_EXTEND_CB)
async def step1_check(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="[x] Extended mode",
                             callback_data=STEP1_COLLAPSE_CB),
        InlineKeyboardButton(text="Settings", callback_data=STEP1_SETTINGS_CB),
    ]])
    await callback.message.edit_text(
        f"Hello, {callback.from_user.username}. \n\n"
        "Extended mode is on.\n\n" + ADDITIONAL_TEXT,
        reply_markup=keyboard,
    )


@router.callback_query(F.data == STEP1_COLLAPSE_CB)
async def step1_uncheck(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="[ ] Extended mode",
                             callback_data=STEP1_EXTEND_CB),
        InlineKeyboardButton(text="Settings", callback_data=STEP1_SETTINGS_CB),
    ]])
    await callback.message.edit_text(
        f"Hello, {callback.from_user.username}. \n\n"
        "Extended mode is off.",
        reply_markup=keyboard,
    )


async def main():
    bot = Bot(token=os.getenv('6739658967:AAGYbweREeDh_vCzhyFZtAHryFTMPCwpAn0'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


asyncio.run(main())