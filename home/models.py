from django.db import models
from slugify import slugify
from smart_selects.db_fields import GroupedForeignKey

from modelcluster.fields import ParentalKey
from wagtail.blocks import PageChooserBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel


class BannerMeta(models.Model):
    image_banner = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='+', verbose_name='Изображение для баннера')

    class Meta:
        abstract = True


class Category(Page):
    subpage_types = ['home.Subcategory']
    parent_page_types = ['home.HomePage']

    name = models.CharField(max_length=256, verbose_name='Название категории')
    content_panels = [
        FieldPanel('title'),
        FieldPanel('name'),

        InlinePanel('subcategories', label='')
    ]

    def __str__(self):
        return f'Категория - {self.name}'

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.slug = f'category-{slug}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(Page):
    subpage_types = ['home.Rubric']
    parent_page_types = ['home.Category']

    name = models.CharField(max_length=256, verbose_name='Название подкатегории')
    category_fk = ParentalKey(Category, related_name='subcategories',
                              on_delete=models.SET_NULL, verbose_name='Категория', null=True, blank=True)
    content_panels = [
        FieldPanel('title'),
        FieldPanel('name'),
        PageChooserPanel('category_fk')

    ]

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.category_fk.name} - {self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Rubric(Page):
    parent_page_types = ['home.Subcategory']

    name = models.CharField(max_length=256, verbose_name='Тип подкатегории')
    subcategory_fk = ParentalKey(Subcategory, related_name='rubrics',
                                 on_delete=models.SET_NULL,
                                 verbose_name='Рубрика', null=True, blank=True)
    content_panels = [
        FieldPanel('title'),
        FieldPanel('name'),
        PageChooserPanel('subcategory_fk')

    ]

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

    def __str__(self):
        return f'{self.subcategory_fk.name} - {self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class HomePage(Page):
    subpage_types = ['home.Category', 'brand.BrandIndex', 'product.ProductIndex']
    parent_page_types = []
    banner = StreamField([
        ('brand_banner', PageChooserBlock(help_text='Баннер брендов', page_type=['brand.Brand'])),
        ('product_banner', PageChooserBlock(help_text='Баннер товаров', page_type=['product.Product']))
    ], null=True, blank=True, verbose_name='Верхний баннер')
    brand_logo = StreamField([
        ('brand_banner', PageChooserBlock(help_text='Лого брендов', page_type=['brand.Brand']))
    ], null=True, blank=True)

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('banner'),
        StreamFieldPanel('brand_logo')
    ]

    def get_context(self, request, *args, **kwargs):
        from brand.models import Brand
        context = super().get_context(request, *args, **kwargs)
        context['brands'] = Brand.objects.live().values('image', 'slug')[:10]
        return context
