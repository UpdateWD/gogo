import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

from db import create_database

logging.basicConfig(level=logging.INFO)

TOKEN = '5970380166:AAED9eB8ltits8vKEeBX83-EfOoFJrqGf9c'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def is_user_subscribed(channel: str, user_id: int) -> bool:
    try:
        status = await bot.get_chat_member(channel, user_id)
        if status.status in ('member', 'administrator', 'creator'):
            return True
    except:
        pass
    return False


def show_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton("✨ Доступ", callback_data='button1')
    button2 = InlineKeyboardButton("👤 Профиль", callback_data='button2')
    button3 = InlineKeyboardButton("🚀 Помощь", callback_data='button3')
    markup.add(button1, button2, button3)
    return markup


def show_profile_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton("🔧 Настройки", callback_data='profile_button1')
    button2 = InlineKeyboardButton("📊 Статистика", callback_data='profile_button2')
    markup.add(button1, button2)
    markup.add(InlineKeyboardButton("🔙", callback_data='back'))
    return markup


def show_back_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton("🔙", callback_data='back')
    markup.add(back_button)
    return markup


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    channel = "gogoik1"
    is_subscribed = await is_user_subscribed(channel, user_id)

    if is_subscribed:
        welcome_text = f'<b>Добро пожаловать <a href="tg://user?id={user_id}">{user_name}</a>.</b>'
        photo = open('image.jpg', 'rb')
        await bot.send_photo(message.chat.id, photo, caption=welcome_text, reply_markup=show_buttons(), parse_mode='html')
    else:
        welcome_text = f'<b>Добро пожаловать <a href="tg://user?id={user_id}">{user_name}</a>.</b>\nПодпишитесь на {channel} и нажмите "Проверить":'
        markup = InlineKeyboardMarkup()
        subscribe_button = InlineKeyboardButton("Подпишитесь на канал", url=f"https://t.me/{channel}")
        check_subscription_button = InlineKeyboardButton("Проверить", callback_data='check_subscription')
        markup.add(subscribe_button)
        markup.add(check_subscription_button)
        await bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='html')


@dp.callback_query_handler(lambda call: True)
async def callback_inline(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    welcome_text = f'<b>Добро пожаловать <a href="tg://user?id={user_id}">{user_name}</a>.</b>'
    channel = "@gogoik1"

    if await is_user_subscribed(channel, user_id):
        if call.data == 'button1':
            photo = open('image.jpg', 'rb')
            await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(photo, caption=f'<b>Вы выбрали кнопку 1</b>', parse_mode='html'), reply_markup=show_back_button())
        elif call.data == 'button2':
            photo = open('image.jpg', 'rb')
            await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(photo, caption=f'<b>Профиль <a href="tg://user?id={user_id}">{user_name}</a></b> \n\n<b>Ключ:</b><code>ss://Y2hhY2hhMjAtaWV0ЗhiR2Fm@95.164.9.246:12919#KROTvpn</code>\n\n<b>Осталось: 12 дней</b>\n<b>Срок работы: 18.09.2023 20:19:22</b>', parse_mode='html'), reply_markup=show_profile_buttons())
        elif call.data == 'button3':
            photo = open('image.jpg', 'rb')
            await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(photo, caption='Вы выбрали кнопку 3', parse_mode='html'), reply_markup=show_back_button())
        elif call.data == 'profile_button1':
            await bot.answer_callback_query(call.id, "Вы выбрали Настройки")
        elif call.data == 'profile_button2':
            await bot.answer_callback_query(call.id, "Вы выбрали Статистика")
        elif call.data == 'check_subscription':
            if await is_user_subscribed(channel, user_id):
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                # Отправляем основное меню после успешной проверки подписки
                photo = open('image.jpg', 'rb')
                await bot.send_photo(call.message.chat.id, photo, caption=welcome_text, reply_markup=show_buttons(), parse_mode='html')
            else:
                await bot.answer_callback_query(call.id, f"Вы не подписаны на {channel}.")
        elif call.data == 'back':
            photo = open('image.jpg', 'rb')
            await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(photo, caption=welcome_text, parse_mode='html'), reply_markup=show_buttons())
    else:
        await bot.answer_callback_query(call.id, f"Вы не подписаны на {channel}.")

if __name__ == '__main__':
    create_database()
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
