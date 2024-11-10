import os
from contextlib import nullcontext

import django

from Scrapper import scrapper

# Ustawienie środowiska Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KCK.settings")
django.setup()

from app.models import Car

cars =[]

def wyswietl_menu():
    print("\n=== MENU ===")
    print("1. Scrapuj samochody i je wyświetl")
    print("2. Dodaj samochód do swojej bazy danych")
    print("3. Wyświetl samochody ze swojej bazy danych")
    print("4. Wyjście")

def run_car_scrapper():
    global cars
    cars=scrapper()

def add_cars_to_database():
    index = int(input("Podaj nr samochodu który chcesz zapisac w swojej bazie danych: "))
    car_obj = cars[index-1]
    new_car = Car(brand=car_obj["Marka"],model=car_obj["Model"],price=car_obj["price"],color=car_obj["Kolor"],engine_capacity=int(car_obj["Pojemność"].replace("cm3","")),power=int(car_obj["Moc"].replace("KM","")))
    new_car.save()
    print("Rekord dodany!")

def show_cars_from_db():
    my_cars=Car.objects.all()
    print(my_cars)

def main():
    while True:
        wyswietl_menu()
        wybor = input("Wybierz opcję: ")

        if wybor == '1':
            run_car_scrapper()
        elif wybor == '2':
            add_cars_to_database()
        elif wybor == '3':
            show_cars_from_db()
        elif wybor == '4':
            print("Do widzenia!")
            break
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")

if __name__ == "__main__":
    main()
