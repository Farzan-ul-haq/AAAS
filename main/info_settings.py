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
EMAIL_HOST_USER='aaasinc786@gmail.com'
EMAIL_HOST_PASSWORD='ylpzhjrbdoeqjzrj'

DRIBBLE_CLIENT_ID = 'd76916be14a7b91d0a8cab3b4aa6c6c3019ded7a941ff2cbe64d533ce117580d'
DRIBBLE_CLIENT_SECRET = 'd51d19756a076ae124294bc34eadf33b71dad342e601f5d9cf7a8d19fdc97905'
DRIBBLE_ACCESS_TOKEN = 'a7e0b11e0b9c2c2006454d374073663a31f09f98baeb4128e53e2683e1b9fcb4'

SHAKIR_CARD_NO = '4782 7800 0041 3883'
SHAKIR_CARD_VALIDITY = '03/27'
SHAKIR_CARD_CVV = '327'

DRIBBLE_SHOTS_URL = 'https://dribbble.com/shots/'