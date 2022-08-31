from django.db import models
from django.http import JsonResponse

from slugify import slugify

from wagtail.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


class Payment(Page):
    subpage_types = []
    parent_page_types = ['cart.CartPage']
    max_count = 1

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'


class Shipping(Page):
    subpage_types = []
    parent_page_types = ['cart.CartPage']
    max_count = 1

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'


class ConfirmOrder(Page):
    subpage_types = []
    parent_page_types = ['cart.CartPage']
    max_count = 1

    class Meta:
        verbose_name = 'Подтверждение заказа'
        verbose_name_plural = 'Подтверждение заказа'


class DoneOrder(Page):
    subpage_types = []
    parent_page_types = ['cart.CartPage']
    max_count = 1

    class Meta:
        verbose_name = 'Завершение заказа'
        verbose_name_plural = 'Подтверждение заказа'


class CartPage(RoutablePageMixin, Page):
    subpage_types = ['cart.Shipping', 'cart.Payment', 'cart.ConfirmOrder', 'cart.DoneOrder']
    parent_page_types = ['home.HomePage']
    max_count = 1

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def get_context(self, request, *args, **kwargs):
        from cart.cart import Cart
        from cart.forms import DeliveryForm
        context = super(CartPage, self).get_context(request, args, kwargs)
        context['cart'] = Cart(request)
        context['delivery_form'] = DeliveryForm()
        return context

    @route(r'^remove-item/')
    def remove_item(self, request, *args, **kwargs):
        from cart.cart import Cart
        product = request.POST.get('product_id', None)
        cart = Cart(request)
        cart.remove(product)
        return JsonResponse({'id': product.split('-')[0]})

    @route(r'^change-qty/')
    def change_qty(self, request, *args, **kwargs):
        from cart.cart import Cart
        product = request.POST.get('product', None)
        sign = request.POST.get('sign')
        cart = Cart(request)
        if sign == '-':
            cart.cart[product]['qty'] -= 1
            cart.save()
        else:
            cart.cart[product]['qty'] += 1
            cart.save()
        return JsonResponse({'qty': cart.cart[product]['qty'],
                             'total_cost': cart.get_item_total_price(cart.cart[product]['price'],
                                                                     cart.cart[product]['qty'])})

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            from cart.forms import DeliveryForm
            delivery_form = DeliveryForm(request)
            if delivery_form.is_valid():
                print(delivery_form)
            return JsonResponse({'ok': 'ok'})
        else:
            return super().serve(request, *args, **kwargs)
