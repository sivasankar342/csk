from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from .models import dealer

class UserAdminConfig(UserAdmin):
    model = dealer
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        ('Personal', {'fields': ('about',)})
    )

    # Override form field for 'about' field
    formfield_overrides = {
        dealer.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})}
    }

    # Customized add fields for User creation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff',)
        }),
    )

# Register the NewUser model with the customized UserAdminConfig
admin.site.register(dealer, UserAdminConfig)