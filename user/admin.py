from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from user.forms import (
    UserChangeForm,
    UserCreationForm,
)

User = get_user_model()

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'is_student', 'is_teacher', 'is_active',)
    list_filter = ('email', 'is_student', 'is_teacher', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'otp')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_student', 'is_teacher', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'otp', 'is_staff', 'is_active', 'is_student', 'is_teacher',
                'is_verified')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


