from django.urls import path, include
from .views import TransactionView

# app_name = 'lannisterapi'
urlpatterns = [
    path('', TransactionView.as_view(),)
]
