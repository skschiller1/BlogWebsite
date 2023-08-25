from django.db import models


# Create your models here.
class Airport(models.Model):
    name = models.CharField(max_length=155)
    callsign = models.CharField(max_length=5)

    lat1 = models.FloatField()
    lat2 = models.FloatField()
    lat3 = models.FloatField()
    latNS = models.CharField(max_length=1)

    long1 = models.FloatField()
    long2 = models.FloatField()
    long3 = models.FloatField()
    longEW = models.CharField(max_length=1)

    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    access = models.CharField(max_length=155)
    open_date = models.DateField(default=None, null=True)
    control_tower = models.CharField(max_length=5, default=None, null=True)

    FSJA = models.FloatField(blank=True, default=None, null=True)
    FS100 = models.FloatField(blank=True, default=None, null=True)
    SSJA = models.FloatField(blank=True, default=None, null=True)
    SS100 = models.FloatField(blank=True, default=None, null=True)
    PSJA = models.FloatField(blank=True, default=None, null=True)
    PS100 = models.FloatField(blank=True, default=None, null=True)
