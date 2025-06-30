from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dp import get_all_products, get_product_by_id, add_menu
from states import OrderState
from utils import save_order_to_json, load_orders_from_json
from keyboards import create_inline_menu
import os, ast
from utils import clear_user_orders

from dotenv import load_dotenv

load_dotenv()
ADMIN_IDs = os.getenv("ADMIN_ID").split(",") 
ADMIN_IDs = [int(i) for i in ADMIN_IDs]       


router = Router()

# /start komandasi
@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    if not message.from_user.id in ADMIN_IDs:
        return await message.answer("⛔ Siz bu botdan foydalana olmaysiz.")
    await message.answer("🍔 Mahsulotni tanlang:", reply_markup=create_inline_menu())
    await state.set_state(OrderState.choosing)

# Mahsulot tanlash (inline tugma)
@router.callback_query(F.data.startswith("select_"))
async def handle_product_select(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user.id in ADMIN_IDs:
        return await callback.answer("⛔ Ruxsat yo‘q.", show_alert=True)

    await callback.message.delete()  # 🔸 Tugmali xabarni o‘chirish

    prod_id = int(callback.data.split("_")[1])
    await state.update_data(selected_product_id=prod_id)

    name, _ = get_product_by_id(prod_id)
    await callback.message.answer(f"{name} nechta sotdingiz?")
    await state.set_state(OrderState.entering_quantity)
    await callback.answer()

# Miqdorni kiritish
@router.message(OrderState.entering_quantity)
async def enter_quantity(message: Message, state: FSMContext):
    if not message.from_user.id in ADMIN_IDs:
        return await message.answer("⛔ Ruxsat yo‘q.")

    if not message.text.isdigit():
        return await message.answer("Iltimos, son kiriting.")

    user_id = message.from_user.id
    count = int(message.text)
    data = await state.get_data()
    prod_id = data.get("selected_product_id")

    save_order_to_json(user_id, prod_id, count)  # 🔸 JSON ga yozish
    await message.answer("✅ Qabul qilindi!", reply_markup=create_inline_menu())
    await state.set_state(OrderState.choosing)

# 🧾 Jami buyurtma
# @router.callback_query(F.data == 'show_total')
# async def show_total_callback(callback: CallbackQuery):
#     await callback.message.delete()  # 🔸 Tugmali xabarni o‘chirish

#     user_id = callback.from_user.id
#     orders = load_orders_from_json(user_id)

#     if not orders:
#         await callback.message.answer("🛒 Hech narsa tanlanmagan.")
#     else:
#         total_text = "🧾 Buyurtma:\n\n"
#         total_price = 0

#         for prod_id_str, quantity in orders.items():
#             prod_id = int(prod_id_str)
#             name, price = get_product_by_id(prod_id)
#             summa = price * quantity
#             total_text += f"{name} — {quantity} ta = {summa:,} so‘m\n"
#             total_price += summa

#         total_text += f"\n💰 Umumiy: {total_price:,} so‘m"
#         await callback.message.answer(total_text)

#     await callback.answer()
@router.callback_query(F.data == 'show_total')
async def show_total_callback(callback: CallbackQuery):
    await callback.message.delete()  # 🔸 Tugmali xabarni o‘chirish

    user_id = callback.from_user.id
    orders = load_orders_from_json(user_id)

    if not orders:
        await callback.message.answer("🛒 Hech narsa tanlanmagan.")
    else:
        total_text = "🧾 Buyurtma:\n\n"
        total_price = 0

        for prod_id_str, quantity in orders.items():
            prod_id = int(prod_id_str)
            name, price = get_product_by_id(prod_id)
            summa = price * quantity
            total_text += f"{name} — {quantity} ta = {summa:,} so‘m\n"
            total_price += summa

        total_text += f"\n💰 Umumiy: {total_price:,} so‘m"
        await callback.message.answer(total_text)

        # 🔸 Buyurtmalar ko‘rsatilib bo‘lgach, foydalanuvchining ordersini tozalaymiz
        clear_user_orders(user_id)

    await callback.answer()


# ➕ Yangi menu qo‘shish
@router.callback_query(F.data == "add_menu")
async def add_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()  # 🔸 Tugmali xabarni o‘chirish
    await callback.message.answer("📝 Yangi menu nomini kiriting:")
    await state.set_state(OrderState.adding_name)
    await callback.answer()

# ➕ Menu nomi kiritish
@router.message(OrderState.adding_name)
async def add_menu_name(message: Message, state: FSMContext):
    await state.update_data(new_menu_name=message.text.strip())
    await message.answer("💰 Narxini kiriting:")
    await state.set_state(OrderState.adding_price)

# ➕ Menu narxi kiritish
@router.message(OrderState.adding_price)
async def add_menu_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Iltimos, narxni raqamda kiriting.")

    data = await state.get_data()
    name = data.get("new_menu_name")
    price = int(message.text.strip())

    result = add_menu(name, price)
    await message.answer(result, reply_markup=create_inline_menu())
    await state.set_state(OrderState.choosing)
