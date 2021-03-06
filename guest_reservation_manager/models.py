from django.db import models
from django.forms import ModelForm
import datetime
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
    beg_date_requested = models.DateField( blank=True, null=True )
    end_date_requested = models.DateField( blank=True, null=True )

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
    # confirmation_number = models.CharField( blank=True, null=True, max_length=2000)
    date_booked = models.DateField( blank=True, null=True )
    location = models.CharField( blank=True, null=True, max_length=2000)
    points_required_for_reservation = models.IntegerField( blank=True, null=True )

#      system will supply when original is cancelled
    prior_confirmation_number = models.CharField( blank=True, null=True, max_length=2000)

    @property
    def confirmation_numbers(self):
        from reservation_manager.models import Reservation

        matching_reservations = []

        for reservation in Reservation.objects.all():
            if reservation.fk_wish_held_for == self:
                matching_reservations.append( reservation.confirmation_number )

        return matching_reservations

    @property
    def reservations(self):
        from reservation_manager.models import Reservation

        reservations_arr = []
        for reservation in Reservation.objects.all():
            if reservation.fk_wish_held_for == self:
                reservations_arr.append(reservation)

        return reservations_arr


    def getLinkedWishes():
        linked_wishes_arr = []
        all_wishes_arr = GuestReservation.objects.order_by("beg_date_requested")


        for wish in all_wishes_arr :
            if len(wish.reservations) > 0 :
                greatest_date = datetime.date(1999,1,1)

                # get the greatest checkin date
                for reservation in wish.reservations:
                    if reservation.date_of_reservation > greatest_date :
                        greatest_date = reservation.date_of_reservation

                print(greatest_date)

                # if the greatest checkin date is greater than now append the wish
                if greatest_date >= datetime.date.today() :
                    linked_wishes_arr.append(wish)

        return linked_wishes_arr


    def getUnLinkedWishes():
        non_linked_wishes_arr = []
        all_wishes_arr = GuestReservation.objects.order_by("beg_date_requested")

        for wish in all_wishes_arr :
            if len(wish.reservations) == 0 and wish.end_date_requested >= datetime.date.today():
                non_linked_wishes_arr.append(wish)

        return non_linked_wishes_arr

    def getWishesLinkedToCanceled():
        pass

    def getPossibleMatches():
        pass



    def __str__(self):
        return str(self.optional_username_to_aim_for) + "   " + str(self.guest) + " , " + str(self.beg_date_requested) + " , " + str(self.end_date_requested) + " , " +" , " + str(self.location_requested) + " , " + str(self.id)

    def __unicode__(self):
        return str(self.optional_username_to_aim_for) + "   " + str(self.guest) + " , " + str(self.beg_date_requested) + " , " + str(self.end_date_requested) + " , " +" , " + str(self.location_requested) + " , " + str(self.id)


class RuthSheet(models.Model):
    A_ResDate = models.CharField( blank=True, null=True, max_length = 2000)
    B_UseDate = models.CharField( blank=True, null=True, max_length = 2000)
    C_NTS = models.CharField( blank=True, null=True, max_length = 2000)
    D_Resort = models.CharField( blank=True, null=True, max_length = 2000)
    E_UnitSize = models.CharField( blank=True, null=True, max_length = 2000)
    F_Slp = models.CharField( blank=True, null=True, max_length = 2000)

    def __str__(self):
        return str(self.id) + "," + str(self.A_ResDate) + "   " + str(self.B_UseDate) + " , " + str(self.C_NTS) + " , " +  str(self.D_Resort) + " , " + str(self.E_UnitSize)+ " , " + str(self.F_Slp)

    def __unicode__(self):
        return str(self.id) + "," + str(self.A_ResDate) + "   " + str(self.B_UseDate) + " , " + str(self.C_NTS) + " , " +  str(self.D_Resort) + " , " + str(self.E_UnitSize)+ " , " + str(self.F_Slp)


class CreateGuestWishForm(ModelForm):
    class Meta:
        model = GuestReservation
        exclude = []

class GuestWishForm1(ModelForm):
    class Meta:
        model = GuestReservation
        fields = ["guest", "beg_date_requested", "end_date_requested" ,"nights_requested", "location_requested", "unit_size", "sleeps"]

class GuestWishForm2(ModelForm):
    class Meta:
        model = GuestReservation
        fields = [
            "unit_size_notes",
            "rent",
            "ad",
            "notes",
            "add_name",
            "guest_sent",
            "ra_sent_rec",
            "down_due_paid",
            "balance_due_paid",
            "guest_cert_yr_number",
            "points_cost",
            "guest_cert_cost",
            "cc_fee",
            "other_fees",
            "total_cost",
            "net_dollars",
            "net_percent",
            "jen",
            "lauren"
        ]

class GuestWishForm3(ModelForm):
    class Meta:
        model = GuestReservation
        fields = ["guest", "beg_date_requested", "end_date_requested", "nights_requested", "location_requested", "unit_size", "sleeps"]
