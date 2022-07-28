from django.db import models
from slugify import slugify

from modelcluster.fields import ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.models import Page, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock

from brand.models import Brand
from home.models import Category, Subcategory, Rubric, BannerMeta


class Product(BannerMeta, Page):
    subpage_types = []
    parent_page_types = ['product.ProductIndex']
    category_fk = ParentalKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория',
                              related_name='category_products')
    subcategory_fk = ParentalKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Подкатегория', related_name='subcategory_products')
    rubric_fk = ParentalKey(Rubric, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Рубрика',
                            related_name='rubric_products')
    brand_fk = ParentalKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Бренд',
                           related_name='brand_products')
    name = models.CharField('Название', max_length=256)
    sizes_info = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='+', verbose_name='Размерная сетка')
    description = StreamField([
        ('description', RichTextBlock()),
        ('specifications', RichTextBlock()),

    ])
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    available = models.BooleanField(default=True, verbose_name='Доступность товара')
    article = models.CharField(max_length=256, verbose_name='Артикул')
    image = StreamField([
        ('images', ImageChooserBlock(help_text='Изображения товара'))
    ])
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара со скидкой')
    sale = models.BooleanField(default=False, verbose_name='Индикатор активности скидки')

    content_panels = [
        FieldPanel('title'),
        FieldPanel('name'),
        StreamFieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('available'),
        FieldPanel('article'),
        StreamFieldPanel('image'),
        FieldPanel('price_discount'),
        FieldPanel('sale'),
        FieldPanel('category_fk'),
        FieldPanel('subcategory_fk'),
        FieldPanel('rubric_fk'),
        FieldPanel('brand_fk'),
        FieldPanel('image_banner')

    ]

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductIndex(BannerMeta, Page):
    subpage_types = ['product.Product']
    parent_page_types = ['home.HomePage']
