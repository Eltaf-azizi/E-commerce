from django.urls import path
from .views import (
    ItemDetailView,
    checkout,
    HomeView,
    add_to_cart
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>/', ItemDetailView, name='product'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart')
]