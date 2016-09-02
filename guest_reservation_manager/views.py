from django.shortcuts import render, redirect
from .models import *
from reservation_manager.fuzzySearch import FuzzySearch
from reservation_manager.models import Reservation
from reservation_manager.models import ReasonHeldForm

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


def displayMatchingReservations(request, wish_id):


    wish = GuestReservation.objects.get(id=wish_id)

    location = wish.location_requested
    bedrooms = wish.unit_size
    bedroom_range = 2
    nights = wish.nights_requested
    nights_range = 4
    beg_date = wish.beg_date_requested
    end_date = wish.end_date_requested

    already_linked_reservations = wish.reservations

    reservations = FuzzySearch.fuzzySearch(
        location,
        bedrooms,
        bedroom_range,
        nights,
        nights_range,
        beg_date,
        end_date
    )


    context = {
        "already_linked_reservations" : already_linked_reservations,
        "reservations" : reservations,
        "wish_id" : wish_id,
        "heldForForm" : ReasonHeldForm()
    }


    return render(request, 'link_wish/index.html', context)
########################################
# url = /guest/wish/new
########################################
def makeBrandNewWish(request):
    if request.POST:
        wish_form = GuestWishForm1(request.POST)
        if wish_form.is_valid():
            wish_form.save()
            return redirect("/guest/makeWish2/"+str(wish_form.instance.id))
        else:
            return displayForm(request,1,GuestWishForm1())
    else:
        return displayForm(request,1,GuestWishForm1())

########################################
# url = /guest/makeWish/wish_id
########################################
def makeNewWish1(request, wish_id):
    instance = GuestReservation.objects.get(id=wish_id)
    if request.POST:
        wish_form = GuestWishForm1(request.POST, instance=instance)
        if wish_form.is_valid():
            wish_form.save()
            return redirect("/guest/makeWish2/"+str(wish_form.instance.id))
        else:
            return displayForm(request,1,GuestWishForm1(instance=instance))
    else:
        return displayForm(request,1,GuestWishForm1(instance=instance))

########################################
# url = /guest/makeWish2
########################################
def makeNewWish2(request, wish_id):
    instance = GuestReservation.objects.get(id=wish_id)
    if request.POST:
        wish_form = GuestWishForm2(request.POST, instance=instance)
        if wish_form.is_valid():
            wish_form.save()
            return redirect("/guest/makeWish3/"+str(wish_form.instance.id))
        else:
            return displayForm(request,2,GuestWishForm2(instance=instance))
    else:
        return displayForm(request,2,GuestWishForm2(instance=instance))

########################################
# url = /guest/makeWish3
########################################
def makeNewWish3(request, wish_id):
    return displayMatchingReservations(request, wish_id)


#######################################
# url = /guest/makeWish3/link/reservation_id/wish_id
#######################################
def commitLink(request, reservation_id, wish_id):

    instance = Reservation.objects.select_related().filter(id=reservation_id)
    instance.update(fk_wish_held_for=wish_id)

    instance = Reservation.objects.get(id=reservation_id)
    if request.POST:
        reason_held_form = ReasonHeldForm(request.POST, instance=instance)
        if reason_held_form.is_valid():
            reason_held_form.save()


    return redirect("/guest/makeWish3/"+str(wish_id))

#######################################
# url = /guest/wish/remove/reservation_id
#######################################
def removeLink(request, reservation_id, wish_id):

    instance = Reservation.objects.select_related().filter(id=reservation_id)
    instance.update(fk_wish_held_for=None, reason_on_hold="NH")

    return redirect("/guest/makeWish3/"+str(wish_id))

#######################################
# url = /guest/wish/dashboard
#######################################
def summarizeWish(request):

    context = {
        "num_fulfilled" : len(GuestReservation.getLinkedWishes()),
        "num_unFulfilled" : len(GuestReservation.getUnLinkedWishes()),
        "num_reservations_unLinked" : len(Reservation.getUnlinkedReservations())
    }

    return render(request,"dashboard/index.html", context)

