from django.contrib import admin
from .models import *


class FootingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Footing._meta.fields]

    class Meta:
        model = Footing


class ContractsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contracts._meta.fields]

    class Meta:
        model = Contracts


class DecisionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Decision._meta.fields]

    class Meta:
        model = Decision


class RIAAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RIA._meta.fields]

    class Meta:
        model = RIA


class DocumentFilesRIAAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DocumentFilesRIA._meta.fields]

    class Meta:
        model = DocumentFilesRIA


class AuthorsRIAAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AuthorsRIA._meta.fields]

    class Meta:
        model = AuthorsRIA


class ReestrAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reestr._meta.fields]

    class Meta:
        model = Reestr


admin.site.register(Footing, FootingAdmin)
admin.site.register(Contracts, ContractsAdmin)
admin.site.register(Decision, DecisionAdmin)
admin.site.register(RIA, RIAAdmin)
admin.site.register(AuthorsRIA, AuthorsRIAAdmin)
admin.site.register(DocumentFilesRIA, DocumentFilesRIAAdmin)
admin.site.register(Reestr, ReestrAdmin)
