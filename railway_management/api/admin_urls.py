from django.urls import path
from .views import add_train

urlpatterns = [
    path('add_train/', add_train, name='admin_add_train'),
]