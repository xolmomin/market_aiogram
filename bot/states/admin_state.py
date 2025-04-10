from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    admin_menu = State()


class AddCategory(StatesGroup):
    name = State()


class ChangeCategory(StatesGroup):
    choice = State()
    name = State()


class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    quantity = State()
    image = State()
    category_id = State()
