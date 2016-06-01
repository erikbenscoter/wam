from django.shortcuts import render
from django.shortcuts import redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from .models import Reservation, Owner, ReservationManagerApplicationSettings
from django.http import HttpResponse
from datetime import datetime
import csv
from threading import Thread
from monthly_summary.models import MonthlyReport
from monthly_summary.views import Report
from datetime import timedelta
from django.contrib.auth.decorators import login_required


def handleOwner(owner):

    reservations = Reservation.objects.all()

    confirmation_numbers_points_dict = dict()

    for reservation in reservations:
        confirmation_numbers_points_dict[reservation.confirmation_number] = reservation.points_required_for_reservation


    try:
        scrape_wyndham = ScrapeWyndham()
        time.sleep(2)
        scrape_wyndham.login(owner.username, owner.password)
        time.sleep(2)
        scrape_wyndham.getToOwnershipSummaryPage()
        time.sleep(2)
        src = scrape_wyndham.getConfirmationPages(owner, confirmation_numbers_points_dict)
        time.sleep(2)
        scrape_wyndham.logout()
        scrape_wyndham.browser.close()
    except Exception as e:
        scrape_wyndham.browser.close()
        handleOwner(owner)


class ScrapeWyndham:

    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.get("https://www.myclubwyndham.com/ffr/index.do")

    def isOffHours():
        if( datetime.now().hour == 23 or (datetime.now().hour >= 0 and datetime.now().hour < 7) ):
            return True
        else:
            return False

    def reformatDate(self, p_date):
        new_date = p_date.replace("/", "-")
        month = re.split("-", new_date)[0]
        day = re.split("-", new_date)[1]
        year = re.split("-", new_date)[2]

        new_date = str(year) + "-" + str(month) + "-" + str(day)
        return new_date

    def login(self, username, password):

        element = self.browser.find_element_by_id("userNamelabelId")
        element.send_keys(str(username))

        element = self.browser.find_element_by_id("passwordlabelId")
        element.send_keys(str(password))

        element = self.browser.find_element_by_class_name("owner-signin-btn")
        element.click()



    def logout(self):

        element = self.browser.find_element_by_link_text("Logout")
        element.click()

    def getToOwnershipSummaryPage(self):
        element = self.browser.find_element_by_link_text("MY MEMBERSHIP")

        builder = ActionChains(self.browser)
        builder.move_to_element(element)
        builder.perform()

        element = self.browser.find_element_by_link_text("View Confirmations")
        element.click()

    def parsePointsPage(self, p_src):
        allInformationIsNotOnline = re.search("Please allow 48 hours for", p_src)
        allInformationIsOnline = not allInformationIsNotOnline

        if(allInformationIsOnline):
            points = re.split("Points Used", p_src)[1]
            points = re.split("</strong>", points)[1]
            points = re.split("</p>", points)[0]
            points = points.strip()
        else:
            points = -1
        return points

    def getToPointsPage(self, p_confirmaion_number):
        time.sleep(1)
        element = self.browser.find_element_by_link_text(str(p_confirmaion_number))
        element.click()
        time.sleep(3)
        points = self.parsePointsPage(self.browser.page_source)
        self.browser.back()
        time.sleep(1)
        return points

    def parseConfirmationRow(self,p_row_text,p_owner, p_confirmaion_numbers_pts_dict):
        conf = p_row_text[0]
        checkin = p_row_text[1]
        nights = p_row_text[2]
        resort = p_row_text[3]
        unit = p_row_text[4]
        booked = p_row_text[5]
        traveler = p_row_text[6]
        upgrade = p_row_text[7]

        booked = self.reformatDate(booked)
        checkin = self.reformatDate(checkin)

        if( conf not in p_confirmaion_numbers_pts_dict.keys() ):

            if( conf != 'N/A' ):
                time.sleep(1)
                pts = self.getToPointsPage(conf)
            else:
                pts = -1

            reservation = Reservation(confirmation_number = conf, date_of_reservation=checkin,
                number_of_nights=nights, location=resort, unit_size=unit, date_booked=booked,
                guest_certificate=traveler, upgrade_status=upgrade,
                fk_owner=p_owner,touched_bool=True,points_required_for_reservation = pts)
            reservation.save()

        else:
            rsrv = Reservation.objects.filter(confirmation_number=conf).update(date_of_reservation = checkin,
                number_of_nights = nights,
                guest_certificate = traveler,
                upgrade_status = upgrade, touched_bool=True)







    def parseConfirmationPage(self, p_owner, p_confirmaion_numbers_pts_dict):
        time.sleep(3)
        columns = self.browser.find_elements_by_tag_name("td")

        columns_text = []
        for column in columns:
            columns_text.append(column.text)

        beg_slice_index = 1  # inclusive
        end_slice_index = 9  # non-inclusive

        rows = len(columns_text) / 9

        reservations = []

        for row_itterator in range( 0, int(rows) ):
            rsrv = self.parseConfirmationRow(columns_text[beg_slice_index:end_slice_index],
                p_owner, p_confirmaion_numbers_pts_dict)
            reservations.append(rsrv)
            beg_slice_index += 9
            end_slice_index += 9

    def getConfirmationPages(self, p_owner, p_confirmaion_numbers_pts_dict):
        more_pages_exist = True
        while more_pages_exist:
            time.sleep(2)
            self.parseConfirmationPage( p_owner, p_confirmaion_numbers_pts_dict)
            try:
                element = self.browser.find_element_by_link_text("Next")
                element.click()
            except:
                more_pages_exist = False




