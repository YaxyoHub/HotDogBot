# # hotdog/keyboards.py

# from dp import get_all_products
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# def create_inline_menu():
#     products = get_all_products()
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text=name, callback_data=f"select_{pid}")]
#             for pid, name, _ in products
#         ] + [
#             [InlineKeyboardButton(text="🧾 Jami", callback_data="show_total")],
#             [InlineKeyboardButton(text="➕ Menu qo'shish", callback_data="add_menu")]
#         ]
#     )
#     return keyboard
from dp import get_all_products
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_inline_menu():
    products = get_all_products()
    
    # Tugmalarni 2 ustunli qatorlarga ajratamiz
    product_buttons = []
    row = []
    for i, (pid, name, _) in enumerate(products, start=1):
        row.append(InlineKeyboardButton(text=name, callback_data=f"select_{pid}"))
        if i % 2 == 0:
            product_buttons.append(row)
            row = []
    if row:  # Agar oxirida bitta tugma qolsa
        product_buttons.append(row)

    # Pastki tugmalarni qo‘shamiz
    product_buttons.append([InlineKeyboardButton(text="🧾 Jami", callback_data="show_total")])
    product_buttons.append([InlineKeyboardButton(text="➕ Menu qo'shish", callback_data="add_menu")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=product_buttons)
    return keyboard
