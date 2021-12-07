from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Follow


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']
    list_filter = ['email', 'username']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Follow)
