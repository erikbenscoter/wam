import re
from reservation_manager.models import Reservation
from datetime import datetime

class FuzzySearch:

    def _cleanByLocation(location, objects):

        desireable = []

        # use regular expressions to try to make a matching
        for itt in range( 0,len(objects) ):

            reservation_location = objects[itt].location
            # if it doesn't match the regular expression remove it
            if (  ( re.search(str(location), str(reservation_location) ) ) ):
                desireable.append(objects[itt])

        return desireable

    def _cleanByBedrooms(bedrooms, bedroom_range, objects):

        desireable = []

        # assure that the params are integers
        bedrooms = int(bedrooms)
        bedroom_range = int(bedroom_range)

        # calculate the bounds
        bedrooms_lower_bound = bedrooms - bedroom_range
        bedrooms_upper_bound = bedrooms + bedroom_range

        # assure the lower bound is gte 0
        if bedrooms_lower_bound <= 0:
            bedrooms_lower_bound = 0

        # form regex to match bedrooms
        # of the form "[smallNum-largeNumber]"
        # this will work because there will be no bedrooms larger than 9 rooms
        bedroom_range_regex = "[{}-{}]".format(bedrooms_lower_bound, bedrooms_upper_bound)

        # use regular expressions to try to make a matching
        for itt in range( 0,len(objects) ):

            reservation_bedroom = str(objects[itt].unit_size)

            # if it doesn't match the regular expression remove it
            if ( ( re.search(bedroom_range_regex, reservation_bedroom ) ) ):
                desireable.append(objects[itt])

        return desireable

    def _cleanByDate(beg_date, end_date, objects):

        beg_date = str(beg_date).replace('/', '-')
        end_date = str(end_date).replace('/', '-')


        all_reservation_objs_in_range = Reservation.objects.filter(date_of_reservation__range=[beg_date,end_date])

        matching_reservations = []

        for reservation in objects :
            if reservation in all_reservation_objs_in_range :
                matching_reservations.append(reservation)

        return matching_reservations

    def _cleanByNights(nights, nights_range, objects):

        desireable = []

        # assure that the params are integers
        nights = int(nights)
        nights_range = int(nights_range)

        # calculate the bounds
        nights_lower_bound = nights - nights_range
        nights_upper_bound = nights + nights_range

        # assure the lower bound is gte 0
        if nights_lower_bound <= 0:
            nights_lower_bound = 0

        # use regular expressions to try to make a matching
        for itt in range( 0,len(objects) ):

            reservation_nights = str(objects[itt].number_of_nights)
            reservation_nights = int(re.findall("[0-9]*", reservation_nights)[0])

            # if it doesn't match the regular expression remove it
            if ( reservation_nights >= nights_lower_bound and reservation_nights <= nights_upper_bound ):
                desireable.append(objects[itt])

        return desireable

    def fuzzySearch(location, bedrooms, bedroom_range, nights, nights_range, beg_date, end_date):

        # Don't put in any reservations that are:
            # already rented
            # being used by the Owner
            # already passed
            # canceled
        matching_reservations = list(Reservation.objects.filter(canceled=False, reason_on_hold="NH"))

        # filter out based on the parameters given
        matching_reservations = FuzzySearch._cleanByLocation(location, matching_reservations)
        matching_reservations = FuzzySearch._cleanByBedrooms(bedrooms, bedroom_range, matching_reservations)
        matching_reservations = FuzzySearch._cleanByDate(beg_date, end_date, matching_reservations)
        matching_reservations = FuzzySearch._cleanByNights(nights, nights_range, matching_reservations)

        # return the matching reservations
        return matching_reservations
