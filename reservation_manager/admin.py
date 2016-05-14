from django.contrib import admin

from .models import Owner
from .models import Reservation

# Register your models here.
admin.site.register( Owner )
admin.site.register( Reservation )
