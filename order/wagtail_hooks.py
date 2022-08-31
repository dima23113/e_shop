from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import OrderItem, Order


class OrderInfoAdmin(ModelAdmin):
    menu_label = 'Информация по заказу'
    model = Order
    menu_icon = 'folder-inverse'
    menu_order = 100
    search_fields = ('customer', 'phone', 'email')
    list_display = ('id', 'customer', 'payment_status', 'payment_id')


class OrderItemsAdmin(ModelAdmin):
    menu_label = 'Позиции заказа'
    model = OrderItem
    menu_icon = 'folder-inverse'
    menu_order = 200
    search_fields = ('order__customer', 'product')
    list_display = ('order__customer', 'product', 'size', 'qty', 'price', 'price_discount')


class OrderGroup(ModelAdminGroup):
    menu_label = 'Заказы'
    menu_icon = 'folder-inverse'
    menu_order = 300
    items = (OrderInfoAdmin, OrderItemsAdmin)


modeladmin_register(OrderGroup)
