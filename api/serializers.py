from django.utils import timezone
from rest_framework import serializers

from .models import Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number',
                'mobile_number', 'company_name', 'date_created', 'date_updated',
                'sales_contact']

        extra_kwargs = {
            'id': {'read_only': True},
            'date_created': {'read_only': True},
            }

    def create(self, validated_data):
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first name', instance.first_name)
        instance.last_name = validated_data.get('last name', instance.last_name)
        instance.phone_number = validated_data.get('phone number', instance.phone_number)
        instance.mobile_number = validated_data.get('mobile number', instance.mobile_number)
        instance.company_name = validated_data.get('company name', instance.company_name)
        instance.date_updated = default=timezone.now
        instance.sales_contact = validated_data.get('sales contact', instance.sales_contact)

        instance.save()
        return instance

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'sales_contact', 'client', 'date_created', 'date_updated',
                'status', 'amount', 'payment_due'
                ]

        extra_kwargs = {
            'id': {'read_only': True},
            'date_created': {'read_only': True},
            }

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sales_contact = validated_data.get('sales contact', instance.sales_contact)
        instance.client = validated_data.get('client', instance.client)
        instance.date_updated = default=timezone.now
        instance.status = validated_data.get('status', instance.status)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.payment_due = validated_data.get('payment due', instance.payment_due)

        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'client', 'date_created', 'date_updated', 'support_contact',
                'status', 'attendees', 'event_date', 'notes'
                ]

        extra_kwargs = {
            'id': {'read_only': True},
            'date_created': {'read_only': True},
            }

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.client = validated_data.get('client', instance.client)
        instance.date_updated = default=timezone.now
        instance.support_contact = validated_data.get('support contact', instance.support_contact)
        instance.status = validated_data.get('status', instance.status)
        instance.attendees = validated_data.get('attendees', instance.attendees)
        instance.event_date = validated_data.get('event date', instance.event_date)
        instance.note = validated_data.get('note', instance.note)

        instance.save()
        return instance
