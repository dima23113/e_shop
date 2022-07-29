from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Category, Rubric


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_order = 000
    menu_icon = 'folder-inverse'
    prepopulated_fields = {'slug': ('name',)}


class RubricAdmin(ModelAdmin):
    model = Rubric
    menu_order = 100
    menu_icon = 'folder-inverse'
    prepopulated_fields = {'slug': ('name',)}


class Menuitem(ModelAdminGroup):
    menu_label = 'Категории'
    menu_icon = 'folder-inverse'
    menu_order = 300
    items = (CategoryAdmin, RubricAdmin)


modeladmin_register(Menuitem)
