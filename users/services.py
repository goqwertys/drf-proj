import stripe
from config import settings
from config.settings import STRIPE_API_KEY

class StripeService:
    def __init__(self):
        self.stripe = stripe
        self.stripe_api_key = STRIPE_API_KEY

    def create_product(self, name, description):
        product = self.stripe.Product.create(
            name=name,
            description=description
        )
        return product.id

    def create_price(self, product_id: str, amount: int, currency: str):
        price=self.stripe.Price.create(
            product=product_id,
            unit_amount=amount,
            currency=currency
        )
        return price.id

    def create_checkout_session(self, price_id: str, success_url: str, cancel_url: str):
        session = self.stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url
        )
        return session.url, session.id

    def handle_webhook(self, payload, sig_header):
        event = self.stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_API_KEY
        )
        if event.get('type') == 'checkout.session.completed':
            session = event['data']['object']
        self.update_payment_status(session["id"])


class CourseService:
    def __init__(self, stripe_service: StripeService):
        self.stripe_service = stripe_service

    def create_course(self):
        pass
