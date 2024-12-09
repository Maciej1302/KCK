from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('business/', views.business_dashboard, name='business_dashboard'),
    path('user/', views.login_view, name='login_view'),
    path('view-cars/', views.show_cars_view, name='show_cars'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
     path('scrap-cars/', views.scrap_cars_view, name='scrap_cars'),
    path('business-saved-cars/', views.show_saved_cars, name='business_saved_cars'),
     path('check-credit-scoring/<int:car_id>/', views.check_credit_scoring_view, name='check_credit_scoring'),
]
