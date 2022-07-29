from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import ProductSize, Product, ProductReview


class ProductSizeAdmin(ModelAdmin):
    menu_label = 'Размеры товаров'
    model = ProductSize
    menu_icon = 'folder-inverse'
    menu_order = 100
    search_fields = ('product__name', 'size', 'qty')
    list_display = ('product', 'size', 'qty')


class ProductAdmin(ModelAdmin):
    menu_label = 'Товары'
    menu_icon = 'folder-inverse'
    model = Product
    menu_order = 000
    search_fields = ('name', 'brand_fk__name')
    list_display = ('name', 'brand_fk', 'category_fk', 'rubric_fk', 'price', 'available')


class ProductReviewAdmin(ModelAdmin):
    menu_label = 'Отзывы'
    menu_icon = 'folder-inverse'
    model = ProductReview
    menu_order = 300
    search_fields = ('product__name', 'headline')
    list_display = ('product', 'headline', 'stars')


class ProductGroup(ModelAdminGroup):
    menu_label = 'Товары'
    menu_icon = 'folder-inverse'
    menu_order = 300
    items = (ProductAdmin, ProductSizeAdmin, ProductReviewAdmin)


modeladmin_register(ProductGroup)
