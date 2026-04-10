import os
import stripe
from requests import session


class StripePayment:
    def __init__(self, items):
        self.items = items if items is not None else []
        self.stripe = stripe
        self.stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.success_url = 'http://localhost:5000/success'
        self.cancel_url = 'http://localhost:5000/cancel'
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    def create_payment(self, metadata):
        try:
            checkout_session = self.stripe.checkout.Session.create(
                line_items= self.items,
                mode='payment',
                metadata=metadata,
                success_url=self.success_url,
                cancel_url=self.cancel_url,
            )
        except Exception as e:
            return {"error": str(e)}

        return checkout_session.url

    def handel_webhook(self, request):
        payload = request.data
        event = None
        sig_header = request.headers.get('Stripe-Signature')

        if self.webhook_secret:
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, self.webhook_secret
                )
            except Exception as e:
                raise ValueError('Chữ ký xác thực webhook bị lỗi')

            return event

        raise Exception("webhook error")
