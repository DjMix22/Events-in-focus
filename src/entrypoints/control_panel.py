import customtkinter
import threading
from customtkinter import CTk

from src.entrypoints.telegram_bot import TelegramBot
from src.entrypoints.parsing import update_database

is_bot_running = False


def run_bot(telegram_bot: TelegramBot) -> None:
    global is_bot_running
    if not is_bot_running:
        bot_thread = threading.Thread(target=telegram_bot.run_bot)
        bot_thread.start()
        is_bot_running = not is_bot_running


def stop_bot(telegram_bot: TelegramBot) -> None:
    global is_bot_running
    is_bot_running = False
    telegram_bot.stop_bot()


class ControlPanel:
    def __init__(self, window: CTk, telegram_bot: TelegramBot):
        self.window = window
        self.telegram_bot = telegram_bot
        self.setup_ui()

    def setup_ui(self) -> None:
        self.window.title("Панель управления")
        self.window.geometry("400x300")
        customtkinter.set_appearance_mode("dark")

        buttons = [
            {"text": "Запустить телеграмм-бота", "command": lambda: run_bot(self.telegram_bot)},
            {"text": "Выключить телеграмм-бота", "command": lambda: stop_bot(self.telegram_bot)},
            {"text": "Обновить базу данных", "command": update_database},
        ]

        for i, button_config in enumerate(buttons):
            button = customtkinter.CTkButton(
                self.window,
                text=button_config["text"],
                command=button_config["command"],
                height=50,
                width=300,
                font=('Arial', 15),
                fg_color='#0267bf',
                hover_color='#1d85e0'
            )
            button.grid(row=i, column=0, padx=10, pady=5)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
