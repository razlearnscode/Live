from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wishlist", views.show_wishlist, name="show_wishlist"),
    path("add_to_wishlist/<int:card_id>", views.add_to_wishlist, name="add_to_wishlist"),
    path("remove_from_wishlist/<int:card_id>", views.remove_from_wishlist, name="remove_from_wishlist"),
]