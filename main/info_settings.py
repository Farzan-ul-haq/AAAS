import datetime


LATEST_BUILD = datetime.datetime.now()

PRODUCT_TYPES = [
    "API",
    'LOGO',
    "TEMPLATE",
    "SOFTWARE"
]

#SMTP Configuration
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='aaas.inc00@gmail.com'
EMAIL_HOST_PASSWORD='yogdaujhajrrfdyw'

DRIBBLE_CLIENT_ID = '765c77fd6b12185f44e5a365b56f11d64066dcd6008317befa4cddfc8e51bc9e'
DRIBBLE_CLIENT_SECRET = '8ae48d4b31c2832f97e24322007ca0b04128ab52e6b1160dadaf2e5573757115'
DRIBBLE_ACCESS_TOKEN = '584ffde7831dc7e13d05c2d02e66ea0c886d2f8b4c737b126fa795f2e87fe0fa'
DRIBBLE_READ_ACCESS_TOKEN = '584ffde7831dc7e13d05c2d02e66ea0c886d2f8b4c737b126fa795f2e87fe0fa'
DRIBBLE_SHOTS_URL = 'https://dribbble.com/shots/'

PINTEREST_PIN_URL = "https://www.pinterest.com/pin/"

COROFLOT_PIN_URL = "https://www.coroflot.com/p/"

SHAKIR_CARD_NO = '4782 7800 0041 3883'
SHAKIR_CARD_VALIDITY = '03/27'
SHAKIR_CARD_CVV = '327'


STRIPE_LIVE_SECRET_KEY = "########"
STRIPE_TEST_SECRET_KEY = "sk_test_51MS2tcDggfMz04hut6mhjgyRUlwgPqmSNDGxo3ycTuVwF5bKHfOFfvH12cEDIgEh0UpAgLGXMzNlCu6XenuaJMYM00pypWUW1B"
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = "whsec_x9Rm8FbkWecFseBnxB76vAmUU5kgbOOm"
# DJSTRIPE_WEBHOOK_SECRET = "whsec_83251f38b839a7093bb8b8649ed2cae43f606185b4fd09c4ee8a011d06573100"
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_USE_NATIVE_JSONFIELD = True
STRIPE_CUSTOMER_ID_APPEND = 'CUS_'
# LOCAL whsec_83251f38b839a7093bb8b8649ed2cae43f606185b4fd09c4ee8a011d06573100

STRIPE_VALID_CARD = "4242424242424242"
DECLINE_CARD = "4000000000000002"
INSUFFICIENT_CARDS = "4000000000009995"
EXPIRED_CARD = "4000000000000069"
INCORRECT_CVC_CARD = "4000000000000127"