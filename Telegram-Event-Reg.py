import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Начать Регистрацию')]
])

class Reg(StatesGroup):
    name = State()

ADMIN_ID = 'ВАШ ID'

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!', reply_markup=keyboard)

@dp.message(F.text == 'Начать Регистрацию')
async def regg(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введи имя и фамилию', reply_markup=ReplyKeyboardRemove())

@dp.message(Reg.name)
async def good(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    user = message.from_user
    text = f'📩 Новая заявка: \nИмя: {data['name']} \nID: {user.id} \nUsername: @{user.username}'
    await message.bot.send_message(ADMIN_ID, text)
    await message.answer(f'Регистрация завершена, Ваши данные: {data['name']}')
    await state.clear()

async def main():
    bot = Bot(token="ВАШ ТОКЕН")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())