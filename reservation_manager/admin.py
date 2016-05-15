from django.contrib import admin

from .models import Owner
from .models import Reservation
from .models import ReservationManagerApplicationSettings

# Register your models here.
admin.site.register( Owner )
admin.site.register( Reservation )
admin.site.register( ReservationManagerApplicationSettings )
