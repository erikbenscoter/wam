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
#    id = models.IntegerField( blank=False, null=False,primary_key=True )
    optional_username_to_aim_for = models.CharField( max_length=2000, blank=True, null=True, default = None)

#                 data ruth enters initial
    guest = models.CharField( blank=True, null=True, max_length = 2000)
    date_rquested = models.DateField( blank=True, null=True )
    nights_requested = models.IntegerField( blank=True, null=True )
    location_requested = models.CharField( blank=True, null=True, max_length=2000)
    unit_size = models.CharField( blank=True, null=True, max_length=2000)
    sleeps = models.IntegerField( blank=True, null=True )

#                 data ruth will add along the way
    unit_size_notes = models.CharField ( blank=True, null=True, max_length=2000 )
    rent = models.FloatField( default=0.00 )
    ad = models.CharField( blank=True, null=True, max_length=2000)
    notes = models.CharField( blank=True, null=True, max_length=2000)
    add_name = models.CharField( blank=True, null=True, max_length=2000)
    guest_sent = models.DateField( blank=True, null=True )
    ra_sent_rec =  models.CharField( blank=True, null=True, max_length=2000)
    down_due_paid = models.CharField( blank=True, null=True, max_length=2000)
    balance_due_paid = models.CharField( blank=True, null=True, max_length=2000)
    guest_cert_yr_number = models.CharField( blank=True, null=True, max_length=2000)
    points_cost = models.FloatField( default=0.00 )
    guest_cert_cost = models.FloatField( default=0.00 )
    cc_fee = models.FloatField( default=0.00 )
    other_fees = models.FloatField( default=0.00 )
    total_cost = models.FloatField( default=0.00 )
    net_dollars = models.FloatField( default=0.00 )
    net_percent = models.FloatField( default=0.00 )
    jen = models.CharField( blank=True, null=True, max_length=2000)
    lauren = models.CharField( blank=True, null=True, max_length=2000)

#  data that can come from reservations
    confirmation_number = models.CharField( blank=True, null=True, max_length=2000)
    date_booked = models.DateField( blank=True, null=True )
    location = models.CharField( blank=True, null=True, max_length=2000)
    points_required_for_reservation = models.IntegerField( blank=True, null=True )

#      system will supply when original is cancelled
    prior_confirmation_number = models.CharField( blank=True, null=True, max_length=2000)

    @property
    def reservations(self):
        # TODO implement this after making the Reservation model changes
        pass


    def __str__(self):
        return str(self.optional_username_to_aim_for) + "   " + str(self.guest) + " , " + str(self.date_rquested) + " , " + " , " + str(self.location_requested) + " , " + str(self.id)

    def __unicode__(self):
        return str(self.optional_username_to_aim_for) + "   " + str(self.guest) + " , " + str(self.date_rquested) + " , " + " , " + str(self.location_requested) + " , " + str(self.id)


class CreateGuestWishForm(ModelForm):
    class Meta:
        model = GuestReservation
        exclude = []
