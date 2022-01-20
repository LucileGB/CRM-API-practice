import logging

import django_filters.rest_framework

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status, generics, filters
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from .permissions import IsForbidden, IsSales, EventPermissions
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request, format=None):
    return Response({
        'clients': reverse('clients', request=request, format=format),
        'contracts': reverse('contracts', request=request, format=format),
        'events': reverse('events', request=request, format=format),
    })


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'create':
            permission_classes = [IsSales]
        else:
            print("bleeeeh")
            logging.info(f"Attempted unauthorized access: {self.action}")

            permission_classes = [IsForbidden]

        return [permission() for permission in permission_classes]

    filter_backends = [filters.SearchFilter,
                    django_filters.rest_framework.DjangoFilterBackend,
                    filters.OrderingFilter]
    search_fields = ["company_name", "email", "first_name", "id", "last_name",
                        "mobile_number", "phone_number"]
    filterset_fields = ['date_created', 'date_updated', 'sales_contact']
    ordering_fields = ['id', 'last_name', 'email', 'company_name',
                        'date_created', 'date_updated', 'sales_contact']

    def perform_create(self, serializer):
        client = serializer.save(sales_contact=self.request.user)

class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'create':
            permission_classes = [IsSales]
        else:
            logging.info(f"Attempted unauthorized access: {self.action} in Contract")
            permission_classes = [IsForbidden]

        return [permission() for permission in permission_classes]

    filter_backends = [filters.SearchFilter,
                    django_filters.rest_framework.DjangoFilterBackend,
                    filters.OrderingFilter]
    search_fields = ["sales_contact", "client", "status"]
    filterset_fields = ['date_created', 'date_updated', 'sales_contact',
                        "status",]
    ordering_fields = ['id', 'amount', 'date_created', 'date_updated', 'sales_contact',
                        "client", "payment_due"]

    def perform_create(self, serializer):
        contract = serializer.save(sales_contact=self.request.user)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'create':
            permission_classes = [EventPermissions]
        else:
            permission_classes = [IsForbidden]

        return [permission() for permission in permission_classes]
    filter_backends = [filters.SearchFilter,
                    django_filters.rest_framework.DjangoFilterBackend,
                    filters.OrderingFilter]
    search_fields = ["support_contact", "client", "status"]
    filterset_fields = ['date_created', 'date_updated', 'support_contact',
                        "status", "notes"]
    ordering_fields = ['id', 'date_created', 'date_updated', 'support_contact',
                        "client", "attendees", "event_date"]
