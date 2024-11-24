import os
from contextlib import nullcontext

import django
from prompt_toolkit.shortcuts import message_dialog, input_dialog, button_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog


from Scrapper import scrapper
from car_methods import create_car
from console_options import CarManager
from user_options import show_available_cars, check_credit_scoring

# Ustawienie środowiska Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KCK.settings")
django.setup()

from app.models import Car


style = Style.from_dict({
    "dialog": "bg:#202020 #ffffff",  # Kolor tła dialogu i tekstu
    "button.focused": "bg:#ff0000 #ffffff",
    # Styl aktywnego przycisku
})


def login():
    wybor = radiolist_dialog(
        title="Logowanie",
        text="Wybierz sposób logowania:",
        values=[
            ("user", "Przeglądaj dostępne samochody"),
            ("business", "Zaloguj się jako klient biznesowy"),
        ],
        style=style
    ).run()

    if wybor == 'business':
        business_logic()
    elif wybor == 'user':
        user_logic()

    else:
        exit()


def business_logic():
    BusinessOpt = CarManager()
    wybor = None
    while wybor != "4":
        wybor = radiolist_dialog(
            title="MENU",
            text="Wybierz opcję poniżej:",
            values=[
                ("1", "Scrapuj samochody"),
                ("2", "Dodaj samochód do bazy"),
                ("3", "Wyświetl samochody z bazy"),
                ("4", "Powrót"),
            ],
            style=style
        ).run()

        if wybor == "1":
            BusinessOpt.run_car_scrapper()
        elif wybor == "2":
            BusinessOpt.add_cars_to_database()
        elif wybor == "3":
            BusinessOpt.show_cars_from_db()

        else:
            login()


def user_logic():

    wybor = radiolist_dialog(
        title="MENU",
        text="Wybierz opcję poniżej:",
        values=[
                ("1", "Przeglądaj"),
                ("2", "Sprawdź możliwość finansowania"),
                ("3", "Powrót"),
            ],
            style=style
        ).run()

    if wybor == "1":
        show_available_cars(previous_window=user_logic)
    elif wybor == "2":
        check_credit_scoring()
    else:
        login()


# Uruchomienie aplikacji
if __name__ == "__main__":
    login()