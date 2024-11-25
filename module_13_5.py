# Тема "Клавиатура кнопок".
# Задача "Меньше текста, больше кликов":

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
info = KeyboardButton(text='Информация')
calc = KeyboardButton(text='Рассчитать')
kb.add(info)
kb.add(calc)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer("Введите свой возраст (гд):")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer("Введите свой пол (m/f):")
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text)

    data = await state.get_data()  # UserState.age,UserState.growth,UserState.weight)
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    gender = str(data['gender'])

    """
    Упрощенный вариант формулы Миффлина - Сан Жеора:
    для мужчин: 10 х вес(кг) + 6, 25 x рост(см) – 5 х возраст(г) + 5;
    для женщин: 10 x вес(кг) + 6, 25 x рост(см) – 5 x возраст(г) – 161.
    """

    if gender == 'm' or gender == 'м':
        result_man = 10 * weight + 6.25 * growth - 5 * age + 5
        await message.answer(f"Ваша дневная норма равна {int(result_man)} калорий.")
    else:
        result_woman = 10 * weight + 6.25 * growth - 5 * age - 161
        await message.answer(f"Ваша дневная норма равна {int(result_woman)} калорий.")

    await state.finish()


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


# =================================================================================================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
