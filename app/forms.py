from django import forms
from app.models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'price', 'color', 'engine_capacity', 'power']
