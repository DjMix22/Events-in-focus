import customtkinter
from dotenv import load_dotenv
from os import getenv

from src.entrypoints.telegram_bot import TelegramBot
from src.entrypoints.control_panel import ControlPanel


try:
    load_dotenv()
    TOKEN = getenv("TOKEN")
    telegram_bot = TelegramBot(TOKEN)
    window = customtkinter.CTk()
    control_panel = ControlPanel(window, telegram_bot)
    window.mainloop()
except KeyboardInterrupt:
    print("Панель управления закрыта!")
