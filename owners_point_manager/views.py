import csv
import re
import time
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from .models import Owner
from .models import Owners_Points_Status
from .models import OwnerPointsManagerApplicationSettings
from datetime import timedelta



# Create your views here.
class ScrapeWyndham:
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.get("https://www.myclubwyndham.com/ffr/index.do")

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

    def getToPointStatusPage(self):
        element = self.browser.find_element_by_link_text("MY MEMBERSHIP")

        builder = ActionChains(self.browser)
        builder.move_to_element(element)
        builder.perform()

        element = self.browser.find_element_by_link_text("Point Status")
        element.click()

    def parsePointStatusPage(self, p_owner):

        print("xxxin parsePointsStatusPage", " second part")
# time.sleep(30)
        columns = self.browser.find_elements_by_tag_name("td")

        columns_text = []
        for column in columns:
            columns_text.append(column.text)

        first_travelfrom_flag_found = False

        tmp = []

        for column_text in columns_text:
            if str(column_text).strip() == "Travel From":
                first_travelfrom_flag_found = True
            if first_travelfrom_flag_found:
                tmp.append(column_text)

        columns_text = []
        for element in tmp:
            columns_text.append(element)

        tmp = []
        print("columns text after cleanig out ")
        for column_text in columns_text:
            print(str(column_text).encode("utf-8"))

        bad_values = ["Travel From", "Expiration", "Points Description", "Points Available", "Housekeeping\nAvailable"]
        print(bad_values)

        for column_text in columns_text:
            if not (column_text in bad_values):
                tmp.append(column_text)

        columns_text = []

        for element in tmp:
            columns_text.append(element)

        tmp = []

        print("columns text after cleanig out ")
        for column_text in columns_text:
            print(str(column_text).encode("utf-8"))

        beg_slice_index = 0  # inclusive
        end_slice_index = 6  # non-inclusive
        rows = len(columns_text) / 5

        ownerspointsstatus = []

        for row_itterator in range(0, int(rows)):
            points = self.parsePointStatusRow(columns_text[beg_slice_index:end_slice_index],
                                              p_owner)
            ownerspointsstatus.append(points)
            print("ownerspointsstatus at 123 ", ownerspointsstatus)
            beg_slice_index += 5
            end_slice_index += 5

    def parsePointStatusRow(self, p_pointstatusrow_text, p_owner):
        #
        #   parse a given point status row for an owner and save it to db
        #
        travelfrom = p_pointstatusrow_text[0]
        expiration = p_pointstatusrow_text[1]
        pointsdescription = p_pointstatusrow_text[2]
        pointsavailable = p_pointstatusrow_text[3]
        housekeepingavailable = p_pointstatusrow_text[4]

        print(travelfrom)
        print(expiration)


        travelfrom = datetime.strptime(str(travelfrom).strip(), '%b %d, %Y')
        expiration = datetime.strptime(str(expiration).strip(), '%b %d, %Y')

        travelfrom = (str(travelfrom).split(' ')[0])
        expiration = (str(expiration).split(' ')[0])

        pointsavailable = pointsavailable.strip()
        housekeepingavailable = housekeepingavailable.strip()
        travelfrom = travelfrom.strip()
        expiration = expiration.strip()

        pointsavailable = pointsavailable.replace(",", "")
        housekeepingavailable = housekeepingavailable.replace(",", "")

        ownerspointsstatus = Owners_Points_Status(Travel_From=travelfrom, Expiration=expiration,
                                                  Points_Description=pointsdescription,
                                                  Points_Available=pointsavailable,
                                                  Housekeeping_Available=housekeepingavailable, fk_owner=p_owner)
        ownerspointsstatus.save()


class Update:
    def get(request):
        Owners_Points_Statuss = Owners_Points_Status.objects.all()

        for ownerspointsstatus in Owners_Points_Statuss:
            ownerspointsstatus.delete()

        owners = Owner.objects.all()
        scrape_wyndham = ScrapeWyndham()

        for owner in owners:
            time.sleep(2)
            scrape_wyndham.login(owner.username, owner.password)
            time.sleep(2)
            scrape_wyndham.getToPointStatusPage()
            time.sleep(2)
            #           src = scrape_wyndham.getConfirmationPages(owner, confirmation_numbers)
            src = scrape_wyndham.parsePointStatusPage(owner)
            time.sleep(2)
            scrape_wyndham.logout()

        scrape_wyndham.browser.close()

        opmas = OwnerPointsManagerApplicationSettings.objects.all()

        for opma in opmas:
            opma.delete()

        opma = OwnerPointsManagerApplicationSettings(last_updated = datetime.now())
        opma.save()

        return redirect("/updatepointsview")

class View:
    def get(request):
        print("at top of View")
        usernames = []
        travelfrom = []
        expiration = []
        pointsdesc = []
        pointsavail = []
        housekeepingavail = []

        newest_date = OwnerPointsManagerApplicationSettings.objects.all()
        newest_date = newest_date[0].last_updated
        print (newest_date)
        newest_date = newest_date + timedelta(hours=-4)
        newest_date = newest_date.strftime("%Y-%m-%d %H:%M:%S")

        Owners_Points_Statuss = Owners_Points_Status.objects.order_by('Travel_From','Expiration')

        for ownerspointsstatus in Owners_Points_Statuss:
            usernames.append(ownerspointsstatus.fk_owner.username)


        for ownerspointsstatus in Owners_Points_Statuss:
            travelfrom.append(ownerspointsstatus.Travel_From)
            print("travel from = ", travelfrom)
        print("travel from at 297", travelfrom)

        for ownerspointsstatus in Owners_Points_Statuss:
            expiration.append(ownerspointsstatus.Expiration)
            print("expiration = ", expiration)

        for ownerspointsstatus in Owners_Points_Statuss:
            pointsdesc.append(ownerspointsstatus.Points_Description)
            print("pointsdesc = ", pointsdesc)

        for ownerspointsstatus in Owners_Points_Statuss:
            pointsavail.append(ownerspointsstatus.Points_Available)
            print("pointsavail = ", pointsavail)

        for ownerspointsstatus in Owners_Points_Statuss:
            housekeepingavail.append(ownerspointsstatus.Housekeeping_Available)
            print("housekeepingavail = ", housekeepingavail)

        context = {
            "ownerspointsstatuss": Owners_Points_Statuss,
            "usernames": set(usernames),
            "travelfrom": set(travelfrom),
            "expiration": set(expiration),
            "pointsdesc": set(pointsdesc),
            "pointsavail": set(pointsavail),
            "housekeepingavail": set(housekeepingavail),
            "last_updated" : str(newest_date)
        }

        return render(request, "owner_points/index.html", context)


class Export:
    def get(request):
        newest = Reservation.objects.all().latest("touched").touched
        reservations = Reservation.objects.all().filter(touched=newest)

        response = HttpResponse(content_type='text/csv')
        response['Content-Description'] = 'attachment; filename="export.xlsx"'

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
        arr.append("touched")
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
            arr.append(reservation.touched)

            writer.writerow(arr)
            arr = []

        return response
