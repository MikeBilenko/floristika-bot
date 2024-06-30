from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from icons import language_icons
from messages import messages
from language import get_selected_language


language_mk = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{language_icons['en']} English",
                callback_data="lang_en"
            ),
            InlineKeyboardButton(
                text=f"{language_icons['ru']} Russian",
                callback_data="lang_ru"
            ),
            InlineKeyboardButton(
                text=f"{language_icons['lv']} Latvian",
                callback_data="lang_lv"
            ),
        ]
    ],
    one_time_keyboard=True,
)


def get_main_kb(user_id):
    selected_language = get_selected_language(user_id)
    main_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=messages[selected_language]["btn_order_status"],
                    callback_data="order-status"
                ),
                InlineKeyboardButton(
                    text=messages[selected_language]["btn_product"],
                    callback_data="product"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=messages[selected_language]["retail_btn"],
                    callback_data="retail",
                ),
                InlineKeyboardButton(
                    text=messages[selected_language]["cooperation_btn"],
                    callback_data="cooperation",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=messages[selected_language]["minimum_order_btn"],
                    callback_data="minimum_order",
                ),
                InlineKeyboardButton(
                    text=messages[selected_language]["payment_btn"],
                    callback_data="payment",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=messages[selected_language]["order_duration_btn"],
                    callback_data="order_duration",
                ),
                InlineKeyboardButton(
                    text=messages[selected_language]["important_btn"],
                    callback_data="important",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=messages[selected_language]["change_language_btn"],
                    callback_data="choose-language",
                ),
                InlineKeyboardButton(
                    text=messages[selected_language]["stores_btn"],
                    callback_data="stores",
                )
            ],
            [
                InlineKeyboardButton(
                    text=messages[selected_language]["btn_support"],
                    callback_data="support"
                ),
            ]
        ],
        one_time_keyboard=False,
    )
    return main_kb


def get_product_back(user_id):
    selected_language = get_selected_language(user_id)
    product_back_mk = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=messages[selected_language]['back'],
                    callback_data="back_product",
                )
            ]
        ]
    )
    return product_back_mk


def get_back_order(user_id):
    selected_language = get_selected_language(user_id)
    order_back_mk = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=messages[selected_language]['back'],
                    callback_data="back_order",
                )
            ]
        ]
    )
    return order_back_mk

