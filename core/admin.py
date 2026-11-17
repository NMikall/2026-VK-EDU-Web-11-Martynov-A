from django.contrib import admin
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile

    def has_delete_permission(self, request, obj=None):
        return False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'user']
    list_select_related = ('user',)
    raw_id_fields = ('user',)
    search_fields = ('nickname', 'user__username')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)