from django.contrib import admin

from .models import Owner
from .models import Owners_Points_Status
from .models import OwnerPointsManagerApplicationSettings

# Register your models here.
# admin.site.register( Owner )
admin.site.register(Owners_Points_Status)
admin.site.register(OwnerPointsManagerApplicationSettings)
