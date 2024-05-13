import customtkinter
import threading
from src.entrypoints.telegram_bot import run_bot, stop_bot
from src.entrypoints.parsing import update_database


def run_telegram_bot():
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()


window = customtkinter.CTk()
window.title("Панель управления")

window.geometry("400x300")

customtkinter.set_appearance_mode("dark")

telegram_bot_button = customtkinter.CTkButton(window, text="Запустить телеграмм-бота", command=run_telegram_bot,
                                              height=50, width=300, font=('Comic Sans MS', 15), fg_color='#0267bf',
                                              hover_color='#1d85e0')
telegram_bot_button.grid(row=0, column=0, padx=10, pady=5)

telegram_bot_stop_button = customtkinter.CTkButton(window, text="Выключить телеграмм-бота", command=stop_bot,
                                                   height=50, width=300, font=('Arial', 15), fg_color='#0267bf',
                                                   hover_color='#1d85e0')
telegram_bot_stop_button.grid(row=1, column=0, padx=10, pady=5)

update_database_button = customtkinter.CTkButton(window, text="Обновить базу данных", command=update_database,
                                                 height=50, width=300, font=('Arial', 15), fg_color='#0267bf',
                                                 hover_color='#1d85e0')
update_database_button.grid(row=2, column=0, padx=10, pady=5)

window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(0, weight=1)

window.mainloop()
