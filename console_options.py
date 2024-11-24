from prompt_toolkit.shortcuts import message_dialog, input_dialog
from Scrapper import scrapper
from app.models import Car
from car_methods import create_car

class CarManager:
    def __init__(self):
        self.cars = []  # Lista przechowująca samochody pobrane przez scraper

    def run_car_scrapper(self):
        """Uruchamia scraper samochodów i zapisuje wyniki w obiekcie."""
        message_dialog(
            title="Scraper został uruchomiony",
            text="Zaraz będziesz mógł sprawdzić najnowsze samochody."
        ).run()
        self.cars = scrapper()
        message_dialog(
            title="Scrapper",
            text=f"Znaleziono {len(self.cars)} samochodów."
        ).run()

    def add_cars_to_database(self):
        """Dodaje wybrany samochód z listy scraperów do bazy danych."""
        if not self.cars:
            message_dialog(
                title="Błąd",
                text="Najpierw musisz scrapować samochody!"
            ).run()
            return

        options = "\n".join(
            [f"{i+1}. {car['Marka']} {car['Model']} - {car['price']}" for i, car in enumerate(self.cars)]
        )
        index_input = input_dialog(
            title="Dodaj samochód",
            text=f"Podaj numer samochodu do zapisania:\n\n{options}"
        ).run()

        if not index_input or not index_input.isdigit():
            message_dialog(
                title="Błąd",
                text="Nieprawidłowy numer."
            ).run()
            return

        index = int(index_input)
        if index < 1 or index > len(self.cars):
            message_dialog(
                title="Błąd",
                text="Nieprawidłowy numer."
            ).run()
            return

        car_obj = self.cars[index - 1]
        new_car = create_car(car_obj)  # Użycie funkcji create_car
        new_car.save()  # Zapisanie obiektu w bazie danych
        message_dialog(
            title="Sukces",
            text="Rekord dodany!"
        ).run()

    def show_cars_from_db(self):
        """Wyświetla samochody zapisane w bazie danych."""
        my_cars = Car.objects.all()
        if not my_cars:
            message_dialog(
                title="Samochody w bazie",
                text="Brak samochodów w bazie danych."
            ).run()
            return

        cars_text = "\n".join(
            [f"{car.id}. {car.brand} {car.model}, Cena: {car.price}, Kolor: {car.color}" for car in my_cars]
        )
        message_dialog(
            title="Samochody w bazie",
            text=cars_text
        ).run()
