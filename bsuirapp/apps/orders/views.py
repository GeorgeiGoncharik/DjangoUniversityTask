import logging

from cart.cart import Cart
from .email_procedure import send_verify_emails
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tokens import order_activation_token

logger = logging.getLogger(__name__)

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            logger.info('order created %s', order.id)
            send_verify_emails(order, request)
            cart.clear()
            logger.info('cart cleared.')
            return render(
                request,
                'orders/created.html',
                {'order': order}
            )
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/create.html',
        {'cart': cart, 'form': form}
    )


def verify(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        order = Order.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
        order = None
        logger.error('no order found while verification')
    if order is not None and order_activation_token.check_token(order, token):
        order.verified = True
        order.save()
        logger.info('order verified %s', order.id)
        return HttpResponse('Отлично! Мы обязательно свяжемся с Вами!')
    else:
        logger.error('problem with verifying order')
        return HttpResponse('Упс. На проблемку напали!')

