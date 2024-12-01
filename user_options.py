from prompt_toolkit.shortcuts import radiolist_dialog, message_dialog, input_dialog

from app.models import Car
from console_options import CarManager
from credit_scoring import predict


def show_available_cars(previous_window):
    """Wyświetla dostępne samochody z możliwością wyboru szczegółów."""
    my_cars = Car.objects.all()
    if not my_cars:
        message_dialog(
            title="Samochody w bazie",
            text="Brak dostępnych samochodów w bazie."
        ).run()
        previous_window()  # Powrót do poprzedniego okna
        return



    # Tworzenie listy opcji dla radiolist_dialog
    car_choices = [(str(car.id), f"{car.brand} {car.model}, Cena: {car.price}") for car in my_cars]


    # Wyświetlenie dialogu wyboru samochodu
    selected_car_id = radiolist_dialog(
        title="Dostępne samochody",
        text="Wybierz samochód, aby zobaczyć szczegóły:",
        values=car_choices
    ).run()

    if not selected_car_id:
        # Powrót do poprzedniego menu
        previous_window()
        return



    # Pobranie wybranego samochodu z bazy
    selected_car = Car.objects.get(id=int(selected_car_id))
    car_details = (
        f"ID: {selected_car.id}\n"
        f"Marka: {selected_car.brand}\n"
        f"Model: {selected_car.model}\n"
        f"Cena: {selected_car.price} PLN\n"
        f"Kolor: {selected_car.color}\n"
        f"Pojemność silnika: {selected_car.engine_capacity} cm3\n"
        f"Moc: {selected_car.power} KM\n"
    )

    # Wyświetlenie szczegółów wybranego samochodu
    message_dialog(
        title=f"Szczegóły samochodu: {selected_car.brand} {selected_car.model}",
        text=car_details
    ).run()

    show_available_cars(previous_window)

def select_car():
    """Pozwala użytkownikowi wybrać samochód z bazy."""
    my_cars = Car.objects.all()
    if not my_cars:
        message_dialog(
            title="Brak samochodów",
            text="W bazie danych nie ma samochodów do sprawdzenia finansowania."
        ).run()
        return "back"

    car_choices = [(str(car.id), f"{car.brand} {car.model}, Cena: {car.price}") for car in my_cars]
    selected_car_id = radiolist_dialog(
        title="Dostępne samochody",
        text="Wybierz samochód, aby sprawdzić możliwość finansowania",
        values=car_choices
    ).run()

    if selected_car_id is None:  # Kliknięcie Cancel
        return "back"

    return Car.objects.get(id=int(selected_car_id))


def get_input(title, text, validation_func=None):
    """Uniwersalne okno do wprowadzania danych z obsługą anulowania."""
    while True:
        value = input_dialog(
            title=title,
            text=text
        ).run()

        if value is None:  # Obsługa cofania
            return "back"

        if validation_func and not validation_func(value):
            message_dialog(
                title="Błąd",
                text="Wprowadzone dane są nieprawidłowe. Spróbuj ponownie."
            ).run()
            continue

        return value


def get_user_age():
    """Pobiera wiek użytkownika z walidacją."""
    return get_input(
        title="Podaj wiek",
        text="Wprowadź swój wiek:",
        validation_func=lambda x: x.isdigit() and int(x) >= 18
    )


def get_annual_income():
    """Pobiera roczny przychód użytkownika z walidacją."""
    return get_input(
        title="Roczny przychód",
        text="Podaj swój roczny przychód (w PLN):",
        validation_func=lambda x: x.isdigit() and int(x) > 0
    )


def get_property_status():
    """Pozwala użytkownikowi wybrać status nieruchomości."""
    property_status = radiolist_dialog(
        title="Status nieruchomości",
        text="Wybierz swój status nieruchomości:",
        values=[
            ("RENT", "Wynajem"),
            ("OWN", "Posiadam"),
            ("MORTGAGE", "Hipoteka"),
            ("OTHER", "Inny")
        ]
    ).run()

    return property_status if property_status is not None else "back"


def get_years_employed(age):
    """Pobiera ilość lat pracy użytkownika z walidacją."""
    return get_input(
        title="Ilość lat pracy",
        text="Podaj ilość lat pracy:",
        validation_func=lambda x: x.isdigit() and 0 <= int(x) <= age
    )


