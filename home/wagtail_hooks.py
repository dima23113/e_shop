from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Category, Subcategory, Rubric


class CategoryAdmin(ModelAdmin):
    model = Category
    index_template_name = 'category.html'
    menu_order = 000
    prepopulated_fields = {'slug': ('name',)}


class SubcategoryAdmin(ModelAdmin):
    model = Subcategory
    menu_order = 100
    prepopulated_fields = {'slug': ('name',)}


class RubricAdmin(ModelAdmin):
    model = Rubric
    menu_order = 200
    prepopulated_fields = {'slug': ('name',)}


class Menuitem(ModelAdminGroup):
    menu_label = 'Элементы меню'
    menu_icon = 'pick'
    menu_order = 500
    items = (CategoryAdmin, SubcategoryAdmin, RubricAdmin)


modeladmin_register(Menuitem)
