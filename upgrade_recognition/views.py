from django.shortcuts import render, redirect
from reservation_manager.models import Reservation

# Create your views here.
def printLocationDictionary(dictionary):
    for key in dictionary:
        print(key)
        for val in dictionary[key]:
            print ("\t conf",': (', val.confirmation_number ,",",val.location, ",", val.date_of_reservation, ")")

    print("\n")

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

    printLocationDictionary(grouped_reservations_by_date)

    return grouped_reservations_by_date


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
        array_of_dictionaries_by_date.append(groupByDate(grouped_reservations_by_location[key]))

    return array_of_dictionaries_by_date

def main(request):
    array_of_dictionaries_by_date = groupByLocation(request)

    context = {
        "array_of_dictionaries_by_date" : array_of_dictionaries_by_date
    }

    return render(request,"upgrades/index.html",context)

if __name__ == '__main__':
    main()
