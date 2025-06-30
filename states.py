from aiogram.fsm.state import StatesGroup, State

class OrderState(StatesGroup):
    choosing = State()
    entering_quantity = State()
    adding_name = State()
    adding_price = State()