from django.db import models
from monthly_summary.models import MonthlyReport
from django.contrib.auth.models import User
from guest_reservation_manager.models import GuestReservation
import re
from django.forms import ModelForm

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
    owner_reimbursement_rate = models.FloatField( blank=True, null=True )

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
        return (self.fk_owner.owner_reimbursement_rate * self.points_required_for_reservation / 1000.00 )


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



    def __str__(self):
        return str(self.confirmation_number) + "," +  str(self.fk_owner.username) + " ,  " + str(self.date_of_reservation) + " , " + str(self.location)
    def __unicode__(self):
        return str(self.confirmation_number) + "," +  str(self.fk_owner.username) + " ,  " + str(self.date_of_reservation) + " , " + str(self.location)


class ReasonHeldForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ["reason_on_hold"]
