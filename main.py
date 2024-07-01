import asyncio
import config
import aiogram
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,Message
from aiogram import html
import string,random
from openai import OpenAI
import openai


logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
bot = Bot('your_tg_key')
messages = []

class tg:

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer(
            f"Hello, {html.bold(html.quote(message.from_user.full_name))}",
            parse_mode=ParseMode.HTML
        )
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню:")
        button_1 = KeyboardButton("генерация пароля")
        keyboard.add(button_1)

    @dp.message()
    async def gen_gpt(message: types.Message):
        global messages
        messages.append({"role": 'user', "content": message.text})
        try:
            client = openai.OpenAI(
                api_key='you_api',
                base_url="https://api.proxyapi.ru/openai/v1")
            chat_completion = client.chat.completions.create(model="gpt-4o-2024-05-13",
                                                             messages=[{"role": "user", "content": message.text}])
            response = chat_completion.choices[0].message.content
            await message.answer(response)
            messages.append({"role": 'assistant', "content": response})
        except Exception as e:
            logging.error(f"Error: {e}")
            await message.answer("Error occurred. Please try again later.")
    # Запуск процесса поллинга новых апдейтов
    async def main(self):
        await dp.start_polling(bot)



if __name__ == "__main__":
    tg_bot=tg()
    asyncio.run(tg_bot.main())
