from django.db import models
from django.forms import ModelForm
from reservation_manager.models import *

# Create your models here.

#from reservation_manager.models import Owner

TRUE_OR_FALSE = (
    (1, "True"),
    (0, "False")
)


#class OwnerPointsManagerApplicationSettings(models.Model):
#    last_updated = models.DateTimeField(blank=True, null=True)

# Create your models here.
class GuestReservation(models.Model):

#                   data from Reservations once ruth enters confimation_number
    optional_username_to_aim_for = models.CharField( max_length=2000, blank=True, null=True, default = None)

#                 data ruth enters initial
    guest = models.CharField( blank=True, null=True, max_length = 2000)
    date_rquested = models.DateField( blank=True, null=True )
    nights_requested = models.IntegerField( blank=True, null=True )
    location_requested = models.CharField( blank=True, null=True, max_length=2000)
    unit_size = models.CharField( blank=True, null=True, max_length=2000)
    sleeps = models.IntegerField( blank=True, null=True )

#                 data ruth will add along the way
    reservation = models.ForeignKey(Reservation, blank=True, null=True, default = None)
    unit_size_notes = models.CharField ( blank=True, null=True, max_length=2000 )
    rent = models.FloatField( default=0.00 )
    ad = models.CharField( blank=True, null=True, max_length=2000)
    notes = models.CharField( blank=True, null=True, max_length=2000)
    addName = models.CharField( blank=True, null=True, max_length=2000)
    guestSent = models.DateField( blank=True, null=True )
    RA_Sent_Rec =  models.CharField( blank=True, null=True, max_length=2000)
    downDue_paid = models.CharField( blank=True, null=True, max_length=2000)
    balanceDue_paid = models.CharField( blank=True, null=True, max_length=2000)
    guestCertYr_number = models.CharField( blank=True, null=True, max_length=2000)
    pointsCost = models.FloatField( default=0.00 )
    guestCertCost = models.FloatField( default=0.00 )
    ccFee = models.FloatField( default=0.00 )
    otherFees = models.FloatField( default=0.00 )
    totalCost = models.FloatField( default=0.00 )
    netDollars = models.FloatField( default=0.00 )
    netPercent = models.FloatField( default=0.00 )
    Jen = models.CharField( blank=True, null=True, max_length=2000)
    Lauren = models.CharField( blank=True, null=True, max_length=2000)


#      system will supply when original is cancelled
    prior_confirmation_number = models.CharField( blank=True, null=True, max_length=2000)



    def __str__(self):
        return str(self.username) + "   " + str(self.guest) + " , " + str(self.date_rquested) + " , " + str(
            self.confirmation_number) + " , " + str(self.location_requested) + " , " + str(self.id)

    def __unicode__(self):
        return str(self.username) + "   " + str(self.guest) + " , " + str(self.date_rquested) + " , " + str(
            self.confirmation_number) + " , " + str(self.location_requested) + " , " + str(self.id)


class CreateGuestWishForm(ModelForm):
    class Meta:
        model = GuestReservation
        exclude = []
