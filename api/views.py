import logging

import django_filters.rest_framework

from rest_framework import filters
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from .permissions import IsForbidden, SalesPermissions, EventPermissions


logger = logging.getLogger(__name__)


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
            permission_classes = [SalesPermissions]
        else:
            permission_classes = [IsForbidden]

        return [permission() for permission in permission_classes]

    filter_backends = [filters.SearchFilter,
                    django_filters.rest_framework.DjangoFilterBackend,
                    filters.OrderingFilter]
    search_fields = ["company_name", "email", "first_name", "id", "last_name",
                        "mobile_number", "phone_number", "sales_contact"]
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
            permission_classes = [SalesPermissions]
        else:
            permission_classes = [IsForbidden]

        return [permission() for permission in permission_classes]

    filter_backends = [filters.SearchFilter,
                    django_filters.rest_framework.DjangoFilterBackend,
                    filters.OrderingFilter]
    search_fields = ["sales_contact", "client", "client__email", "status"]
    filterset_fields = ['date_created', 'date_updated', 'sales_contact',
                        'payment_due', "status", "client", "client__email"]
    ordering_fields = ['id', 'amount', 'date_created', 'date_updated',
                        'sales_contact', "client", "client_email", "payment_due"]

    def perform_create(self, serializer):
        client = Client.objects.get(id=serializer.validated_data['client'].id)
        if client.sales_contact.id != self.request.user.id:
            logger.warning("Attempt to create a contract for a client with another sale support.")
            raise PermissionDenied({"message": "You can only create contracts for your own clients."})
        else:
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
    search_fields = ["support_contact", "client", "status", "event_date",
                    "client__email", "client__sales_contact__id"]
    filterset_fields = ['date_created', 'date_updated', 'support_contact',
                        "status", "event_date", "notes", "client__email",
                        "client__sales_contact__id"]
    ordering_fields = ['id', 'date_created', 'date_updated', 'support_contact',
                        "client", "attendees", "event_date", "client__email",
                        "client__sales_contact__id"]

    def perform_create(self, serializer):
        client = Client.objects.get(id=serializer.validated_data['client'].id)
        if client.sales_contact.id != self.request.user.id:
            logger.warning("Attempt to create an event for a client with another sale support.")
            raise PermissionDenied({"message": "You don't have permission to create this event."})

        else:
            event = serializer.save()
