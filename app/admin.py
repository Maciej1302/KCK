from django.contrib import admin

# Register your models here.
from . models import Car

class CarAdmin(admin.ModelAdmin):
    model = Car
    fields = ["brand","model","price"]
admin.site.register(Car,CarAdmin)