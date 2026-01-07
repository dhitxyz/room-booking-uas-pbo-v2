from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date
from django.db import models

from .models import Room, Booking
from .forms import BookingForm
from .views import validate_booking, booking_success_message

@login_required
def home(request):
    today = timezone.localdate()
    total_rooms = Room.objects.count()
    booking_today = Booking.objects.filter(user=request.user, date=today)
    total_booking_today = booking_today.count()
    waiting_approval = Booking.objects.filter(
        user=request.user,
        status='menunggu'
    )
    
    total_waiting_approval = waiting_approval.count()
    
    return render(request, 'index.html', {
        'total_rooms' : total_rooms,
        'booking' : booking_today,
        'total_booking_today' : total_booking_today,
        'total_waiting_approval' : total_waiting_approval
    })

@login_required
def room_list(request):
    rooms = Room.objects.all().order_by('floor')
    search_query = request.GET.get('search', '')

    if search_query:
        rooms = rooms.filter(
            models.Q(name__icontains=search_query) |
            models.Q(floor__icontains=search_query)
        )

    today = date.today()
    now_time = timezone.localtime().time()
    room_status = []

    for room in rooms:
        bookings = Booking.objects.filter(
            room=room,
            status__in=['menunggu', 'disetujui']
        ).filter(
            models.Q(date__gt=today) |
            models.Q(date=today, end_time__gte=now_time)
        ).order_by('date', 'start_time')

        user_has_booking = False
        if request.user.is_authenticated:
            user_has_booking = bookings.filter(user=request.user).exists()

        room_status.append({
            'room': room,
            'bookings': bookings,
            'user_has_booking': user_has_booking
        })

    return render(request, 'room_list.html', {
        'room_status': room_status,
        'search_query': search_query
    })

@login_required
def booking_create(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            error_message = validate_booking(form, room)
            if error_message:
                messages.error(request, error_message)
                return redirect('room_list')

            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.status = 'menunggu'
            booking.save()

            booking_success_message(request)
            return redirect('booking_list')

        for field, errors in form.errors.items():
            messages.error(request, " ".join(errors))
        return redirect('room_list')

    return redirect('room_list')

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-start_time')
    return render(request, 'booking_list.html', {'bookings': bookings})
