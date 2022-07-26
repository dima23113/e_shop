from django.db import models
from slugify import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page


class Brand(Page):
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
        ImageChooserPanel('image')
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
