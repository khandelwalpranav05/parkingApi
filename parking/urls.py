from django.urls import path
from .views import available_space_count,vehicle_exit

urlpatterns = [
    path("/parking-spots/<ticketID>/exit", vehicle_exit),
    path("/parking-spots", available_space_count),
]
