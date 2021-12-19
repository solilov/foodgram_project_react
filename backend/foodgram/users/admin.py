from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.models import Follow

User = get_user_model()


class New_UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']
    list_filter = ['email', 'username']


admin.site.unregister(User)
admin.site.register(User, New_UserAdmin)
admin.site.register(Follow)
