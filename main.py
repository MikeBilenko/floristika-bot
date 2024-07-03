import os
import asyncio
from aiogram import Router
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import keyboards
from language import (
    get_selected_language,
    load_state,
    save_state,
)
from db import API
from messages import (
    messages,
    order_status_translations,
)
from icons import language_icons
from states import (
    GetOrderState,
    GetProductDetails,
)
from aiogram.fsm.context import FSMContext

router = Router()
bot = Bot(token=os.getenv("TELEGRAM_API_KEY"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(CommandStart())
async def start(message: Message):
    try:
        user_id = message.from_user.id
        language = get_selected_language(user_id)
        await message.answer(
            text=messages[language]["greeting"],
            reply_markup=keyboards.get_main_kb(user_id),
        )
    except:
        await message.answer(
            f"Hello {message.from_user.first_name}\n"
            f"Please choose language first: \n",
            reply_markup=keyboards.language_mk,
        )


@router.callback_query(lambda query: "lang_" in query.data)
async def process_language_callback(callback_query: types.CallbackQuery):
    language = callback_query.data.replace("lang_", "")
    user_id = callback_query.from_user.id
    state = load_state()
    state[user_id] = language
    save_state(state)
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )
    await callback_query.answer()
    await callback_query.message.answer(language_icons[language])
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id)
    )


@router.callback_query(lambda query: query.data == "support")
async def process_support_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    selected_language = get_selected_language(user_id)

    await callback_query.message.answer(
        messages[selected_language]["support"]
    )
    await bot.send_message(
        os.getenv("MANAGER_CHAT_ID"),
        f"New support request from "
        f"{callback_query.from_user.full_name} "
        f"{callback_query.from_user.last_name if callback_query.from_user.last_name else ''}.")
    await callback_query.message.answer("<a href='https://t.me/floristika_assistant_bot'>@floristika_assistant_bot</a>")

@router.callback_query(lambda query: query.data == "stores")
async def get_stores_data(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    stores = API.get_stores()
    for store in stores:
        message = ""
        message += f"🏢 *{store.get('name')}*\n"
        message += f"🌍 *{messages[language]['country']}:* ({store.get('country')})\n"
        message += f"📍 *{messages[language]['address']}:* {store.get('address')}, {store.get('city')}, {store.get('postal_code')}\n"
        message += f"📞 *{messages[language]['phone_number']}:* {store.get('phone_number')}\n\n"
        await callback_query.message.answer(message)

    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id)
    )


@router.callback_query(lambda query: query.data == "product")
async def get_product_details(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await state.set_state(GetProductDetails.vendor_code)
    await callback_query.message.answer(
        messages[language]["enter_vendor"],
        reply_markup=keyboards.get_product_back(user_id)
    )


@router.callback_query(lambda query: query.data == "order-status")
async def get_order_status(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await state.set_state(GetOrderState.order_id)
    await callback_query.message.answer(
        messages[language]["enter_order"],
        reply_markup=keyboards.get_back_order(user_id)
    )


@router.callback_query(lambda query: query.data == "back_order")
async def back_to_previous_state(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await state.clear()
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id)
    )


@router.callback_query(lambda query: query.data == "back_product")
async def back_to_previous_state_product(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await state.clear()
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id)
    )


@router.message(GetOrderState.order_id)
async def get_order_status_details(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_selected_language(user_id)
    if message.text:
        await state.update_data(order_id=message.text)
        data = await state.get_data()
        await state.clear()
        order = API.get_order_status(data["order_id"])
        if order:
            await message.answer(order_status_translations[language][order.get("status")])
            await message.answer(
                f"{messages[language]['select']}: ",
                reply_markup=keyboards.get_main_kb(user_id)
            )
        else:
            await message.answer(messages[language]['no_order'])
            await message.answer(
                f"{messages[language]['select']}: ",
                reply_markup=keyboards.get_main_kb(user_id)
            )

    else:
        await message.answer(messages[language]['correct_id'])


@router.message(GetProductDetails.vendor_code)
async def get_product_details(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_selected_language(user_id)
    if message.text:
        await state.update_data(vendor_code=message.text)
        data = await state.get_data()
        await state.clear()
        product = API.get_product(data['vendor_code'])
        if product:

            image = product.get("images")[0].get("image")
            await message.answer(f"{product.get(f'name_{language}')}")
            await message.answer_photo(image)
            await message.answer(f"{messages[language]['price']}: {product.get('price')}€")
            await message.answer(f"{messages[language]['category']}: {product.get('category').get(f'name_{language}')}")
            await message.answer(
                f"{messages[language]['subcategory']}: {product.get('subcategory').get(f'name_{language}')}")
            await message.answer(f"{messages[language]['color']}: {product.get('color').get(f'name_{language}')}")
            await message.answer(f"{messages[language]['size']}: {product.get('size').get(f'name_{language}')}")
            await message.answer(f"{messages[language]['review']}: {product.get('rate')}")
            await message.answer(f"{messages[language]['vendor_code']}: {product.get('vendor_code_public')}")
            await message.answer(f"<a "
                                 f"href='https://floristika.life/products/{product.get('category').get('slug')}/{product.get('subcategory').get('slug')}/{product.get('slug')}/'>"
                                 f"{messages[language]['see_more']}"
                                 f"</a>")
            await message.answer(f"{messages[language]['select']}: ", reply_markup=keyboards.get_main_kb(user_id))
        else:
            await message.answer(messages[language]['no_product'])
            await message.answer(f"{messages[language]['select']}: ", reply_markup=keyboards.get_main_kb(user_id))

    else:
        await message.answer(messages[language]['correct_id'])


@router.callback_query(lambda query: query.data == "cooperation")
async def get_cooperation(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await callback_query.message.answer(
        messages[language]["cooperation"],
    )
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id),
    )


@router.callback_query(lambda query: query.data == "choose-language")
async def get_choose_language(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await callback_query.message.answer(

        messages[language]["select_language"],
        reply_markup=keyboards.language_mk,
    )


@router.callback_query(lambda query: query.data == "retail")
async def get_retail_data(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await callback_query.message.answer(
        messages[language]["retail"],
    )
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id),
    )


@router.callback_query(lambda query: query.data == "important")
async def get_important(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await callback_query.message.answer(
        messages[language]["important"],
    )
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id),
    )


@router.callback_query(lambda query: query.data == "minimum_order")
async def get_minimum_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await callback_query.message.answer(
        messages[language]["minimum_order"],
    )
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id),
    )


@router.callback_query(lambda query: query.data == "payment")
async def get_payment(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await callback_query.message.answer(
        messages[language]["payment"],
    )
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id),
    )


@router.callback_query(lambda query: query.data == "order_duration")
async def get_payment(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = get_selected_language(user_id)
    await callback_query.message.answer(
        messages[language]["order_duration"],
    )
    await callback_query.message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id),
    )


@router.message()
async def echo(message: Message):
    user_id = message.from_user.id
    language = get_selected_language(user_id)

    await message.answer(
        f"{messages[language]['select']}: ",
        reply_markup=keyboards.get_main_kb(user_id),
    )


async def main() -> None:
    dp = Dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(
        router,
    )
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
