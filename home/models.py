from django.db import models
from slugify import slugify
from smart_selects.db_fields import GroupedForeignKey

from modelcluster.fields import ParentalKey

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from instance_selector.edit_handlers import InstanceSelectorPanel

from wagtailautocomplete.edit_handlers import AutocompletePanel


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
