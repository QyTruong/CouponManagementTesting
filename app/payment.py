import os
import stripe


class StripePayment:
    def __init__(self, items):
        self.items = items if items is not None else []
        self.stripe = stripe
        self.stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.success_url = 'http://localhost:5000/success'
        self.cancel_url = 'http://localhost:5000/cancel'
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    def create_payment(self, metadata):
        checkout_session = self.stripe.checkout.Session.create(
            line_items= self.items,
            mode='payment',
            metadata=metadata,
            success_url=self.success_url,
            cancel_url=self.cancel_url,
        )

        return {
            "url": checkout_session.url
        }

    def handle_webhook(self, request):
        payload = request.get_data()
        sig_header = request.headers.get('Stripe-Signature')

        if not self.webhook_secret:
            raise ValueError('Chưa cài webhook secret')

        event = stripe.Webhook.construct_event(payload, sig_header, self.webhook_secret)

        return event