def get_past_due_loans():
    """Pozwala użytkownikowi określić historię spłat pożyczek."""
    past_due_loans = radiolist_dialog(
        title="Historia spłat pożyczek",
        text="Czy kiedykolwiek miałeś opóźnienia w spłacie pożyczki?",
        values=[
            ("Y", "Tak"),
            ("N", "Nie")
        ]
    ).run()

    return past_due_loans if past_due_loans is not None else "back"


def show_summary(user_data, selected_car):
    """Wyświetla podsumowanie danych i pozwala na ich edycję."""
    while True:
        summary = (
            f"Samochód: {selected_car.brand} {selected_car.model}, Cena: {selected_car.price}\n"
            f"Wiek: {user_data['person_age']}\n"
            f"Roczny przychód: {user_data['person_income']} PLN\n"
            f"Status nieruchomości: {user_data['person_home_ownership']}\n"
            f"Ilość lat pracy: {user_data['person_emp_length']}\n"
            f"Historia spłat pożyczek: {'Tak' if user_data['cb_person_default_on_file'] == 'yes' else 'Nie'}\n"
        )
        action = radiolist_dialog(
            title="Podsumowanie Twoich danych",
            text=f"{summary}\n\nWybierz opcję:",
            values=[
                ("edit", "Edytuj dane"),
                ("confirm", "Zatwierdź i sprawdź zdolność finansowania"),
            ]
        ).run()

        user_data['loan_amnt'] = selected_car.price

        if action == "edit":
            field_to_edit = radiolist_dialog(
                title="Edycja danych",
                text="Wybierz, które dane chcesz edytować:",
                values=[
                    ("age", "Wiek"),
                    ("annual_income", "Roczny przychód"),
                    ("property_status", "Status nieruchomości"),
                    ("years_employed", "Ilość lat pracy"),
                    ("past_due_loans", "Historia spłat pożyczek")
                ]
            ).run()

            if field_to_edit == "age":
                age = get_user_age()
                if age == "back":
                    continue
                user_data["person_age"] = int(age)

            elif field_to_edit == "annual_income":
                income = get_annual_income()
                if income == "back":
                    continue
                user_data["person_income"] = int(income)

            elif field_to_edit == "property_status":
                property_status = get_property_status()
                if property_status == "back":
                    continue
                user_data["person_home_ownership"] = property_status

            elif field_to_edit == "years_employed":
                years_employed = get_years_employed(user_data["person_age"])
                if years_employed == "back":
                    continue
                user_data["person_emp_length"] = int(years_employed)

            elif field_to_edit == "past_due_loans":
                past_due_loans = get_past_due_loans()
                if past_due_loans == "back":
                    continue
                user_data["cb_person_default_on_file"] = past_due_loans

        elif action == "confirm":
            message_dialog(
                title="Zatwierdzenie danych",
                text="Poczekaj, trwa ocena Twojej zdolności kredytowej..."
            ).run()
            pred = predict(user_data)
            print(pred)

            show_credit_decision(pred, selected_car)
            break

def show_credit_decision(pred, selected_car):
    """
    Wyświetla wynik oceny zdolności kredytowej na podstawie predykcji.
    """

    from menu import user_logic

     # Drugi element to prawdopodobieństwo akceptacji
    decision_text = (
        "Gratulacje! Masz wysokie szanse na uzyskanie finansowania!" if pred == 1
        else "Niestety, na podstawie wprowadzonych danych, Twoja zdolność kredytowa jest zbyt niska."
    )

    message_dialog(
        title="Wynik oceny zdolności kredytowej",
        text=(
            f"Wynik analizy zdolności kredytowej dla samochodu {selected_car.brand} {selected_car.model}:\n\n"
            f"{decision_text}"
        )
    ).run()

    user_logic()

def check_credit_scoring():
    """Główna logika sprawdzania zdolności kredytowej."""
    while True:
        selected_car = select_car()
        if selected_car == "back":
            return

        user_data = {}

        # Pobieranie danych krok po kroku
        age = get_user_age()
        if age == "back":
            continue
        user_data["person_age"] = int(age)

        income = get_annual_income()
        if income == "back":
            continue
        user_data["person_income"] = int(income)

        property_status = get_property_status()
        if property_status == "back":
            continue
        user_data["person_home_ownership"] = property_status

        years_employed = get_years_employed(user_data["person_age"])
        if years_employed == "back":
            continue
        user_data["person_emp_length"] = int(years_employed)

        past_due_loans = get_past_due_loans()
        if past_due_loans == "back":
            continue
        user_data["cb_person_default_on_file"] = past_due_loans

        # Wyświetlenie podsumowania i edycji
        show_summary(user_data, selected_car)
        break