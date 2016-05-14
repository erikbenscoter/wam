from django.db import models
from datetime import datetime


# get_user_model("reservation_manager.models.Reservation")


# Create your models here.
class MonthlyReport(models.Model):
    check_number = models.CharField( blank=True, null=True, max_length=2000 )
    amount_paid = models.FloatField( default=0.00 )
    date_paid = models.DateTimeField( null=True, default=None, blank=True )


    @property
    def total_owed_owner_month(self):
        from reservation_manager.models import Reservation
        reservations = Reservation.objects.filter(fk_monthly_report=self)

        total_owed = 0

        for reservation in reservations:
            total_owed += reservation.owed_owner

        return total_owed

    @property
    def owner(self):
        from reservation_manager.models import Reservation

        reservation = Reservation.objects.filter(fk_monthly_report=self)

        try:
            reservation = reservation[0]
            return reservation.fk_owner
        except:
            return None


    @property
    def month(self):
        from reservation_manager.models import Reservation

        reservation = Reservation.objects.filter(fk_monthly_report=self)

        try:
            reservation = reservation[0]
            return reservation.date_of_reservation.month
        except:
            return None


    @property
    def year(self):
        from reservation_manager.models import Reservation

        reservation = Reservation.objects.filter(fk_monthly_report=self)

        try:
            reservation = reservation[0]
            return reservation.date_of_reservation.year
        except:
            return None


    def __str__(self):
        return str(self.month) + " " + str(self.year) +" "+ str(self.owner)
