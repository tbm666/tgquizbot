from aiogram import types
from questions import quiz_data
from db import get_quiz_state, update_quiz_state, update_user_score, add_user
from keyboards import generate_options_keyboard

async def get_question(message, user_id):
    question_index, score = await get_quiz_state(user_id)
    if question_index >= len(quiz_data):
        await message.answer(f"🏁 Квиз завершен! Ваш счёт: {score}/{len(quiz_data)}")
        await update_user_score(user_id, score)
        return

    q = quiz_data[question_index]
    kb = generate_options_keyboard(question_index, q['options'])
    await message.answer(f"🧠 Вопрос {question_index + 1}/{len(quiz_data)}:\n\n{q['question']}", reply_markup=kb)


async def handle_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    question_index, score = await get_quiz_state(user_id)

    q_idx_str, opt_idx_str = callback.data.split(":")
    q_idx, o_idx = int(q_idx_str), int(opt_idx_str)

    if q_idx != question_index:
        await callback.answer("⏳ Это старая кнопка.", show_alert=True)
        return

    correct_index = quiz_data[q_idx]['correct_option']

    if o_idx == correct_index:
        await callback.message.answer("✅ Верно!")
        score += 1
    else:
        correct_text = quiz_data[q_idx]['options'][correct_index]
        await callback.message.answer(f"❌ Неверно! Правильный ответ: {correct_text}")

    question_index += 1
    await update_quiz_state(user_id, question_index, score)
    await callback.bot.edit_message_reply_markup(chat_id=user_id, message_id=callback.message.message_id, reply_markup=None)

    await get_question(callback.message, user_id)


async def new_quiz(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    await add_user(user_id, username)
    await update_quiz_state(user_id, 0, 0)
    await get_question(message, user_id)
