from django.utils import timezone
from datetime import date
from django.contrib import messages
from .models import Booking

def booking_success_message(request):
    messages.success(request, 'Booking berhasil dibuat! Menunggu persetujuan admin.')

def validate_booking(form, room):
    cleaned_data = form.cleaned_data
    booking_date = cleaned_data.get('date')
    start = cleaned_data.get('start_time')
    end = cleaned_data.get('end_time')

    # Cek jam selesai > jam mulai
    if start and end and start >= end:
        return "Jam selesai harus lebih besar dari jam mulai"

    # Cek tanggal lewat
    if booking_date < date.today():
        return "Tidak bisa booking di tanggal yang sudah lewat"

    # Cek jika booking hari ini, waktu sudah lewat
    if booking_date == timezone.localdate() and start <= timezone.localtime().time():
        return "Waktu booking sudah lewat"

    # Cek konflik booking
    conflicts = Booking.objects.filter(
        room=room,
        date=booking_date,
        status__in=['menunggu', 'disetujui'],
        start_time__lt=end,
        end_time__gt=start
    )

    if conflicts.exists():
        conflicting = conflicts.first()
        return (
            f"Ruangan sudah di booking pada tanggal {conflicting.date}, "
            f"{conflicting.start_time} - {conflicting.end_time}"
        )

    return None
