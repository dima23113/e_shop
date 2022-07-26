# Generated by Django 4.0.6 on 2022-07-23 13:09

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_category_subcategory_rubric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubric',
            name='subcategory_fk',
            field=smart_selects.db_fields.GroupedForeignKey(blank=True, group_field='category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rubrics', to='home.subcategory', verbose_name='Подкатегория'),
        ),
    ]
