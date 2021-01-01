from django.db.models.signals import post_save
from django.dispatch import receiver

from parking.models import ParkingSpot,VehicleDetail


@receiver(signal=post_save, sender=ParkingSpot)
def update_floor_count(sender, instance, created, *args, **kwargs):
    if instance.is_available is False:
        floor = instance.floor
        floor.available_space -= 1
        floor.save()
    else:
        floor = instance.floor
        floor.available_space += 1
        floor.save()


@receiver(signal=post_save, sender=VehicleDetail)
def update_floor_parking_spot(sender, instance, created, *args, **kwargs):
    parking_spot = instance.parking_spot
    parking_spot.ticket_id = None
    parking_spot.is_available = True
    parking_spot.save()
