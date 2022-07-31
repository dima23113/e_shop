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
    slogan = models.CharField(max_length=256, verbose_name='Слоган к баннеру', null=True, blank=True)

    class Meta:
        abstract = True


class CategoriesMeta(models.Model):
    description = models.TextField(verbose_name='Описанние категории', null=True, blank=True)
    logo = models.ForeignKey('wagtailimages.Image',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name='+',
                             verbose_name='Лого категории'
                             )
    category_banner = models.ForeignKey('wagtailimages.Image',
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True,
                                        related_name='+',
                                        verbose_name='Баннер категории'
                                        )

    class Meta:
        abstract = True


class Category(CategoriesMeta, Page):
    subpage_types = ['home.Rubric']
    parent_page_types = ['home.HomePage']

    name = models.CharField(max_length=256, verbose_name='Название категории')
    content_panels = [
        FieldPanel('title'),
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('logo'),
        FieldPanel('category_banner'),
        InlinePanel('rubrics', label='')
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


class Rubric(CategoriesMeta, Page):
    parent_page_types = ['home.Category']

    name = models.CharField(max_length=256, verbose_name='Рубрика')
    category_fk = ParentalKey(Category, related_name='rubrics',
                              on_delete=models.SET_NULL,
                              verbose_name='Категория', null=True, blank=True)
    content_panels = [
        FieldPanel('title'),
        FieldPanel('name'),
        PageChooserPanel('category_fk'),
        FieldPanel('description'),
        FieldPanel('logo'),
        FieldPanel('category_banner')

    ]

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

    def __str__(self):
        return f'{self.category_fk.name} - {self.name}'

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
    banner_bottom = StreamField([
        ('brand_banner_bottom', PageChooserBlock(help_text='Нижний баннер брендов', page_type=['brand.Brand'])),
        ('product_banner_bottom', PageChooserBlock(help_text='Нижний банер товара', page_type=['product.Product'])),
        ('products_banner_bottom',
         PageChooserBlock(help_text='Нижний банер товаров', page_type=['product.ProductIndex']))
    ], null=True, blank=True, verbose_name='Нижний баннер')

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('banner'),
        StreamFieldPanel('brand_logo'),
        StreamFieldPanel('banner_bottom')
    ]

    def get_context(self, request, *args, **kwargs):
        from brand.models import Brand
        context = super().get_context(request, *args, **kwargs)
        context['brands'] = Brand.objects.live().values('image', 'slug')[:10]
        return context
