from django.urls import path

from api import views

urlpatterns = [
    path('clients/', views.clients),
    path('snippets/<int:pk>', views.client_details),
]
