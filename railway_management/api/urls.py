from django.urls import path
from .views import register, login_user, add_train, get_seat_availability, book_seat, get_booking_details

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('add_train/', add_train, name='add_train'),
    path('get_seat_availability/', get_seat_availability, name='get_seat_availability'),
    path('book_seat/', book_seat, name='book_seat'),
    path('get_booking_details/', get_booking_details, name='get_booking_details'),
]
