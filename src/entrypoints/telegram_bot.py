from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

from src.adapters.repos.event_repo import EventRepo
from src.domain.event import EventTypes
from src.domain.errors import DuplicateValueError
from src.adapters.repos.user_repo import UserRepo
from src.constants import months_translate, event_translate

load_dotenv()
ID_MAIN_ADMIN = getenv("ID_MAIN_ADMIN")

file_path_to_data = Path(__file__).parent.parent.parent / 'data'


class TelegramBot:
    def __init__(self, TOKEN: str):
        self.bot = TeleBot(TOKEN)
        self.event_repo = EventRepo(file_path=file_path_to_data / 'events.json')
        self.events = self.event_repo.load()
        self.setup_handlers()

    def setup_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start_command)
        self.bot.message_handler(commands=['help'])(self.help_command)
        self.bot.message_handler(commands=['events'])(self.events_command)
        self.bot.callback_query_handler(
            func=lambda call: call.data in (EventTypes.Movie, EventTypes.Concert, EventTypes.Performance))(
            self.show_events)
        self.bot.callback_query_handler(func=lambda call: "event" in call.data)(self.show_info_about_event)
        self.bot.message_handler(commands=['admin'])(self.admin_command)
        self.bot.callback_query_handler(func=lambda call: call.data.split()[0] in ("yes", "no"))(self.add_to_admins)

    def check_user_in_list(self, user_id: int, chat_id: int, list_save: str) -> bool:
        user_repo = UserRepo(user_id, file_path_to_data / 'users.json')
        if user_repo.id_in_db(list_save):
            self.bot.send_message(
                chat_id=chat_id,
                text="*🚫 Вы в бан листе!*",
                parse_mode="Markdown"
            )
            return True

    def start_command(self, message: Message):
        if self.check_user_in_list(message.from_user.id, message.chat.id, "bans"):
            return None
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
        self.bot.send_message(
            chat_id=message.chat.id,
            text=start_message,
            parse_mode="HTML"
        )

    def help_command(self, message: Message):
        if self.check_user_in_list(message.from_user.id, message.chat.id, "bans"):
            return None
        help_message = (
            "*🎉Напиши команду /events, если вы хотите узнать события на последующую неделю!\n"
            "🚀Напиши команду /admin, если вы хотите стать админом!*"
        )
        self.bot.send_message(
            chat_id=message.chat.id,
            text=help_message,
            parse_mode="Markdown"
        )

    def events_command(self, message: Message):
        if self.check_user_in_list(message.from_user.id, message.chat.id, "bans"):
            return None
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

        self.bot.send_message(
            chat_id=message.chat.id,
            text="*📺 Выберите тип события:*",
            reply_markup=markup,
            parse_mode="Markdown"
        )

    def show_events(self, call: CallbackQuery):
        markup = InlineKeyboardMarkup()

        selected_events = [event for event in self.events if event.event_type == call.data]

        for event in selected_events:
            markup.add(InlineKeyboardButton(
                text=f"{event.name}",
                callback_data=f"event_{event.id}"
            ))

        self.bot.send_message(
            chat_id=call.message.chat.id,
            text=f"*{event_translate[call.data]} на последующую неделю:*",
            reply_markup=markup,
            parse_mode="Markdown"
        )

    def show_info_about_event(self, call: CallbackQuery):
        event_id = int(call.data.split('_')[1])

        current_event = next(event for event in self.events if event.id == event_id)

        time_slots = "\n".join(
            f"- 🕰️ {time_slot.start_date.strftime('%d')} {months_translate[time_slot.start_date.strftime('%B')]} "
            f"{time_slot.start_date.strftime('%H:%M')}, цена: {time_slot.price}, место: {time_slot.place}"
            for time_slot in current_event.time_slots
        )

        message = (
            f"*🌟 {current_event.name}\n\n"
            f"🎩 Жанр: {current_event.genre}\n"
            f"🌐 Ссылка на событие:* {current_event.url}*\n\n"
            f"🗓️ Возможное время на запись:\n"
            f"{time_slots}*"
        )

        self.bot.send_message(
            chat_id=call.message.chat.id,
            text=message,
            parse_mode="Markdown"
        )

    def admin_command(self, message: Message):
        if self.check_user_in_list(message.from_user.id, message.chat.id, "bans"):
            return None
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(
            text="✅",
            callback_data=f"yes {message.chat.id}"
        ))
        markup.add(InlineKeyboardButton(
            text="❌",
            callback_data=f"no {message.chat.id}"
        ))
        self.bot.send_message(
            chat_id=ID_MAIN_ADMIN,
            text=f"*Пользователь с ником {message.from_user.first_name}, id:* `{message.from_user.id}`* "
                 f"хочет добавиться в админы.\nПринять его в админы:*",
            parse_mode="Markdown",
            reply_markup=markup
        )

    def add_to_admins(self, call: CallbackQuery):
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

        self.bot.send_message(
            chat_id=ID_MAIN_ADMIN,
            text=text_to_main_admin,
            parse_mode="Markdown"
        )
        self.bot.send_message(
            chat_id=user_id,
            text=text_to_user,
            parse_mode="Markdown"
        )

    def run_bot(self):
        self.bot.polling()

    def stop_bot(self):
        self.bot.stop_polling()
