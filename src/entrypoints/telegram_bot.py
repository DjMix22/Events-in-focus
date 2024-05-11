from telebot import TeleBot
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv("TOKEN")
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    start_message = (
        '<b>🌟 Приветствую вас в моём телеграм-боте, посвященном актуальным событиям в городе!\n\n'
        '📱 Ссылки на разработчика и проект:\n'
        '· GitHub: <a href=\'https://github.com/DjMix22\'>DjMix22</a>\n'
        '· GitHub проекта: <i><u>Репозиторий закрыт</u> (находится на стадии разработки)</i>\n'
        '· Telegram: @DjMix22\n'
        '· Telegram канал с обновлениями: @events_in_focus\n\n'
        '📜Для получения помощи по командам и функционалу бота, воспользуйтесь командой /help.\n\n'
        'Наслаждайтесь актуальными событиями и новостями в городе с нашим телеграм-ботом!</b>'
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=start_message,
        parse_mode="HTML"
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    help_message = (
        "<b>🎉Напиши команду /events, если вы хотите узнать события!\n"
        "🚀Напиши команду /admin, если вы хотите стать админом!</b>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=help_message,
        parse_mode="HTML"
    )


@bot.message_handler(commands=['event'])
def events_command(message):
    ...


@bot.message_handler(commands=['admin'])
def admin_command(message):
    ...


if __name__ == "__main__":
    bot.polling()

