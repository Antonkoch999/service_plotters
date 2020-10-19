from django.contrib import admin
from main_service_of_plotters.apps.materials.models import Template, Label
from import_export import resources
from import_export.admin import ImportExportMixin


# Register your models here.


class LabelResource(resources.ModelResource):

    class Meta:
        model = Label


class CustomLabelAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = LabelResource
    list_display = ('scratch_code', 'barcode', 'date_creation', 'count')


admin.site.register(Template)
admin.site.register(Label, CustomLabelAdmin)


