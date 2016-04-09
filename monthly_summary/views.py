from django.shortcuts import render
from reservation_manager.models import Reservation

# Create your views here.
class Report:
    def get(request):

        reservations = Reservation.objects.all().order_by('-date_of_reservation')

        context = {
            "reservations" : reservations
        }
        return render(request, "report/index.html",context)
