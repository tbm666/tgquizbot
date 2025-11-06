import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from config import API_TOKEN
from db import init_db
from quiz_logic import new_quiz, handle_answer
from keyboards import main_menu_keyboard
from stats import generate_score_chart

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Добро пожаловать в квиз 🤖", reply_markup=main_menu_keyboard())


@dp.message(F.text == "🎮 Начать игру")
async def cmd_quiz(message: types.Message):
    await message.answer("🚀 Начинаем квиз!")
    await new_quiz(message)


@dp.message(F.text == "📊 Результаты")
async def cmd_results(message: types.Message):
    path = await generate_score_chart()
    if path:
        await message.answer_photo(photo=types.FSInputFile(path), caption="📈 Топ игроков")
    else:
        await message.answer("Пока нет результатов 😔")


@dp.callback_query()
async def callback_router(callback: types.CallbackQuery):
    await handle_answer(callback)


async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
