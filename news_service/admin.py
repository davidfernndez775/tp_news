from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.


class JournalistPostInline(admin.TabularInline):
    model = models.JournalistPost


class JournalistInline(admin.StackedInline):
    model = models.Journalist
    can_delete = False
    verbose_name_plural = "journalists"


admin.site.register(models.Journalist)
admin.site.register(models.Post)
admin.site.register(models.Theme)
admin.site.register(models.Comment)
admin.site.register(models.Client)


class UserAdmin(BaseUserAdmin):
    inlines = [JournalistInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
