from django.contrib import admin

#from .models import Owner
from .models import guest_reservation
#from .models import OwnerPointsManagerApplicationSettings

# Register your models here.
# admin.site.register( Owner )
admin.site.register(guest_reservation)
#admin.site.register(OwnerPointsManagerApplicationSettings)
