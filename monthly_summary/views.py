from django.shortcuts import render
from reservation_manager.models import Reservation
from reservation_manager.models import Owner

# Create your views here.
class Report:
    def get(request, p_owner_username, p_year, p_month):

        reservations = Reservation.objects.filter( date_of_reservation__year=p_year,
                                    date_of_reservation__month=p_month).order_by('-date_of_reservation')
        owner = Owner.objects.get(username=p_owner_username)

        context = {
            "reservations" : reservations,
            "owner" : owner,
            "year" : p_year,
            "month" : p_month
        }
        return render(request, "report/index.html",context)
