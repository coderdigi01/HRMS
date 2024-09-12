from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import UserProfile, OTP

class UserProfileAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ('mobile_number', 'email', 'is_admin')
    list_filter = ('is_admin',)

    # Fields to display in the admin edit page
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    # Fields to display in the create user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'email', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('mobile_number', 'email')
    ordering = ('mobile_number',)
    filter_horizontal = ()

# Register the custom User model
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OTP)

# Optionally, unregister the Group model since we are not using it
admin.site.unregister(Group)
