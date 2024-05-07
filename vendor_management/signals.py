from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor

# Signal to update on-time delivery rate and fulfillment rate
@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        # Update on-time delivery rate
        on_time_deliveries = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed',
            delivery_date__lte=instance.delivery_date
        ).count()
        total_deliveries = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed'
        ).count()
        if total_deliveries > 0:
            instance.vendor.on_time_delivery_rate = (on_time_deliveries / total_deliveries) * 100
        
        # Update quality rating average
        completed_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed',
            quality_rating__isnull=False
        )
        if completed_orders.exists():
            quality_avg = completed_orders.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
            instance.vendor.quality_rating_avg = quality_avg
        
        # Update fulfillment rate
        successful_fulfillment = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed'
        ).count()
        if total_deliveries > 0:
            instance.vendor.fulfillment_rate = (successful_fulfillment / total_deliveries) * 100
        
        # Save vendor metrics
        instance.vendor.save()

    # Update average response time
    if instance.acknowledgment_date:
        response_times = [
            (po.acknowledgment_date - po.issue_date).total_seconds()
            for po in PurchaseOrder.objects.filter(vendor=instance.vendor)
            if po.acknowledgment_date
        ]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            instance.vendor.average_response_time = avg_response_time
        
        # Save vendor metrics
        instance.vendor.save()
