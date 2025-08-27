# listings/views.py
import os
import requests
import uuid
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_confirmation_email_task



# Chapa API Configuration
CHAPA_API_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/"

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.

    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
.ac
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class InitiatePaymentView(APIView):
    """
    API endpoint to initiate a payment with Chapa.
    Expects a 'booking_id' in the request body.
    """
    def post(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")
        if not booking_id:
            return Response({"error": "Booking ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = get_object_or_404(Booking, id=booking_id)
            user = request.user
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        # Generate a unique transaction reference
        tx_ref = f"tx-{booking.id}-{uuid.uuid4()}"

        # Create a payment record in the database
        payment = Payment.objects.create(
            user=user,
            booking=booking,
            amount=booking.amount,
            tx_ref=tx_ref,
            status=Payment.PaymentStatus.PENDING
        )

        # Prepare data for Chapa API
        payment_data = {
            "amount": str(booking.amount),
            "currency": "ETB",  # Or your desired currency
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "tx_ref": tx_ref,
            "callback_url": f"https://yourdomain.com/verify-payment/{tx_ref}", # URL Chapa will redirect to
            "return_url": f"https://yourfrontend.com/payment-success/", # URL user sees after payment
            "customization[title]": "Payment for Travel Booking",
            "customization[description]": f"Booking ID: {booking.id}",
        }

        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(CHAPA_API_URL, json=payment_data, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            chapa_response = response.json()

            if chapa_response.get("status") == "success":
                checkout_url = chapa_response["data"]["checkout_url"]
                return Response({"checkout_url": checkout_url}, status=status.HTTP_200_OK)
            else:
                payment.status = Payment.PaymentStatus.FAILED
                payment.save()
                return Response({"error": "Failed to initiate payment with Chapa.", "details": chapa_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            payment.status = Payment.PaymentStatus.FAILED
            payment.save()
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class VerifyPaymentView(APIView):
    """
    API endpoint to verify a payment with Chapa using the transaction reference.
    This can be used as a callback URL or called by the frontend.
    """
    def get(self, request, tx_ref, *args, **kwargs):
        try:
            payment = get_object_or_404(Payment, tx_ref=tx_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
        }

        try:
            response = requests.get(f"{CHAPA_VERIFY_URL}{tx_ref}", headers=headers)
            response.raise_for_status()
            chapa_response = response.json()

            if chapa_response.get("status") == "success":
                # Payment was successful
                payment.status = Payment.PaymentStatus.COMPLETED
                payment.save()

                # Trigger background task to send confirmation email
                send_confirmation_email_task.delay(payment.id)

                return Response({"message": "Payment verified successfully."}, status=status.HTTP_200_OK)
            else:
                # Payment failed or is still pending
                payment.status = Payment.PaymentStatus.FAILED
                payment.save()
                return Response({"error": "Payment verification failed.", "details": chapa_response}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"An error occurred during verification: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
