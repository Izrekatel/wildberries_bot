from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class User(UserAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email',)
    list_editable = ('username', 'first_name', 'last_name', 'email',)
    search_fields = ('pk', 'username', 'first_name', 'last_name', 'email',)
    list_filter = ('username', 'first_name', 'last_name', 'email',)
    empty_value_display = '-пусто-'
    add_fieldsets = (
        (None,
            {'classes': ('wide',), 'fields': (
                'email',
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2'
            )
            }),
    )
