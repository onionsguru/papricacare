from django.contrib import admin

# Register your models here.

from .models import *


class HospitalAdmin(admin.ModelAdmin):
    model = Hospital
    list_display = ('id','name','sigungu','class_name')
    list_filter = ('class_name','maching_flag')
    search_fields = ('name','address')

class MedicalSpecialtyAdmin(admin.ModelAdmin):
    model = MedicalSpecialty
    list_display = ('id','hospital','m_specialty_name','doctor_num','cdiag_dr_num')
    # search_fields = ('hospital__name',)

class DoctorAdmin(admin.ModelAdmin):
    model = Doctor
    search_fields = ('name','hospital')
    autocomplete_fields = ('hospital',)

admin.site.register(Hospital,HospitalAdmin)
admin.site.register(MedicalSpecialty,MedicalSpecialtyAdmin)
admin.site.register(Doctor,DoctorAdmin)
