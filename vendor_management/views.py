from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status

class VendorListCreateView(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'on_time_delivery_rate': serializer.data['on_time_delivery_rate'],
                 'quality_rating_avg': serializer.data['quality_rating_avg'],
                 'average_response_time': serializer.data['average_response_time'],
                 'fulfillment_rate': serializer.data['fulfillment_rate']})
        # return Response(serializer.data['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate'])

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Set acknowledgment date
        instance.acknowledgment_date = request.data.get('acknowledgment_date', timezone.now())
        instance.save()

        # Calculate average response time
        response_times = PurchaseOrder.objects.filter(
            vendor=instance.vendor, acknowledgment_date__isnull=False
        ).values_list('acknowledgment_date', 'issue_date')

        if response_times:
            # Calculate total seconds and then get the average
            total_seconds = sum(
                abs((ack_date - issue_date).total_seconds())
                for ack_date, issue_date in response_times
            )
            average_response_time = total_seconds / len(response_times)
        else:
            # Avoid division by zero if there are no response times
            average_response_time = 0

        # Update the vendor's average response time
        instance.vendor.average_response_time = average_response_time
        instance.vendor.save()

        return Response({'acknowledgment_date': instance.acknowledgment_date})


