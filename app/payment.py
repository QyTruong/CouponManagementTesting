import os

import stripe


class StripePayment:
    def __init__(self, items):
        self.items = items if items is not None else []
        self.stripe = stripe
        self.stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.success_url = 'http://localhost:4242/success'
        self.cancel_url = 'http://localhost:4242/cancel'

    def create_payment(self, metadata, coupon_id):
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

