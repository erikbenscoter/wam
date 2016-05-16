from django.shortcuts import render, redirect
from reservation_manager.models import Reservation
from django.contrib.auth.decorators import login_required


# Create your views here.
def printLocationDictionary(dictionary):
    for key in dictionary:
        print(key)
        for val in dictionary[key]:
            print ("\t conf",': (', val.confirmation_number ,",",val.location, ",", val.date_of_reservation, ")")

    print("\n")

def groupByNights(reservation_array):
    numNights = []

    for reservation in reservation_array:
        numNights.append(reservation.number_of_nights)

    numNights = set(numNights)

    grouped_reservations_by_nights = {}

    for numNight in numNights:
        grouped_reservations_by_nights[numNight] = []
        for reservation in reservation_array:
            if(reservation.number_of_nights == numNight):
                grouped_reservations_by_nights[numNight].append(reservation)

    return grouped_reservations_by_nights;
def groupByDate(reservation_array):
    dates = []

    for reservation in reservation_array:
        dates.append(reservation.date_of_reservation)

    dates = set(dates)

    grouped_reservations_by_date = {}

    for date in dates:
        grouped_reservations_by_date[date] = []
        for reservation in reservation_array:
            if(reservation.date_of_reservation == date):
                grouped_reservations_by_date[date].append(reservation)

    array_of_dict = []
    for key in grouped_reservations_by_date:
        array_of_dict.append(groupByNights(grouped_reservations_by_date[key]))

    return array_of_dict


def groupByLocation(request):
    locations = []

    reservations = Reservation.objects.all()

    for reservation in reservations:
        locations.append(reservation.location)

    locations = set(locations)

    grouped_reservations_by_location = {}
    array_of_dictionaries_by_date = []

    for location in locations:
        reservations = Reservation.objects.filter(location=location)
        grouped_reservations_by_location[location] = reservations


    for key in grouped_reservations_by_location:
        array_of_dictionaries_by_date.extend(groupByDate(grouped_reservations_by_location[key]))

    return array_of_dictionaries_by_date


@login_required(redirect_field_name="/admin", login_url="/login/")
def main(request):
    array_of_dictionaries_by_date = groupByLocation(request)

    context = {
        "array_of_dictionaries_by_date" : array_of_dictionaries_by_date
    }

    return render(request,"upgrades/index.html",context)

if __name__ == '__main__':
    main()
