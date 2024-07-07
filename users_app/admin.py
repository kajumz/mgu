from django.contrib import admin
from .models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Author._meta.fields]

    class Meta:
        model = Author


class NotificationsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Notifications._meta.fields]

    class Meta:
        model = Notifications


admin.site.register(Author, AuthorAdmin)
admin.site.register(Notifications, NotificationsAdmin)
