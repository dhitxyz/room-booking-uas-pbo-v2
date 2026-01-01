from django.contrib import admin
from .models import Booking, Room, Facility

admin.site.register(Booking)
admin.site.register(Facility)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ('facilities',)
