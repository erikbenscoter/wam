import csv
import re
import time

from datetime import datetime
from datetime import timedelta

from django.core.mail import send_mail

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from .models import Owner
from .models import Owners_Points_Status
from .models import OwnerPointsManagerApplicationSettings


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

        bad_values = ["Travel From", "Expiration", "Points Description", "Points Available", "Housekeeping\nAvailable"]

        for column_text in columns_text:
            if not (column_text in bad_values):
                tmp.append(column_text)

        columns_text = []

        for element in tmp:
            columns_text.append(element)

        tmp = []

        beg_slice_index = 0  # inclusive
        end_slice_index = 6  # non-inclusive
        rows = len(columns_text) / 5

        ownerspointsstatus = []

        for row_itterator in range(0, int(rows)):
            points = self.parsePointStatusRow(columns_text[beg_slice_index:end_slice_index],
                                              p_owner)
            ownerspointsstatus.append(points)

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

            src = scrape_wyndham.parsePointStatusPage(owner)
            time.sleep(2)
            scrape_wyndham.logout()

        scrape_wyndham.browser.close()

        opmas = OwnerPointsManagerApplicationSettings.objects.all()

        for opma in opmas:
            opma.delete()

        opma = OwnerPointsManagerApplicationSettings(last_updated = datetime.now())
        opma.save()

#        mail_admins(
#            'WAM Owner Point Manager',
#            'Update has run.',
#            connection=None,
#            html_message=None
#        )


#        send_mail (
#            'WAM Owner Point Manager',
#            'Update has run.',
#            'Glenn.Benscoter@gmail.com',
#            ['Glenn.Benscoter@gmail.com'],
#            fail_silently=False
#        )

        return redirect("/updatepointsview")

class View:
    def get(request):

        usernames = []
        travelfrom = []
        expiration = []
        pointsdesc = []
        pointsavail = []
        housekeepingavail = []

        newest_date = OwnerPointsManagerApplicationSettings.objects.all()
        newest_date = newest_date[0].last_updated

        newest_date = newest_date + timedelta(hours=-4)
        newest_date = newest_date.strftime("%Y-%m-%d %H:%M:%S")

        Owners_Points_Statuss = Owners_Points_Status.objects.order_by('Travel_From','Expiration')

        for ownerspointsstatus in Owners_Points_Statuss:
            usernames.append(ownerspointsstatus.fk_owner.username)

        for ownerspointsstatus in Owners_Points_Statuss:
            travelfrom.append(ownerspointsstatus.Travel_From)

        for ownerspointsstatus in Owners_Points_Statuss:
            expiration.append(ownerspointsstatus.Expiration)

        for ownerspointsstatus in Owners_Points_Statuss:
            pointsdesc.append(ownerspointsstatus.Points_Description)

        for ownerspointsstatus in Owners_Points_Statuss:
            pointsavail.append(ownerspointsstatus.Points_Available)

        for ownerspointsstatus in Owners_Points_Statuss:
            housekeepingavail.append(ownerspointsstatus.Housekeeping_Available)

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
