from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

from src.adapters.repos.event_repo import EventRepo
from src.domain.event import EventTypes
from src.domain.exceptions import DuplicateValueError
from src.adapters.repos.user_repo import UserRepo
from src.constants import months_translate, event_translate

load_dotenv()
TOKEN = getenv("TOKEN")
ID_MAIN_ADMIN = getenv("ID_MAIN_ADMIN")
bot = TeleBot(TOKEN)

file_path_to_data = Path(__file__).parent.parent / 'data'

event_repo = EventRepo(file_path=file_path_to_data / 'events.json')
events = event_repo.load()


@bot.message_handler(commands=['start'])
def start_command(message):
    start_message = (
        "<b>🌟 Приветствую вас в моём телеграм-боте, посвященном актуальным событиям в городе!\n\n"
        "📱 Ссылки на разработчика и проект:\n"
        "· GitHub: <a href='https://github.com/DjMix22'>DjMix22</a>\n"
        "· GitHub проекта: <i><u>Репозиторий закрыт</u> (находится на стадии разработки)</i>\n"
        "· Telegram: @DjMix22\n"
        "· Telegram канал с обновлениями: @events_in_focus\n\n"
        "📜Для получения помощи по командам и функционалу бота, воспользуйтесь командой /help.\n\n"
        "Наслаждайтесь актуальными событиями и новостями в городе с нашим телеграм-ботом!</b>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=start_message,
        parse_mode="HTML"
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    help_message = (
        "*🎉Напиши команду /events, если вы хотите узнать события на последующую неделю!\n"
        "🚀Напиши команду /admin, если вы хотите стать админом!*"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=help_message,
        parse_mode="Markdown"
    )


@bot.message_handler(commands=['events'])
def events_command(message):
    markup = InlineKeyboardMarkup()
    event_types = {
        "🎬 Фильмы": EventTypes.Movie,
        "🎤 Концерты": EventTypes.Concert,
        "🎫 Выступления": EventTypes.Performance
    }

    for event_type, event_type_obj in event_types.items():
        markup.add(InlineKeyboardButton(
            text=event_type,
            callback_data=event_type_obj
        ))

    bot.send_message(
        chat_id=message.chat.id,
        text="*📺 Выберите тип события:*",
        reply_markup=markup,
        parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data in (EventTypes.Movie, EventTypes.Concert, EventTypes.Performance))
def show_events(call: CallbackQuery):
    markup = InlineKeyboardMarkup()

    selected_events = [event for event in events if event.event_type == call.data]

    for event in selected_events:
        markup.add(InlineKeyboardButton(
            text=f"{event.name}",
            callback_data=f"event_{event.id}"
        ))

    bot.send_message(
        chat_id=call.message.chat.id,
        text=f"*{event_translate[call.data]} на последующую неделю:*",
        reply_markup=markup,
        parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: "event" in call.data)
def show_info_about_event(call: CallbackQuery):
    event_id = int(call.data.split('_')[1])

    current_event = next(event for event in events if event.id == event_id)

    time_slots = "\n".join(
        f"- {time_slot.start_date.strftime('%d')} {months_translate[time_slot.start_date.strftime('%B')]} {time_slot.start_date.strftime('%H:%M')}"
        for time_slot in current_event.time_slots
    )

    message = (
        f"*🌟 {current_event.name}\n\n"
        f"🎩 Жанр: {current_event.genre}\n"
        f"🌐 Ссылка на событие:* {current_event.url}*\n\n"
        f"🗓️ Возможное время на запись:\n"
        f"{time_slots}*"
    )

    bot.send_message(
        chat_id=call.message.chat.id,
        text=message,
        parse_mode="Markdown"
    )


@bot.message_handler(commands=['admin'])
def admin_command(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="✅",
        callback_data=f"yes {message.chat.id}"
    ))
    markup.add(InlineKeyboardButton(
        text="❌",
        callback_data=f"no {message.chat.id}"
    ))
    bot.send_message(
        chat_id=ID_MAIN_ADMIN,
        text=f"*Пользователь с ником {message.from_user.first_name}, id:* `{message.from_user.id}`* "
             f"хочет добавиться в админы.\nПринять его в админы:*",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.split()[0] in ("yes", "no"))
def add_to_admins(call: CallbackQuery):
    data = call.data.split()
    success, user_id = data[0], int(data[1])

    if success == "yes":
        try:
            user_repo = UserRepo(user_id, file_path_to_data / 'users.json')
            user_repo.save("admins")

            text_to_main_admin = f"*Вы успешно добавили в админы пользователя с id:* `{user_id}`*!*"
            text_to_user = "*Вы успешно добавились в список администрации!*"

        except DuplicateValueError:
            text_to_main_admin = f"*Пользователь с id:* `{user_id}` *уже является администратором!*"
            text_to_user = "*Вы уже находитесь в списке администрации!*"

    else:
        text_to_main_admin = f"*Вы не добавили в админы пользователя с id:* `{user_id}`*!*"
        text_to_user = "*Вас отказали в добавлении в список администрации!*"

    bot.send_message(
        chat_id=ID_MAIN_ADMIN,
        text=text_to_main_admin,
        parse_mode="Markdown"
    )
    bot.send_message(
        chat_id=user_id,
        text=text_to_user,
        parse_mode="Markdown"
    )


if __name__ == "__main__":
    bot.polling()
