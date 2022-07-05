from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from student.models import CourseRegistration


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        cr = get_object_or_404(CourseRegistration, id=ipn.invoice)

        if cr.course.price == ipn.mc_gross:
            cr.paid = True
            cr.subscribed = True
            cr.transaction_id = ipn.txn_id
            cr.save()
