from django.urls import path
from . import views

urlpatterns = [
    #base url just leave blank
    path ('', views.store, name="store"),
    path ('cart', views.cart, name="cart"),
    path ('checkout', views.checkout, name="checkout"),
]