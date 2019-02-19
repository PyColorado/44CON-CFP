from .base import *


EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    'SENDGRID_API_KEY': configuration["anymail"]["sendgrid"]["api_key"],
    'SENDGRID_SENDER_DOMAIN': configuration["anymail"]["sendgrid"]["sender_domain"],
}
DEFAULT_FROM_EMAIL = configuration['anymail']['from_email']
