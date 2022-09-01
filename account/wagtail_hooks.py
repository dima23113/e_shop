from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import CustomUser


class UserListAdmin(ModelAdmin):
    menu_label = 'Пользователи'
    model = CustomUser
    menu_icon = 'folder-inverse'
    menu_order = 300
    search_fields = ('email', 'phone')
    list_display = ('email', 'phone', 'email_mailing')


modeladmin_register(UserListAdmin)
