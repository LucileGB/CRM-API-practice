from django.urls import path
from django.views.generic import RedirectView

from api import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('clients/', views.clients, name='clients'),
    path('clients/<int:pk>', views.client_details),
    path('contracts/', views.contracts, name='contracts'),
    path('contracts/<int:pk>', views.contract_details),
    path('events/', views.events, name='events'),
    path('events/<int:pk>', views.event_details),
]
