from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_active', 'get_groups')
    search_fields = ['email']
    list_filter = ('is_staff', 'is_active')

    def get_groups(self, obj):
        return ", ".join(obj.groups.values_list('name', flat=True))
    get_groups.short_description = 'Roles'
