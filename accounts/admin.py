from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Inline admin for UserProfile to be displayed within User admin.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'avatar', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class CustomUserAdmin(UserAdmin):
    """
    Custom User admin that includes UserProfile inline.
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    """
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('user', 'bio', 'avatar', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
