from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Vendor, PurchaseOrder
from django.utils import timezone
import datetime

class VendorAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Test Vendor')

    def test_create_vendor(self):
        url = reverse('vendor-list')
        data = {'name': 'New Vendor'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        data = {'name': 'Updated Vendor'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, 'Updated Vendor')

    def test_delete_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PurchaseOrderAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Test Vendor')
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            issue_date=timezone.now(),
            order_number='PO123'
        )

    def test_create_purchase_order(self):
        url = reverse('purchaseorder-list')
        data = {
            'vendor': self.vendor.pk,
            'order_number': 'PO124',
            'issue_date': timezone.now()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_purchase_order(self):
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk})
        data = {'order_number': 'PO125'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AcknowledgePurchaseOrderAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Test Vendor')
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            issue_date=timezone.now(),
            order_number='PO123'
        )

    def test_acknowledge_purchase_order(self):
        url = reverse('acknowledge-purchaseorder', kwargs={'pk': self.purchase_order.pk})
        acknowledgment_date = timezone.now()  # Current time for acknowledgment
        data = {'acknowledgment_date': acknowledgment_date}

        response = self.client.patch(url, data, format='json')  # Patch or Update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()

        # Check that the acknowledgment date has been set
        self.assertEqual(self.purchase_order.acknowledgment_date, acknowledgment_date)

        # Check if the average response time was correctly calculated and set in the vendor
        expected_response_time = (acknowledgment_date - self.purchase_order.issue_date).total_seconds()
        self.assertAlmostEqual(self.vendor.average_response_time, expected_response_time, places=2)


class VendorPerformanceAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Performance Vendor',
            on_time_delivery_rate=90.0,
            quality_rating_avg=4.5,
            average_response_time=1000,
            fulfillment_rate=95.0
        )

    def test_vendor_performance(self):
        url = reverse('vendor-performance', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the performance data
        data = response.json()
        self.assertEqual(data['on_time_delivery_rate'], 90.0)
        self.assertEqual(data['quality_rating_avg'], 4.5)
        self.assertEqual(data['average_response_time'], 1000)
        self.assertEqual(data['fulfillment_rate'], 95.0)
