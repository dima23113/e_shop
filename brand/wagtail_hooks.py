from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Brand


class BrandListAdmin(ModelAdmin):
    menu_label = 'Бренды'
    model = Brand
    menu_icon = 'folder-inverse'
    menu_order = 300
    search_fields = ('name',)
    list_display = ('name',)


modeladmin_register(BrandListAdmin)
