import os
import django

# Konfiguracja Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KCK.settings")
django.setup()

# Import modelu
from app.models import Car

def create_car(car_obj: dict) -> Car:
    new_car = Car(
        brand=car_obj["Marka"],
        model=car_obj["Model"],
        price=car_obj["price"],
        color=car_obj["Kolor"],
        engine_capacity=int(car_obj["Pojemność"].replace("cm3", "")),
        power=int(car_obj["Moc"].replace("KM", ""))
    )
    return new_car
