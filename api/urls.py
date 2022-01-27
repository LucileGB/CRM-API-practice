from django.urls import include, path

from api import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='clients')
router.register(r'contracts', views.ContractViewSet, basename='contracts')
router.register(r'events', views.EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
]
