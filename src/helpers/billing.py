import stripe
from decouple import config

SECRET_API_KEY = config('API_KEY')
DJANGO_DEBUG = config('DEBUG', default=False, cast=bool)

if 'sk_test' in SECRET_API_KEY and not DJANGO_DEBUG:
    raise ValueError("Invalid stripe key")

stripe.api_key = SECRET_API_KEY

def create_customer(name="", email="", metadata={}, raw=True):
    try:
        response = stripe.Customer.create(
            name=name,
            email=email,
            metadata=metadata,
        )
        return response if raw else response.id
    except Exception as e:
        print("Stripe Error:", e)
        raise

PRODUCT_API_KEY= config('PRODUCT_API_KEY')
stripe.api_key =PRODUCT_API_KEY
product = stripe.Product.create(name="Gold Plan")

def create_product(name="", metadata={}, raw=True):
    try:
        response = stripe.Customer.create(
            name=name,
            metadata=metadata,
        )
        return response if raw else response.id
    except Exception as e:
        print("Stripe Error:", e)
        raise