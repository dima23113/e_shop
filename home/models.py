from django.db import models
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from slugify import slugify

from modelcluster.fields import ParentalKey
from wagtail.blocks import PageChooserBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


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


class Category(RoutablePageMixin, CategoriesMeta, Page):
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

    def serve(self, request, *args, **kwargs):
        if request.method == 'GET':
            print(self.slug)
            from product.models import Product
            context = super().get_context(request, *args, **kwargs)
            paginator = Paginator(Product.objects.live().filter(category_fk=self.id, available=True), 60)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['products'] = page_obj
            return render(request, 'home/category.html', context=context)

    '''@route(r'^category/(?P<category>[-\w]+)/$')
    def get_products(self, request, category, *args, **kwargs):
        print(request, category, args, kwargs)
        return self.render(request)'''

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


class HomePage(RoutablePageMixin, Page):
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
