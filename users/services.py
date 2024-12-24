import stripe
from django.conf import settings
from django.urls import reverse


class StripeService:
    def __init__(self):
        self.api_key = settings.STRIPE_API_KEY
        stripe.api_key = self.api_key

    def create_stripe_product(self, name, description):
        """ Creates Stripe product """
        try:
            product = stripe.Product.create(
                name=name,
                description=description
            )
            return product
        except stripe.error.StripeError as e:
            raise ValueError(f'Error creating product in Stripe: {e}')

    def create_stripe_price(self, product_id, unit_amount, currency="usd"):
        """ Creates Stripe product """
        try:
            price = stripe.Price.create(
                currency=currency,
                unit_amount=unit_amount,
                product=product_id
            )
            return price
        except stripe.error.StripeError as e:
            raise ValueError(f'Error creating price in Stripe: {e}')

    def create_stripe_session(self, success_url, price_id):
        """ Creates Stripe product """
        try:
            session = stripe.checkout.Session.create(
                success_url=success_url,
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1
                    }
                ],
                mode="payment",
            )
            return session
        except stripe.error.StripeError as e:
            raise ValueError(f'Error creating session in Stripe: {e}')

    def handle_payment(self, payment, success_url):
        """ Handle payment in stripe """
        service = payment.get_service()
        if not service:
            raise ValueError('Payment must be associated with a course or lesson.')

        stripe_product = self.create_stripe_product(
            name=service.name,
            description=service.description
        )

        stripe_price = self.create_stripe_price(
            product_id=stripe_product.id,
            unit_amount=int(payment.amount * 100)
        )

        session = self.create_stripe_session(
            success_url=success_url,
            price_id=stripe_price.id
        )

        payment.link = session.url
        payment.session_id = session.id
        payment.save()

        return session
