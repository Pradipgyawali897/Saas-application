import stripe
from decouple import config

SECRET_API_KEY = config('API_KEY')
DJANGO_DEBUG = config('DEBUG', default=False, cast=bool)

if 'sk_test' in SECRET_API_KEY and not DJANGO_DEBUG:
    raise ValueError("Stripe test key used while DEBUG=False. Use live key in production.")

stripe.api_key = SECRET_API_KEY


def create_customer(name="", email="", metadata=None, raw=True):
    metadata = metadata or {}
    try:
        response = stripe.Customer.create(
            name=name,
            email=email,
            metadata=metadata,
        )
        return response if raw else response.id
    except Exception as e:
        print("Stripe Error [Customer]:", e)
        raise


def create_product(name="", metadata=None, raw=False):
    metadata = metadata or {}
    try:
        response = stripe.Product.create(
            name=name,
            metadata=metadata,
        )
        print(response)
        return response if raw else response.id
    except Exception as e:
        print("Stripe Error [Product]:", e)
        raise

def create_price(currency="usd", unit_amount=999, recurring="month", product=None, metadata=None, raw=False):
    if product is None:
        raise Exception("Stripe Error: Product ID is required to create a price.")
    
    metadata = metadata or {}
    
    try:
        response = stripe.Price.create(
            currency=currency,
            unit_amount=unit_amount,
            recurring={"interval": recurring}, 
            product=product,
            metadata=metadata,
        )
        return response if raw else response.id

    except Exception as e:
       raise Exception( f"Unexpected error in create_price: {e}")

