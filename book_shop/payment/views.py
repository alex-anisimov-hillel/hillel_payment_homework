from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from payment.models import Payment
from payment.stripe_service import StripePayment
from payment.serializers import PaymentSerializer, PaymentCreateSerializer
from orders.models import Order



STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY

def checkout_view(request, order_id=None):
    order = None
    if order_id:
        order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment/checkout.html', {'stripe_public_key': STRIPE_PUBLIC_KEY, 'order': order})


def send_order_confirmation_email(email, order_id):
    if not email:
        return
    send_mail(
        subject='Order confirmation',
        message=f'The payment for our order #{order_id} was successful!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related('user')

    def get_serializer_class(self):
        if self.action == 'create_payment_intent':
            return PaymentCreateSerializer
        return PaymentSerializer

    @action(detail=False, methods=['POST'])
    def create_payment_intent(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            payment, payment_intent = StripePayment.create_payment_intent(user=request.user,
                                                                          amount=Decimal(serializer.validated_data['amount']),
                                                                          currency=serializer.validated_data['currency'],
                                                                          description=serializer.validated_data['description'],
                                                                          metadata=serializer.validated_data.get('metadata', {}))
            return Response({'payment_id': str(payment.id), 'client_secret': payment_intent.client_secret, 'amount': str(payment.amount),
                             'currency': payment.currency, 'status': payment.status}, status=status.HTTP_201_CREATED)
        except ValueError as exception:
            return Response({'Value error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            return Response({'Error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['POST'])
    def confirm_payment(self, request, pk):
        payment = self.get_object()
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.payment_method = payment
        order.save()
        try:
            payment = StripePayment.confirm_payment(payment_id=str(payment.id), stripe_payment_intent_id=payment.stripe_payment_intent_id)
            if order.user.email != "":
                send_order_confirmation_email(order.user.email, order_id)
            serializer = self.get_serializer(payment)
            return Response(serializer.data)
        except Exception as exception:
            return Response({'Error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)