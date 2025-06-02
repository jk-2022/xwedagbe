from django.contrib import admin

from .models import CustomUser, DemandeDemarcheur

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(DemandeDemarcheur)