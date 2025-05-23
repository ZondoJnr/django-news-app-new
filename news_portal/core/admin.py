from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Publisher, Article, Newsletter

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {
            'fields': ('role', 'subscriptions_to_publishers', 'subscriptions_to_journalists')
        }),
    )

admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Newsletter)

