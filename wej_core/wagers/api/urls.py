# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/participants/', views.ParticipantList.as_view(), name='participant-list'),
    path('api/participants/<int:pk>/', views.ParticipantDetail.as_view(), name='participant-detail'),
    path('api/wagers/', views.WagerList.as_view(), name='wager-list'),
    path('api/wagers/<int:pk>/', views.WagerDetail.as_view(), name='wager-detail'),
    path('api/wager-requests/', views.WagerRequestList.as_view(), name='wager-request-list'),
    path('api/wager-requests/<int:pk>/', views.WagerRequestDetail.as_view(), name='wager-request-detail'),
]