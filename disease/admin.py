from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry


# Register your models here.

class DiseaseDetailDivisionAdmin(admin.ModelAdmin):
    model = DiseaseDetailDivision

    list_display = ['id','div_name',]

#
# def linked_diseases_count(obj):
#     return obj.disease_set.all().count()
# linked_diseases_count.short_description = 'd_count'


class DiseaseDetailInline(admin.StackedInline):
    model = Disease.diseaseDetail.through


class DiseaseDetailAdmin(admin.ModelAdmin):
    model = DiseaseDetail
    search_fields = ('rep_title',)
    list_editable = ('disease_detail_division',)
    list_filter = ('disease_detail_division','source','translate_flag')
    # list_filter = ('',)
    # inlines = [DiseaseDetailInline,]
    # autocomplete_fields = ('diseases',)

    list_display = ('id','disease_detail_division','linked_diseases_count','rep_title', 'rep_title_en','title1','title2','title3')

    def linked_diseases_count(self, obj):
        return obj.diseases.all().count()
    linked_diseases_count.short_description = 'd_count'
    #
    # def get_formsets_with_inlines(self, request, obj=None):
    #     for inline in self.get_inline_instances(request, obj):
    #         # # hide MyInline in the add view
    #         # if isinstance(inline, DiseaseDetailInline) and obj is None:
    #         #     continue
    #         obj = obj.diseases.all()
    #         yield inline.get_formset(request, obj), inline

    # def has_change_permission(self, request, obj=None):
    #     return False


class DiseaseAdmin(admin.ModelAdmin):
    model = Disease
    search_fields = ('name_kr','code')
    list_filter = ('is_rep', )
    autocomplete_fields = ('diseaseDetail',)

    list_display = ['id','name_kr','str_disease_detail','code', 'rep_code','is_rep']

    def str_disease_detail(self, obj):
        str = ''

        for dd in obj.diseaseDetail.all():
            str = str + dd.rep_title + ' / '

        return str

    str_disease_detail.short_description = 'details'


admin.site.register(Disease,DiseaseAdmin)
admin.site.register(DiseaseDetail,DiseaseDetailAdmin)
admin.site.register(DiseaseDetailDivision,DiseaseDetailDivisionAdmin)
admin.site.register(LogEntry)