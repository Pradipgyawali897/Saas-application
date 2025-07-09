# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
from decouple import config
import stripe
SECRET_API_KEY=config('API_KEY')
DJANGO_DEBUG=config('DEBUG',default=False,cast=bool)
if 'sk_test' in SECRET_API_KEY and not DJANGO_DEBUG:
    raise ValueError("Invalid stripe key")
stripe.api_key = SECRET_API_KEY
def create_consumer(raw=True):
    customer = stripe.Customer.create(
    name="",
    email="",
    )
    if raw:
        return customer
    stripe_id=customer.id
    return stripe_id