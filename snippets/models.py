from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


@register_snippet
class FooterText(models.Model):

    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Текст футера"

    class Meta:
        verbose_name_plural = 'Текст футера'
