from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin

from main_service_of_plotters.apps.materials.models import Label, Template


class LabelResource(resources.ModelResource):

    class Meta:
        model = Label


class CustomLabelAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = LabelResource
    list_display = ('scratch_code', 'barcode', 'date_creation', 'count')
    list_filter = ('date_creation', )
    search_fields = ('date_creation', )


admin.site.register(Template)
admin.site.register(Label, CustomLabelAdmin)
