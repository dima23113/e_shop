from django.db import models
from slugify import slugify

from modelcluster.fields import ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.models import Page, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock

from brand.models import Brand
from home.models import Category, Rubric, BannerMeta


class Product(BannerMeta, Page):
    subpage_types = []
    parent_page_types = ['product.ProductIndex']
    category_fk = ParentalKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория',
                              related_name='category_products')
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
        FieldPanel('rubric_fk'),
        FieldPanel('brand_fk'),
        FieldPanel('image_banner'),
        FieldPanel('slogan'),
        InlinePanel('product_size', label='Размеры товара')

    ]

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductSize(models.Model):
    size = models.CharField(max_length=256, verbose_name='Размер товара')
    qty = models.IntegerField(verbose_name='Количество')
    product = ParentalKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='product_size')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return f'Размер для товара {self.product}'


class ProductReview(models.Model):
    product = ParentalKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='product_review')
    headline = models.CharField(max_length=50, verbose_name='Заголовок отзыва', help_text='Заголовок к отзыву')
    review = models.TextField(max_length=500, verbose_name='Отзыв на товар')
    stars = models.IntegerField('Оценка товара')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.headline


class ProductIndex(BannerMeta, Page):
    subpage_types = ['product.Product']
    parent_page_types = ['home.HomePage']

    content_panels = [
        FieldPanel('image_banner'),
        FieldPanel('slogan')
    ]
