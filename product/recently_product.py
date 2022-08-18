from decimal import Decimal
from django.conf import settings
from product.models import Product


class RvProduct(object):

    def __init__(self, request, new_session=None):
        if new_session:
            self.session = new_session
        else:
            self.session = request.session
        rv_product = self.session.get(settings.RV_PRODUCT_SESSION_ID)
        if not rv_product:
            rv_product = self.session[settings.RV_PRODUCT_SESSION_ID] = {}
        self.rv_product = rv_product

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.rv_product:
            if len(self.rv_product) == 5:
                self.remove(self.rv_product[list(self.rv_product.keys())[0]])
            self.rv_product[product_id] = {
                'product_ids': product.id,
            }
        self.save()

    def save(self):
        self.session[settings.RV_PRODUCT_SESSION_ID] = self.rv_product
        self.session.modified = True

    def remove(self, product):
        product_id = str(product)
        if product_id in self.rv_product:
            del self.rv_product[product_id]
            self.save()

    def __iter__(self):
        products_id = self.rv_product.keys()
        product_id_lst = [product for product in products_id]
        for i in range(len(product_id_lst)):
            self.rv_product[product_id_lst[i]]['product'] = Product.objects.get(id=product_id_lst[i])

        for item in self.rv_product.values():
            yield item

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
