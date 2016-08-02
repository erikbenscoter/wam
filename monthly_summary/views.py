from django.shortcuts import render, redirect
from reservation_manager.models import Reservation
from reservation_manager.models import Owner
from monthly_summary.models import MonthlyReport
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
class GenerateReport:

    @login_required(redirect_field_name="/admin", login_url="/login/")
    def get(request, error=0):

        monthly_summaries = MonthlyReport.objects.all()

        months = []
        years = []
        owners = []

        for monthly_summary in monthly_summaries:
            months.append(monthly_summary.month)
            years.append(monthly_summary.year)
            owners.append(monthly_summary.owner)

        years = set(years)
        years = list(years)

        months = set(months)
        months = list(months)

        owners = set(owners)
        owners = list(owners)

        if(error==0):
            error=None


        context = {
            "error" : error,
            "owners" : owners,
            "months" : months,
            "years" : years


        }
        return render(request,"generate_report/index.html", context)

class Report:

    def getMonthName( p_month_number):
#
#               CHANGE A MONTH NUMBER TO A monthname
#
        switcher = {
            1: "January",
            2: "Febuary",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }

        return switcher.get(p_month_number,"no month")

    def removeExcessSummaries():
        all_reports = MonthlyReport.objects.all()

        for report in all_reports:
            if(report.owner is None):
                report.delete()


    def updateSummaries():

        all_reservations = Reservation.objects.filter(fk_monthly_report__isnull=True, canceled=False)

        for reservation in all_reservations:


            if(not (reservation.is_held_for_owner)):

                month = reservation.date_of_reservation.month
                year = reservation.date_of_reservation.year
                owner = reservation.fk_owner

                matching_summaries = list(MonthlyReport.objects.all())

                matching_summary = "none found"

                for summary in matching_summaries:
                    if(summary and summary.owner == owner and summary.month == month and summary.year == year):
                        matching_summary = summary

                if( matching_summary == "none found" ):
                    new_monthly_report = MonthlyReport()
                    new_monthly_report.save()

                    reservation.fk_monthly_report = new_monthly_report
                    reservation.save()
                else:
                    reservation.fk_monthly_report = matching_summary
                    reservation.save()

        Report.removeExcessSummaries()

    @login_required(redirect_field_name="/admin", login_url="/login/")
    def get(request, p_owner_username, p_year, p_month):

        all_reports = list(MonthlyReport.objects.all())
        all_reservations = list(Reservation.objects.all().order_by('date_of_reservation'))
        matching_reservations = []

        desired_summary = None

        for report in all_reports:
            if(int(report.month) == int(p_month) and int(report.year) == int(p_year) and str(report.owner.username) == str(p_owner_username)):
                desired_summary = report

        if(desired_summary is None):
            return GenerateReport.get(request,1)

        for reservation in all_reservations:
            if(reservation.fk_monthly_report):
                if(reservation.fk_monthly_report.id):
                    if(str(reservation.fk_monthly_report.id) == str(desired_summary.id)):
                        if(not (reservation.is_held_for_owner)):
                            if(not (reservation.canceled)):
                                matching_reservations.append(reservation)

        reservations = matching_reservations

        month_name = Report.getMonthName(int(p_month))

        context = {
            "reservations" : reservations,
            "owner" : desired_summary.owner,
            "year" : p_year,
            "month" : p_month,
            "monthname" : month_name,
            "monthly_summary" : desired_summary
        }
        return render(request, "report/index.html",context)

    @login_required(redirect_field_name="/admin", login_url="/login/")
    def savePayment(request,p_check_number, p_amt_paid, p_monthly_summary):
        summary = MonthlyReport.objects.filter(id=p_monthly_summary)
        summary.update(check_number = p_check_number, amount_paid=p_amt_paid, date_paid=datetime.now())

        month = summary[0].month
        year = summary[0].year
        username = summary[0].owner.username

        return redirect('/report/'+str(username)+"/"+str(month)+"/"+str(year))


    def setIsSavedForOwner(request, reservation_id):
        reservation = Reservation.objects.filter(id=reservation_id)
        reservation.update(reason_on_hold="OWN")

        month       = reservation[0].fk_monthly_report.month
        year        = reservation[0].fk_monthly_report.year
        username    = reservation[0].fk_monthly_report.owner.username

        return redirect('/report/'+str(username)+"/"+str(month)+"/"+str(year))
