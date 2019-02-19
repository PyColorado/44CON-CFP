from .base import *


EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    'MAILGUN_API_KEY': configuration["anymail"]["mailgun"]["api_key"],
    'MAILGUN_SENDER_DOMAIN': configuration["anymail"]["mailgun"]["sender_domain"],
}
