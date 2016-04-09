from django.db import models
from datetime import datetime
# from reservation_manager.models import Reservation

# Create your models here.
class MonthlyReport(models.Model):
    check_number = models.CharField( blank=True, null=True, max_length=2000 )
    amount_paid = models.FloatField( default=0.00 )
    date_paid = models.DateTimeField( default=datetime.now , blank=True )

    @property
    def total_owed_owner_month(self):
        reservations = Reservation.objects.filter(fk_monthly_report=self)

        total_owed = 0

        for reservation in reservations:
            total_owed += reservation.owed_owner

        return total_owed
