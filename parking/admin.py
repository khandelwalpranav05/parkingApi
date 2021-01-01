from django.contrib import admin
from .models import ParkingSpot,Floor, VehicleDetail
# Register your models here.

admin.site.register(VehicleDetail)
admin.site.register(ParkingSpot)
admin.site.register(Floor)
