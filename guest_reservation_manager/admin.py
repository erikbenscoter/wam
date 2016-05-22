from django.contrib import admin

#from .models import Owner
from .models import GuestReservation
#from .models import OwnerPointsManagerApplicationSettings

# Register your models here.
# admin.site.register( Owner )
admin.site.register(GuestReservation)
#admin.site.register(OwnerPointsManagerApplicationSettings)
