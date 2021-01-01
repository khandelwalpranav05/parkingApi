import uuid

from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from .models import ParkingSpot,Floor,VehicleDetail

from rest_framework.decorators import api_view
from rest_framework.response import Response

"""
request_data = {
    "vehicle_data":{"registration_number":xxx}
    
"""

@api_view(["POST"])
def vehicle_exit(request,ticket_id:str):
    if request.method == "POST":
        vehicle_obj = VehicleDetail.objects.filter(ticket_id=ticket_id).first()
        if not vehicle_obj:
            return Response(status=status.HTTP_200_OK,data={"Message":"Ticket id not valid"})

        end_time = timezone.now()
        start_time = vehicle_obj.entered_time
        time_diff = (end_time-start_time)
        cost = (time_diff.hour*60 + time_diff.minute)*0.1
        vehicle_obj.status = VehicleDetail.EXIT
        vehicle_obj.save() # A signal reciever for updating the available space of the selected floor and is_available of parking spot obj( parking/reciver.py)
        return Response(status=status.HTTP_200_OK,data={"payment":cost})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST,data={"Message":"Bad Request"})


@api_view(["GET","POST"])
def available_space_count(request):
    if request.method == "GET":
        # aggregating all the available space in a single query and this avoids the loop
        total_available_space = Floor.objects.raw('select sum(available_space) from parking_floor')
        return Response(status=status.HTTP_200_OK,data={"total_available_space":total_available_space})
    elif request.method == "POST":
        request_body = request.data
        vehicle_data = request_body.get("vehicle_data")
        if not vehicle_data:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"Message":"Bad Request"})

        floor = Floor.objects.filter(available_space__lt=Floor.TOTAL).first()
        if not floor:
            return Response(status=status.HTTP_200_OK,data={"Message":"No parking space available"})

        parking_spot = ParkingSpot.objects.filter(floor_id=floor.id,is_available=True).first()
        ticket_id = str(uuid.uuid4())
        try:
            vehicle_obj = VehicleDetail.objects.create(registration_number=vehicle_data["registration_number"],
                                                   ticket_id=ticket_id,parking_spot=parking_spot)
            parking_spot.is_available = False
            parking_spot.save() # A signal reciever for updating the available space of the selected floor( parking/reciver.py)
            return Response(status=status.HTTP_201_CREATED,data={"ticket_id":ticket_id,"Message":"Vehicle parked"})
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={"Message":"Vehicle not parking, Please try again"})