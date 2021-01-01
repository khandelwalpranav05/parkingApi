from django.db import models

# Create your models here.


class Floor(models.Model):
    TOTAL = 25
    available_space = models.IntegerField(default=TOTAL)
    floor_number = models.PositiveSmallIntegerField(unique=True)


class ParkingSpot(models.Model):
    # chosing PositiveSmallIntegerField to optimise db space
    row = models.PositiveSmallIntegerField()
    col = models.PositiveSmallIntegerField()
    is_available = models.BooleanField(default=True)
    ticket_id = models.CharField(null=True,blank=True,max_length=256)
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE)


class VehicleDetail(models.Model):

    PARKED = 0
    EXIT = 1
    VEHICLE_STATUS = (
        (PARKED,"parked"),
        (EXIT,"exit")
    )

    registration_number = models.CharField(unique=True,max_length=256)
    entered_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField()
    status = models.CharField(choices=VEHICLE_STATUS,default=0,max_length=50)
    ticket_id = models.CharField(null=True, blank=True, max_length=256)
    parking_spot = models.ForeignKey(ParkingSpot,on_delete=models.CASCADE)

"""
Here's we are assuming that the model Floor and ParkingSpot are prepopulated before interacting with any API call
5 floor objects will get populated with available_space as 25 representing all 5 floors
125 parking spot objects will get populated with 25 each for each floor and with row and col values varies from 0 to 5
"""