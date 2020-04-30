from django.shortcuts import render, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import order_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


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
            cur_site = get_current_site(request)
            mail_subject = 'Подтверждение оформления ремонта. '
            message = render_to_string('orders/verify_order.html', {
                'order': order,
                'domain': cur_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(order.pk)).decode(),
                'token': order_activation_token.make_token(order)
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            cart.clear()
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
    if order is not None and order_activation_token.check_token(order, token):
        order.verified = True
        order.save()
        return HttpResponse('Отлично! Мы обязательно свяжемся с Вами!')
    else:
        return HttpResponse('Упс. На проблемку напали!')

