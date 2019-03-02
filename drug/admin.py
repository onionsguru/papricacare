from django.contrib import admin
import drug

# Register your models here.
'''
class DrugInline(admin.TabularInline):
    model = drug.models.Drug
    extra = 2
'''
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code',)
    list_filter = []
    search_fields = ['code']
    
class RegistrationAdmin(admin.ModelAdmin):
    # fields = ['code', 'drug_name', 'drug_class']
    list_display = ('code', 'drug_name', 'drug_class')
    list_filter = ['drug_class']
    search_fields = ['code', 'drug_name']
    
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('code',)
    list_filter = []
    search_fields = ['code']
    
class IngreFormAdmin(admin.ModelAdmin):
    list_display = ('name','form','desc')
    list_filter = ['form']
    search_fields = ['name','desc']
    
class IngreDescAdmin(admin.ModelAdmin):
    list_display = ('desc_id', 'ingredient_name', 'translate_status', 'one_liner', 'one_liner_kr', 'bottom_line_en', 'bottom_line_kr', 'upside_en', 'upside_kr', 'downside_en', 'downside_kr', 'mechnism_en', 'mechnism_kr', 'pharmacist_tips', 'pharmacist_tips_kr')
    
    list_filter = []
    search_fields = []

admin.site.register(drug.models.Product, ProductAdmin)
admin.site.register(drug.models.Registration, RegistrationAdmin)
admin.site.register(drug.models.Ingredient, IngredientAdmin)
admin.site.register(drug.models.IngreForm, IngreFormAdmin)
admin.site.register(drug.models.IngreDesc, IngreDescAdmin)