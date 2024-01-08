from django.contrib import admin
from . import models

# Register your models here.


class JournalistPostInline(admin.TabularInline):
    model = models.JournalistPost


admin.site.register(models.Journalist)
admin.site.register(models.Post)
admin.site.register(models.Theme)
admin.site.register(models.Comment)
admin.site.register(models.Bulletin_Suscriptor)
