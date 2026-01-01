from django.db import models
from django.contrib.auth.models import User

class Facility(models.Model):
    name = models.CharField(max_length=100)
    icon_svg = models.TextField()

    def __str__(self):
        return self.name
    
class Room(models.Model):
    name = models.CharField(max_length=100)
    floor = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    facilities = models.ManyToManyField(Facility, blank=True, related_name='rooms')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.floor}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('menunggu', 'Menunggu'), ('disetujui', 'Disetujui'), ('ditolak', 'Ditolak')],
        default='menunggu'
    )

    def __str__(self):
        return f"{self.user.username} - {self.room.name}"
