from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username','first_name', 'last_name', 'email', 'is_superuser', 'is_coach', 'uniqueID' )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'promotion', 'uniqueID')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_coach'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined', 'date_of_birth')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)