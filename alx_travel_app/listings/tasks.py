from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Payment, Booking
from django.conf import settings
import logging


# Get a logger instance
logger = logging.getLogger(__name__)

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


@shared_task
def send_booking_confirmation_email(booking_id):
    """
    Sends a booking confirmation email to the user asynchronously.

    Args:
        booking_id (int): The ID of the booking to send confirmation for.
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        subject = 'Your Booking Confirmation'
        message = f"""
        Dear {booking.user.username},

        Thank you for your booking!

        Here are your booking details:
        - Listing: {booking.listing.title}
        - Check-in Date: {booking.check_in_date}
        - Check-out Date: {booking.check_out_date}
        - Guests: {booking.guests}

        We look forward to hosting you!

        Best regards,
        The ALX Travel App Team
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [booking.user.email]

        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Successfully sent booking confirmation email for booking ID: {booking_id}")

    except Booking.DoesNotExist:
        logger.error(f"Booking with ID {booking_id} does not exist. Email not sent.")
    except Exception as e:
        logger.error(f"Failed to send email for booking ID {booking_id}: {e}")
