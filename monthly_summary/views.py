from django.shortcuts import render, redirect
from reservation_manager.models import Reservation
from reservation_manager.models import Owner
from monthly_summary.models import MonthlyReport
from datetime import datetime
from django.utils import timezone

# Create your views here.
class GenerateReport:

    def get(request):

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


        context = {
            "owners" : owners,
            "months" : months,
            "years" : years


        }
        return render(request,"generate_report/index.html", context)

class Report:
    def updateSummaries(self):

        all_reservations = Reservation.objects.filter(fk_monthly_report__isnull=True)

        for reservation in all_reservations:
            month = reservation.date_of_reservation.month
            year = reservation.date_of_reservation.year
            owner = reservation.fk_owner

            matching_summaries = list(MonthlyReport.objects.all())

            matching_summary = "none found"

            if(matching_summaries):
                for summary in matching_summaries:
                    if(summary and summary.owner == owner and summary.month == month and summary.year == year):
                        matching_summary = summary



            if( matching_summary == "none found" ):
                new_monthly_report = MonthlyReport()
                new_monthly_report.save()

                reservation.fk_monthly_report = new_monthly_report
                reservation.save()
            else:
                reservation.fk_monthly_report = matching_summaries[0]
                reservation.save()

    def get(request, p_owner_username, p_year, p_month):

        reservations = Reservation.objects.filter( date_of_reservation__year=p_year,
                                    date_of_reservation__month=p_month).order_by('-date_of_reservation')
        owner = Owner.objects.get(username=p_owner_username)

        monthly_summaries = MonthlyReport.objects.all()

        desired_summary = None

        for monthly_summary in monthly_summaries:
            if(monthly_summary.owner.username == p_owner_username):
                if(int(monthly_summary.year) == int(p_year)):
                    if(int(monthly_summary.month) == int(p_month)):
                        desired_summary = monthly_summary

        context = {
            "reservations" : reservations,
            "owner" : owner,
            "year" : p_year,
            "month" : p_month,
            "monthly_summary" : desired_summary
        }
        return render(request, "report/index.html",context)

    def savePayment(request,p_check_number, p_amt_paid, p_monthly_summary):
        summary = MonthlyReport.objects.filter(id=p_monthly_summary)
        summary.update(check_number = p_check_number, amount_paid=p_amt_paid, date_paid=datetime.now())

        month = summary[0].month
        year = summary[0].year
        username = summary[0].owner.username

        return redirect('/report/'+str(username)+"/"+str(month)+"/"+str(year))
