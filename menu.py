import os
from contextlib import nullcontext

import django
from prompt_toolkit.shortcuts import message_dialog, input_dialog, button_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog


from Scrapper import scrapper
from car_methods import create_car
from console_options import run_car_scrapper, add_cars_to_database, show_cars_from_db

# Ustawienie środowiska Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KCK.settings")
django.setup()

from app.models import Car


style = Style.from_dict({
    "dialog": "bg:#202020 #ffffff",  # Kolor tła dialogu i tekstu
    "button.focused": "bg:#ff0000 #ffffff",  # Styl aktywnego przycisku
})


# Główna logika
wybor = None
while wybor != "4":
    wybor = button_dialog(
        title="MENU",
        text="Wybierz opcję poniżej:\n(Użyj klawiszy strzałek):",
        buttons=[
            ("Scrapuj samochody", "1"),
            ("Dodaj samochód do bazy", "2"),
            ("Wyświetl samochody z bazy", "3"),
            ("Wyjście", "4"),
        ],
        style=style
    ).run()

    if wybor == "1":
        run_car_scrapper()
    elif wybor == "2":
        add_cars_to_database()
    elif wybor == "3":
        show_cars_from_db()

message_dialog(
    title="Koniec",
    text="Do widzenia!"
).run()