from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from KCK.settings import TEMPLATES
from Scrapper import scrapper
from app.models import Car
from credit_scoring import predict
from .forms import CarForm  # Formularz, który stworzysz do obsługi dodawania samochodów
import Scrapper
from car_methods import create_car
def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'business':
            return redirect('business_dashboard')
        elif user_type == 'user':
            return redirect('user_dashboard')
    return render(request, 'login.html')

def business_dashboard(request):
    return render(request, 'business_dashboard.html')

def user_dashboard(request):
    return render(request, 'user_dashboard.html')


def scrap_cars_view(request):
    scraped_cars = []
    if request.method == 'POST' and 'scrap' in request.POST:
        try:
            # Wywołanie funkcji scrapującej
            scraped_cars = scrapper()  # Zakładam, że funkcja scrapper zwraca listę słowników z danymi
            request.session['scraped_cars'] = scraped_cars  # Przechowanie danych w sesji na czas dodawania
            messages.success(request, f"Znaleziono {len(scraped_cars)} samochodów.")
        except Exception as e:
            messages.error(request, f"Wystąpił błąd podczas scrapowania: {str(e)}")

    elif request.method == 'POST' and 'add_to_db' in request.POST:
        # Obsługa zapisu do bazy danych
        try:
            car_ids = request.POST.getlist('car_ids')  # Lista ID wybranych samochodów
            scraped_cars = request.session.get('scraped_cars', [])  # Pobranie zescrapowanych samochodów z sesji
            for car_id in car_ids:
                car_data = scraped_cars[int(car_id)]
                car=create_car(car_data)
                car.save()
            messages.success(request, f"Zapisano {len(car_ids)} samochodów do bazy danych.")
        except Exception as e:
            messages.error(request, f"Wystąpił błąd podczas zapisywania do bazy: {str(e)}")
        return redirect('business_dashboard')

    return render(request, 'app/scrap_cars.html', {'scraped_cars': scraped_cars})

def show_cars_view(request):
    cars = Car.objects.all()  # Pobranie wszystkich samochodów z bazy danych
    return render(request, 'app/show_cars.html', {'cars': cars})

def show_saved_cars(request):
    cars = Car.objects.all()
    return render(request, 'app/business_saved_cars.html', {'cars': cars})

def check_credit_scoring_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)  # Pobranie samochodu z bazy danych
    if request.method == 'POST':
        # Pobierz dane od użytkownika
        age = int(request.POST.get('age', 0))
        income = int(request.POST.get('income', 0))
        property_status = request.POST.get('property_status', 'OWN')
        years_employed = int(request.POST.get('years_employed', 0))
        past_due_loans = request.POST.get('past_due_loans', 'N')

        # Logika finansowania
        user_data = {
            "person_age": age,
            "person_income": income,
            "person_home_ownership": property_status,
            "person_emp_length": years_employed,
            "cb_person_default_on_file": past_due_loans,
            "loan_amnt": car.price,
        }

        # Symulacja wyniku (zastąp tym, co używasz w `predict`)
        is_eligible = predict(user_data)  # Zakładam, że masz funkcję `predict`

        # Komunikat wynikowy
        if is_eligible == 1:
            messages.success(request, f"Gratulacje! Możesz finansować samochód {car.brand} {car.model}.")
        else:
            messages.error(request, f"Niestety, nie spełniasz wymagań do finansowania tego samochodu.")
        print(is_eligible)
        return render(request, 'app/credit_result.html', {'car': car, 'result': is_eligible})

    return render(request, 'app/check_credit_scoring.html', {'car': car})