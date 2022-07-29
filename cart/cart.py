from decimal import Decimal
from django.conf import settings
from product.models import Product, ProductSize


class Cart(object):

    def __init__(self, request, new_session=None):
        if new_session:
            self.session = new_session
        else:
            self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, qty=1, size=None, update_qty=False):
        product_id = str(product.id) + '-' + size
        if product_id not in self.cart:
            if product.price_discount is None:
                self.cart['product_id'] = {
                    'qty': 0,
                    'price': str(product.price),
                    'size': size,
                    'discount_price': str(product.price)
                }
            else:
                self.cart[product_id] = {
                    'qty': 0,
                    'price': str(product.price),
                    'size': size,
                    'discount_price': str(product.price_discount)
                }
        if update_qty:
            self.cart[product_id]['qty'] = qty
        else:
            if self.cart[product_id]['qty'] < ProductSize.objects.get(product=product, size=size).qty:
                self.cart[product_id]['qty'] += qty
            else:
                pass
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        products_id = self.cart.keys()
        product_id_lst = [product for product in products_id]
        for i in range(len(product_id_lst)):
            self.cart[product_id_lst[i]]['product'] = Product.objects.get(id=product_id_lst[i].split('-')[0])
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def get_total_discount_price(self):
        return sum(Decimal(item['discount_price']) * item['qty'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
