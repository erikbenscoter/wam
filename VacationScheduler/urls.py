"""VacationScheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from guest_reservation_manager.views import makeBrandNewWish
from guest_reservation_manager.views import makeNewWish1
from guest_reservation_manager.views import makeNewWish2
from guest_reservation_manager.views import makeNewWish3
from guest_reservation_manager.views import commitLink
from guest_reservation_manager.views import removeLink
from guest_reservation_manager.views import summarizeWish
from guest_reservation_manager.views import showLinkedWishes
from guest_reservation_manager.views import showUnLinkedWishes

from owners_point_manager.views import Update as update_owners_points_update
from owners_point_manager.views import View as update_owners_points_view
from reservation_manager.views import Export
from reservation_manager.views import Update
from reservation_manager.views import View
from monthly_summary.views import Report
from monthly_summary.views import GenerateReport
from login import views as login_views
from upgrade_recognition import views as upgrade_recognition_views
from VacationScheduler.custom_startup import setUpToRunHourly
from db_manager.views import DBManager
from guest_reservation_manager.views import View as guest_reservations_views




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^update/', Update.get),
    url(r'^export/', Export.get),
    url(r'^report/(?P<p_owner_username>.*)/(?P<p_month>[0-9][0-9]?)/(?P<p_year>[0-9][0-9][0-9][0-9])', Report.get),
    url(r'^save_payment/(?P<p_check_number>[0-9]*)/(?P<p_amt_paid>[0-9]*.?[0-9]*)/(?P<p_monthly_summary>.*)', Report.savePayment),

    url(r'^set_is_saved_for_owner/(?P<reservation_id>[0-9]*)', Report.setIsSavedForOwner),

    url(r'^generate_report/', GenerateReport.get),
	url(r'^login/$', login_views.login_user),
	url(r'^$', View.get),

    url(r'^guest/wish/new/$',makeBrandNewWish),
    url(r'^guest/makeWish/(?P<wish_id>[0-9]*)$',makeNewWish1),
    url(r'^guest/makeWish2/(?P<wish_id>[0-9]*)$',makeNewWish2),
    url(r'^guest/makeWish3/(?P<wish_id>[0-9]*)$',makeNewWish3),
    url(r'^guest/makeWish3/link/(?P<reservation_id>[0-9]*)/(?P<wish_id>[0-9]*)$',commitLink),
    url(r'^guest/wish/remove/(?P<reservation_id>[0-9]*)/(?P<wish_id>[0-9]*)$',removeLink),
    url(r'^guest/wish/dashboard/', summarizeWish),
    url(r'^guest/wish/view/fulfilledWishes/', showLinkedWishes),
    url(r'^guest/wish/view/unFulfilledWishes/', showUnLinkedWishes),


    url(r'^guestreservationview/', guest_reservations_views.get),

    url(r'^updatepoints/', update_owners_points_update.get),
    url(r'^updatepointsview/', update_owners_points_view.get),
    url(r'^upgrades/', upgrade_recognition_views.main),
    url(r'^dumpdata/', DBManager.dumpData),
    url(r'^viewbackups/', DBManager.viewUpdates)


]
# this adds the cron
# setUpToRunHourly()
