from django.contrib.auth.admin import UserAdmin
from account.models import User
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _

UserAdmin.fieldsets = (
    (None, {"fields": ("phone_number", "username", "password")}),
    (_("Personal info"), {"fields": ("first_name", "last_name", "email", "age", "profile_photo", 'about_me')}),
    (
        _("Permissions"),
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
    ),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
)
UserAdmin.add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": ("phone_number", "username", "password1", "password2"),
        },
    ),
)

admin.site.register(User, UserAdmin)

admin.site.unregister(Site)
admin.site.unregister(Group)
