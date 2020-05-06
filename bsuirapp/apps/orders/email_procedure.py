from smtplib import SMTPException
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import order_activation_token
from django.core.mail import EmailMessage
import multiprocessing
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def send_verify_emails(order, request):
    cur_site = get_current_site(request)
    mail_subject = 'Подтверждение оформления ремонта.'
    now = datetime.now()
    message = render_to_string('orders/verify_order.html', {
        'order': order,
        'time': now.strftime("%d/%m/%Y, %H:%M:%S"),
        'domain': cur_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(order.pk)).decode(),
        'token': order_activation_token.make_token(order)
    })

    email = EmailMessage(
        mail_subject, message, to=[order.email]
    )
    process = multiprocessing.Process(target=send_email, args=(email,))
    process.start()


def send_email(email):
    logger.info('sending mail')
    try:
        email.send()
        logger.info('email sent successfully.')
    except SMTPException as e:
        logger.error('there was an error sending an email: %s', e)