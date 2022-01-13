from django.urls import path

from api import views

urlpatterns = [
    path('clients/', views.clients, name='clients'),
    path('clients/<int:pk>', views.client_details),
]