#######################################
# url = /guest/wish/view/fulfilledWishes/
#######################################
def showLinkedWishes(request):
    return View.get(request, GuestReservation.getLinkedWishes() )

#######################################
# url = /guest/wish/view/UnFulfilledWishes/
#######################################
def showUnLinkedWishes(request):
    return View.get(request, GuestReservation.getUnLinkedWishes() )



class View:

#    @login_required(redirect_field_name="/admin", login_url="/login/")
    def get(request, guest_reservations=None):
        guestreservation = []

        ad = []
        addName = []
        balanceDue_paid = []
        ccFee = []
        confirmation_number = []
        date_booked = []
        beg_date_requested = []
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

        if not guest_reservations:
            guest_reservations = GuestReservation.objects.order_by("beg_date_requested")


        for guestreservation in guest_reservations:
            ad.append(guestreservation.ad)

        for guestreservation in guest_reservations:
            addName.append(guestreservation.add_name)

        for guestreservation in guest_reservations:
            balanceDue_paid.append(guestreservation.balance_due_paid)

        for guestreservation in guest_reservations:
            ccFee.append(guestreservation.cc_fee)

        for guestreservation in guest_reservations:
            confirmation_number.append(guestreservation.confirmation_numbers)

        for guestreservation in guest_reservations:
            date_booked.append(guestreservation.date_booked)

        for guestreservation in guest_reservations:
            beg_date_requested.append(guestreservation.beg_date_requested)

        for guestreservation in guest_reservations:
            downDue_paid.append(guestreservation.down_due_paid)

        for guestreservation in guest_reservations:
            guest.append(guestreservation.guest)

        for guestreservation in guest_reservations:
            guestCertCost.append(guestreservation.guest_cert_cost)

        for guestreservation in guest_reservations:
            guestCertYr_number.append(guestreservation.guest_cert_yr_number)

        for guestreservation in guest_reservations:
            guestSent.append(guestreservation.guest_sent)

        for guestreservation in guest_reservations:
            Jen.append(guestreservation.jen)

        for guestreservation in guest_reservations:
            Lauren.append(guestreservation.lauren)

        for guestreservation in guest_reservations:
            location.append(guestreservation.location)

        for guestreservation in guest_reservations:
            location_requested.append(guestreservation.location_requested)

        for guestreservation in guest_reservations:
            netDollars.append(guestreservation.net_dollars)

        for guestreservation in guest_reservations:
            netPercent.append(guestreservation.net_percent)

        for guestreservation in guest_reservations:
            nights_requested.append(guestreservation.nights_requested)

        for guestreservation in guest_reservations:
            notes.append(guestreservation.notes)

        for guestreservation in guest_reservations:
            otherFees.append(guestreservation.other_fees)

        for guestreservation in guest_reservations:
            points_required_for_reservation.append(guestreservation.points_required_for_reservation)

        for guestreservation in guest_reservations:
            pointsCost.append(guestreservation.points_cost)

        for guestreservation in guest_reservations:
            RA_Sent_Rec.append(guestreservation.ra_sent_rec)

        for guestreservation in guest_reservations:
            rent.append(guestreservation.rent)

        for guestreservation in guest_reservations:
            sleeps.append(guestreservation.sleeps)

        for guestreservation in guest_reservations:
            totalCost.append(guestreservation.total_cost)

        for guestreservation in guest_reservations:
            unit_size.append(guestreservation.unit_size)

        for guestreservation in guest_reservations:
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
            "guestreservations" : guest_reservations,

            "ad" : set(ad),
            "addName" : set(addName),
            "balanceDue_paid" : set(balanceDue_paid),
            "ccFee" : set(ccFee),
            # "confirmation_numbers" : set(confirmation_number),
            "date_booked" : set(date_booked),
            "beg_date_requested" : set(beg_date_requested),
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
