from aiogram.fsm.state import StatesGroup, State


class GetOrderState(StatesGroup):
    order_id = State()


class GetProductDetails(StatesGroup):
    vendor_code = State()
