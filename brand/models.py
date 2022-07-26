from django.db import models

from slugify import slugify

from wagtail.admin.panels import FieldPanel, StreamFieldPanel
from wagtail.blocks import PageChooserBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page

from home.models import BannerMeta
from .services import sort_brand_list


class Brand(BannerMeta, Page):
    subpage_types = []
    parent_page_types = ['brand.BrandIndex']
    name = models.CharField('Название бренда', max_length=256)
    description = RichTextField(blank=True, null=True, verbose_name='Описание бренда')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='+',
                              verbose_name='Лого бренда'
                              )
    content_panels = [
        FieldPanel('title'),
        FieldPanel('name'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
        FieldPanel('image_banner'),
        FieldPanel('slogan')
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, kwargs)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class BrandIndex(Page):
    subpage_types = ['brand.Brand']
    parent_page_types = ['home.HomePage']
    description = RichTextField(verbose_name='Описание страницы брендов', null=True, blank=True)
    top_brands = StreamField([
        ('top_brands', PageChooserBlock(help_text='Выбор топ брендов', page_type=['brand.Brand']))
    ], null=True, blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        StreamFieldPanel('top_brands')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['brands'] = sort_brand_list()
        return context
