from django.shortcuts import render, redirect
from .models import *

# Create your views here.

# def makeNewWish(request):
#     if request.POST:
#         wish_form = CreateGuestWishForm(request.POST)
#         if wish_form.is_valid():
#             wish_form.save()
#     else:
#         wish_form = CreateGuestWishForm()
#
#     context = {
#         "form" : wish_form
#     }
#     return render(request, 'new_wish/index.html', context)


def displayForm(request, step_number, form):

    context = {
        "form" : form,
        "step_number" : step_number,
        "url" : request.path
    }
    return render(request, 'new_wish/index1.html', context)

########################################
# url = /guest/makeWish
########################################
def makeNewWish1(request):
    if request.POST:
        print("POSTED")
        wish_form = GuestWishForm1(request.POST)
        if wish_form.is_valid():
            wish_form.save()
            return redirect("/guest/makeWish2/"+str(wish_form.instance.id))
        else:
            return displayForm(request,1,GuestWishForm1())
    else:
        return displayForm(request,1,GuestWishForm1())

########################################
# url = /guest/makeWish2
########################################
def makeNewWish2(request, wish_id):
    instance = GuestReservation.objects.get(id=wish_id)
    if request.POST:
        wish_form = GuestWishForm2(request.POST, instance=instance)
        if wish_form.is_valid():
            wish_form.save()
            return redirect("/guestreservationview")
        else:
            return displayForm(request,2,GuestWishForm2(instance=instance))
    else:
        return displayForm(request,2,GuestWishForm2(instance=instance))

########################################
# url = /guest/makeWish3
########################################
def makeNewWish3(request, wish_id):
    if request.POST:
        wish_form = GuestWishForm3(request.POST)
        if wish_form.is_valid():
            wish_form.save()
            return redirect("/guestreservationview")
        else:
            return displayForm(request,3,GuestWishForm3)
    else:
        return displayForm(request,3,GuestWishForm3)

class View:

#    @login_required(redirect_field_name="/admin", login_url="/login/")
    def get(request):
        guestreservation = []

        ad = []
        addName = []
        balanceDue_paid = []
        ccFee = []
        confirmation_number = []
        date_booked = []
        date_requested = []
        downDue_paid = []
        guest = []
        guestCertCost = []
        guestCertYr_number = []
        guestSent = []
        Jen = []
        Lauren = []
        location = []
        location_requested = []
        netDollars = []
        netPercent = []
        nights_requested = []
        notes = []
        otherFees = []
        points_required_for_reservation = []
        pointsCost = []
        RA_Sent_Rec = []
        rent = []
        sleeps = []
        totalCost = []
        unit_size = []
        unit_size_notes = []


#        newest_date = ReservationManagerApplicationSettings.objects.all()
#        newest_date = newest_date[0].last_updated
#        print (newest_date)
#        newest_date = newest_date + timedelta(hours=-4)
#        newest_date = newest_date.strftime("%Y-%m-%d %H:%M:%S")


#        reservations = Reservation.objects.filter(date_of_reservation__gte=datetime.today())

        GuestReservations = GuestReservation.objects.order_by("date_requested")

        for guestreservation in GuestReservations:
            ad.append(guestreservation.ad)

        for guestreservation in GuestReservations:
            addName.append(guestreservation.add_name)

        for guestreservation in GuestReservations:
            balanceDue_paid.append(guestreservation.balance_due_paid)

        for guestreservation in GuestReservations:
            ccFee.append(guestreservation.cc_fee)

        for guestreservation in GuestReservations:
            confirmation_number.append(guestreservation.confirmation_number)

        for guestreservation in GuestReservations:
            date_booked.append(guestreservation.date_booked)

        for guestreservation in GuestReservations:
            date_requested.append(guestreservation.date_requested)

        for guestreservation in GuestReservations:
            downDue_paid.append(guestreservation.down_due_paid)

        for guestreservation in GuestReservations:
            guest.append(guestreservation.guest)

        for guestreservation in GuestReservations:
            guestCertCost.append(guestreservation.guest_cert_cost)

        for guestreservation in GuestReservations:
            guestCertYr_number.append(guestreservation.guest_cert_yr_number)

        for guestreservation in GuestReservations:
            guestSent.append(guestreservation.guest_sent)

        for guestreservation in GuestReservations:
            Jen.append(guestreservation.jen)

        for guestreservation in GuestReservations:
            Lauren.append(guestreservation.lauren)

        for guestreservation in GuestReservations:
            location.append(guestreservation.location)

        for guestreservation in GuestReservations:
            location_requested.append(guestreservation.location_requested)

        for guestreservation in GuestReservations:
            netDollars.append(guestreservation.net_dollars)

        for guestreservation in GuestReservations:
            netPercent.append(guestreservation.net_percent)

        for guestreservation in GuestReservations:
            nights_requested.append(guestreservation.nights_requested)

        for guestreservation in GuestReservations:
            notes.append(guestreservation.notes)

        for guestreservation in GuestReservations:
            otherFees.append(guestreservation.other_fees)

        for guestreservation in GuestReservations:
            points_required_for_reservation.append(guestreservation.points_required_for_reservation)

        for guestreservation in GuestReservations:
            pointsCost.append(guestreservation.points_cost)

        for guestreservation in GuestReservations:
            RA_Sent_Rec.append(guestreservation.ra_sent_rec)

        for guestreservation in GuestReservations:
            rent.append(guestreservation.rent)

        for guestreservation in GuestReservations:
            sleeps.append(guestreservation.sleeps)

        for guestreservation in GuestReservations:
            totalCost.append(guestreservation.total_cost)

        for guestreservation in GuestReservations:
            unit_size.append(guestreservation.unit_size)

        for guestreservation in GuestReservations:
            unit_size_notes.append(guestreservation.unit_size_notes)


#        for reservation in reservations:
#            usernames.append(reservation.fk_owner.username)

#        for reservation in reservations:
#            resorts.append(reservation.location)

#        for reservation in reservations:
#            unit_sizes.append(reservation.unit_size)

#        for reservation in reservations:
#            travelers.append(reservation.guest_certificate)

#        for reservation in reservations:
#            upgrades.append(reservation.upgrade_status)



        context = {
#            "reservations" : reservations.order_by('date_of_reservation'),
            "guestreservations" : GuestReservations,

            "ad" : set(ad),
            "addName" : set(addName),
            "balanceDue_paid" : set(balanceDue_paid),
            "ccFee" : set(ccFee),
            "confirmation_number" : set(confirmation_number),
            "date_booked" : set(date_booked),
            "date_requested" : set(date_requested),
            "downDue_paid" : set(downDue_paid),
            "guests" : set(guest),
            "guestCertCost" : set(guestCertCost),
            "guestCertYr_number" : set(guestCertYr_number),
            "guestSent" : set(guestSent),
            "Jen" : set(Jen),
            "Lauren" : set(Lauren),
            "location" : set(location),
            "location_requesteds" : set(location_requested),
            "netDollars" : set(netDollars),
            "netPercent" : set(netPercent),
            "nights_requested" : set(nights_requested),
            "notes" : set(notes),
            "otherFees" : set(otherFees),
            "points_required_for_reservation" : set(points_required_for_reservation),
            "pointsCost" : set(pointsCost),
            "RA_Sent_Rec" : set(RA_Sent_Rec),
            "rent" : set(rent),
            "rent" : set(rent),
            "totalCost" : set(totalCost),
            "unit_size" : set(unit_size),
            "unit_size_notes" : set(unit_size_notes)





        }

        return render( request, "guest_reservations/index.html", context)
