from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Payment

@shared_task
def send_confirmation_email_task(payment_id):
    """
    Sends a payment confirmation email to the user.
    """
    try:
        payment = get_object_or_404(Payment, id=payment_id)
        user = payment.user
        booking = payment.booking

        subject = 'Your Booking is Confirmed!'
        message = f"""
        Dear {user.first_name},

        Your payment of {payment.amount} for booking ID {booking.id} has been successfully processed.

        Thank you for booking with us!

        Best regards,
        ALX Travel App
        """
        from_email = 'noreply@alxtravel.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
        return f"Confirmation email sent to {user.email} for payment {payment_id}"
    except Payment.DoesNotExist:
        return f"Payment with ID {payment_id} not found."