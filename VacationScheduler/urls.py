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

from owners_point_manager.views import Update as update_owners_points
from owners_point_manager.views import View as update_owners_points_view
from reservation_manager.views import Export
from reservation_manager.views import Update
from reservation_manager.views import View

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^update/', Update.get),
    url(r'^export/', Export.get),
    url(r'^$', View.get),
    url(r'^updatepoints/', update_owners_points.get),
    url(r'^updatepointsview/', update_owners_points_view.get),

]
