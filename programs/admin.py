from django.contrib import admin
from .models import Airport


class AirportAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Airport, AirportAdmin)
