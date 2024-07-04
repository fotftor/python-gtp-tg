import asyncio
import aiogram
import logging
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import openai
import os
from dotenv import load_dotenv


load_dotenv('api.env')
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
bot = Bot(os.getenv("TOKEN"))
messages = []
image=[]

class tg:

    @dp.message(Command("start"))
    async def cmd_start(self,message: types.Message):
        await message.answer(f"Hello")


    @dp.message()
    async def gen_gpt(self,message: types.Message):
        global messages
        messages.append({"role": 'user', "content": message.text})
        try:
            model = "gpt-4o-2024-05-13"
            client = openai.OpenAI(
                api_key=os.getenv("DOMAIN"),
                base_url="https://api.proxyapi.ru/openai/v1")
            chat_completion = client.chat.completions.create(model=model,messages=[{"role": "user", "content": message.text}])
            response = chat_completion.choices[0].message.content
            await message.answer(response)
            messages.append({"role": 'assistant', "content": response})
        except Exception as e:
            logging.error(f"Error: {e}")
            await message.answer("Error occurred. Please try again later.")

    @dp.message(Command("image"))
    async def image_handler(self,message: Message):
        global image
        image.append({"role": 'user', "content": message.text})
        try:
            model = "dall-e-3"
            client = openai.OpenAI(
                api_key=os.getenv("DOMAIN"),
                base_url="https://api.proxyapi.ru/openai/v1")

            chat_completion1 = client.chat.completions.create(model=model,messages=[{"role": "user", "content": message.text}])
            response1 = chat_completion1.images.generate(
                model="dall-e-3",
                prompt=message.text[4:].split(maxsplit=1),
                n=1,
                size="1024x1024",
            )
            await message.answer_photo(response1.data.url)
        except Exception as e:
            logging.error(f"Error: {e}")
            await message.answer("Error occurred. Please try again later.")


    async def main(self):
        await dp.start_polling(bot)



if __name__ == "__main__":
    tg_bot=tg()
    asyncio.run(tg_bot.main())

