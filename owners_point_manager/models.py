from django.db import models

from reservation_manager.models import Owner

TRUE_OR_FALSE = (
    (1, "True"),
    (0, "False")
)


# Create your models here.
class Owners_Points_Status(models.Model):
    fk_owner = models.ForeignKey(Owner)
    Travel_From = models.DateField(blank=True, null=True)
    Expiration = models.DateField(blank=True, null=True)
    Points_Description = models.CharField(blank=True, null=True, max_length=20)
    Points_Available = models.IntegerField(blank=True, null=True)
    Housekeeping_Available = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.fk_owner.username) + "   " + str(self.Travel_From) + " , " + str(self.Expiration) + " , " + str(
            self.Points_Available)

    def __unicode__(self):
        return str(self.fk_owner.username) + "   " + str(self.Travel_From) + " , " + str(self.Expiration) + " , " + str(
            self.Points_Available)
