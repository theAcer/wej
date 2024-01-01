# wagers/urls.py
from django.urls import path, include
from . import views

app_name = 'wagers'

urlpatterns = [
    path('', include('wagers.api.urls')),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('place_wager/<int:pk>/', views.PlaceWagerView.as_view(), name='place_wager'),
    path('create_event/', views.EventCreateView.as_view(), name='create_event'),

]