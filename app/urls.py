from django.urls import path
from .views import home, room_list, booking_create, booking_list
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('room/', room_list, name='room_list'),
    path('create/<int:room_id>/', booking_create, name='booking_create'),
    path('list/', booking_list, name='booking_list'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
