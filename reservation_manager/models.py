from django.db import models
from monthly_summary.models import MonthlyReport
from django.contrib.auth.models import User
from guest_reservation_manager.models import GuestReservation
import re
from django.forms import ModelForm
from datetime import datetime

TRUE_OR_FALSE = (
    (1, "True"),
    (0, "False")
)

REASON_ON_HOLD_CHOICES = (
	("UPGD", "Needed For Upgrade"),
	("WSH","Guest requested this"),
	("OWN","Owner requested this"),
	("NH", "Not being held")
)

# Create your models here.
class Owner( models.Model ):
    email = models.EmailField( blank=True, null=True )
    username = models.CharField(  max_length=2000)
    password = models.CharField(  max_length=2000)
    first_name = models.CharField( blank=True, null=True, max_length=2000)
    last_name = models.CharField( blank=True, null=True, max_length=2000)
    phone_number = models.CharField( blank=True, null=True, max_length=2000)
    owner_reimbursement_rate = models.DecimalField( blank=True, null=True, decimal_places=0, max_digits=3)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

class ReservationManagerApplicationSettings(models.Model):
    last_updated = models.DateTimeField(blank=True, null=True)
    last_updated_by = models.ForeignKey(User, blank=True, null=True)

class Reservation( models.Model ):
    fk_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True)
    fk_monthly_report = models.ForeignKey(MonthlyReport, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    fk_wish_held_for = models.ForeignKey(GuestReservation, on_delete=models.SET_NULL, null=True,blank=True, default=None)
    reason_on_hold = models.CharField(max_length=5, choices = REASON_ON_HOLD_CHOICES,default="NH")
    location = models.CharField( blank=True, null=True, max_length=2000)
    date_of_reservation = models.DateField( blank=True, null=True )
    number_of_nights = models.IntegerField( blank=True, null=True )
    unit_size = models.CharField( blank=True, null=True, max_length=2000)
    confirmation_number = models.CharField( max_length=2000)
    points_required_for_reservation = models.IntegerField( blank=True, null=True )
    is_buyer_lined_up = models.IntegerField( blank=True, null=True, choices = TRUE_OR_FALSE) # remove this
    amount_paid = models.FloatField( blank=True, null=True )
    date_booked = models.DateField( blank=True, null=True )
    upgrade_status = models.CharField( blank=True, null=True, max_length = 2000)
    guest_certificate = models.CharField( blank=True, null=True, max_length = 2000)
    touched = models.DateField( blank=True, null=True,default=None )
    touched_bool = models.NullBooleanField(blank=True,null=True,default=None)
    canceled = models.NullBooleanField(blank=True, null=True, default=None)



    @property
    def owed_owner(self):
        ret_val = ((float(self.fk_owner.owner_reimbursement_rate)/1000.00 * self.points_required_for_reservation ))
        ret_val =  format(round(ret_val,2), '.2f')
        return ret_val

    @property
    def is_rented(self):
        if( re.search("Owner:",self.guest_certificate) ):
            return False
        else:
            return True

    @property
    def is_held_for_owner(self):
        if(self.reason_on_hold == "OWN"):
            return True
        else:
            return False

    @property
    def filtered_location(self):
        ret_val = str(self.location)
        ret_val = ret_val.replace("Wyndham Vacation Resorts at","")
        ret_val = ret_val.replace("Wyndham Vacation Resorts","")
        ret_val = ret_val.replace("Wyndham", "")
        ret_val = str(ret_val).strip()
        return ret_val

    @property
    def filtered_guest_certificate(self):
        ret_val = str(self.guest_certificate)
        ret_val = ret_val.replace("Guest:","")
        ret_val = str(ret_val).strip()
        return ret_val

    @property
    def filtered_points_required_for_reservation(self):
        ret_val = str(self.points_required_for_reservation)
        ret_val = float(float(ret_val)/1000.00)
        ret_val =  format(round(ret_val,3), '.3f')
        return ret_val

    @property
    def filtered_reason_on_hold(self):
        key = self.reason_on_hold
        for tup in REASON_ON_HOLD_CHOICES:
            if tup[0] == key :
                value = tup[1]
        return value


    def getUnlinkedReservations():
        non_linked = []
        all_non_canceled_reservations = Reservation.objects.filter(canceled=False, date_of_reservation__gte=datetime.now())
        for reservation in all_non_canceled_reservations :
            if reservation.fk_wish_held_for == None :
                non_linked.append(reservation)

        return non_linked

    def __str__(self):
        return str(self.confirmation_number) + "," +  str(self.fk_owner.username) + " ,  " + str(self.date_of_reservation) + " , " + str(self.location)
    def __unicode__(self):
        return str(self.confirmation_number) + "," +  str(self.fk_owner.username) + " ,  " + str(self.date_of_reservation) + " , " + str(self.location)


class ReasonHeldForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ["reason_on_hold"]