class Update:

    #static variables
    update_in_progress = False

    def updateCanceled():

        todays_date = datetime.today()
        future_reservations = Reservation.objects.filter(date_of_reservation__gte=todays_date)

        for i in range(0,len(future_reservations)):
            reservation = future_reservations[i]

            if(reservation.touched_bool==True):
                Reservation.objects.filter(id=reservation.id).update(canceled=False, touched_bool=False)
            else:
                Reservation.objects.filter(id=reservation.id).update(canceled=True, touched_bool=False)




    @login_required(redirect_field_name="/admin", login_url="/login/")
    def get(request):

        do_not_update_this_time = False

        if ( ScrapeWyndham.isOffHours() ):
            return HttpResponse(
                "<h1><center>You tried to update during off-hours, please try again after 7:00am</center></h1><br>" +
                "<h2><center>You can still view the views page, just cannot update until after 7:00am</h2></center>" )



        if( Update.update_in_progress):
            while( Update.update_in_progress):
                pass

            return redirect("/")

        else:
            Update.update_in_progress = True

            owners = Owner.objects.all()
            thread_array = []

            Reservation.objects.filter(points_required_for_reservation=-1).delete()

            for owner in owners:
                thread_array.append(Thread(target=handleOwner, args=(owner,)))

            while (thread_array != []):
                left_in_thread_array = len(thread_array)

                #run 3 threads at once or whatever is left in the array
                if(left_in_thread_array < 5):
                    threads_to_run_at_once = left_in_thread_array
                else:
                    threads_to_run_at_once = 5

                for i in range(0,threads_to_run_at_once):
                    thread_array[i].start()

                for i in range(0,threads_to_run_at_once):
                    thread_array[i].join()

                for i in range(0,threads_to_run_at_once):
                    thread_array.pop(0)


            Report.updateSummaries()

            Update.updateCanceled()

            application = ReservationManagerApplicationSettings(last_updated=datetime.now(), last_updated_by=request.user).save()



            Update.update_in_progress = False

            return redirect("/")

class View:

    @login_required(redirect_field_name="/admin", login_url="/login/")
    def get(request):
        usernames = []
        resorts = []
        unit_sizes = []
        travelers = []
        upgrades = []

        newest_date = ReservationManagerApplicationSettings.objects.all().order_by('-last_updated')
        newest_date = newest_date[0].last_updated
        print (newest_date)
        newest_date = newest_date + timedelta(hours=-4)
        newest_date = newest_date.strftime("%Y-%m-%d %H:%M:%S")

        updated_by = ReservationManagerApplicationSettings.objects.all().order_by('-last_updated')[0].last_updated_by

        if(last_updated_by==None):
            last_updated_by="WAM Admin"



        reservations = Reservation.objects.filter(date_of_reservation__gte=datetime.today())

        for reservation in reservations:
            usernames.append(reservation.fk_owner.username)

        for reservation in reservations:
            resorts.append(reservation.location)

        for reservation in reservations:
            unit_sizes.append(reservation.unit_size)

        for reservation in reservations:
            travelers.append(reservation.guest_certificate)

        for reservation in reservations:
            upgrades.append(reservation.upgrade_status)



        context = {
            "reservations" : reservations.order_by('date_of_reservation'),
            "usernames" : set(usernames),
            "resorts" : set(resorts),
            "unit_sizes" : set(unit_sizes),
            "travelers" : set(travelers),
            "upgrades" : set(upgrades),
            "last_updated" : str(newest_date),
            "updated_by" : str(updated_by)
        }

        return render( request, "main/index.html", context)

class Export:

    @login_required(redirect_field_name="/admin", login_url="/login/")
    def get(request):

        reservations = Reservation.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Description'] = 'attachment; filename="export.xls"'

        arr = []

        writer = csv.writer(response)
        arr.append("username")
        arr.append("location")
        arr.append("date_of_reservation")
        arr.append("number_of_nights")
        arr.append("unit_size")
        arr.append("confirmation_number")
        arr.append("points_required_for_reservation")
        arr.append("is_buyer_lined_up")
        arr.append("amount_paid")
        arr.append("date_booked")
        arr.append("upgrade_status")
        arr.append("guest_certificate")
        arr.append("canceled")
        writer.writerow(arr)
        arr = []
        for reservation in reservations:
            arr.append(reservation.fk_owner.username)
            arr.append(reservation.location)
            arr.append(reservation.date_of_reservation)
            arr.append(reservation.number_of_nights)
            arr.append(reservation.unit_size)
            arr.append(reservation.confirmation_number)
            arr.append(reservation.points_required_for_reservation)
            arr.append(reservation.is_buyer_lined_up)
            arr.append(reservation.amount_paid)
            arr.append(reservation.date_booked)
            arr.append(reservation.upgrade_status)
            arr.append(reservation.guest_certificate)
            arr.append(reservation.canceled)

            writer.writerow(arr)
            arr = []

        return response
