from django.contrib import admin
import drug

# Register your models here.
'''
class DrugInline(admin.TabularInline):
    model = drug.models.Drug
    extra = 2
'''
class ProductAdmin(admin.ModelAdmin):
    # PROD_CODE    REG_CODE    ING_CODE    durcode1 .. durcode4
    list_display = ('prod_code', 'reg_code', 'ing_code', 'durcode1', 'durcode2', 'durcode3', 'durcode4')
    list_filter = []
    search_fields = ['prod_code', 'reg_code', 'ing_code', 'durcode1', 'durcode2', 'durcode3', 'durcode4']
    
class RegistrationAdmin(admin.ModelAdmin):
    # REG_CODE    ING_CODE    DRUG_NAME    DRUG_CLASS    STORAGE    EXP_DATE    ATTATCH    LOOK    MANUFAC_ID    MANUFACTURER    IMG_FILE
    list_display = ('reg_code', 'ing_code', 'drug_name', 'drug_class', 'storage', 'exp_date', 
                    'attach', 'look', 'manufac_id','manufacturer', 'img_file')
    list_filter = ['drug_class', 'manufac_id', 'manufacturer' ]
    search_fields = ['reg_code', 'ing_code', 'drug_name',]
    
class IngredientAdmin(admin.ModelAdmin):
    # ING_CODE    ING_FORM_ID
    list_display = ('ing_code', 'ing_form_id')
    list_filter = []
    search_fields = ['ing_code']
    
class IngreFormAdmin(admin.ModelAdmin):
    # ING_FORM_ID    ING_NAME_ENG    ING_NAME_KR    FORM    DESC_ID    NOTE    ING_ID    CODE
    list_display = ('ing_form_id', 'ing_name_eng', 'ing_name_kr', 'form', 'desc_id', 'note', 'ing_id', 'code' )
    list_filter = ['form', 'code']
    search_fields = ['ing_form_id', 'ing_name_eng', 'ing_name_kr']
    
class IngreDescAdmin(admin.ModelAdmin):
    # list_display = ('desc_id', 'ingredient_name', 'translate_status', 'one_liner', 'one_liner_kr', 'bottom_line_en', 'bottom_line_kr', 'upside_en', 'upside_kr', 'downside_en', 'downside_kr', 'mechnism_en', 'mechnism_kr', 'pharmacist_tips', 'pharmacist_tips_kr')
    list_display = ('desc_id', 'ingredient_name', 'translate_status', 'one_liner_kr', 'bottom_line_kr', 'upside_kr', 'downside_kr', 'mechnism_kr')
    list_filter = ['translate_status']
    search_fields = ['ingredient_name', 'translate_status', 'one_liner', 'one_liner_kr', 'bottom_line_en', 'bottom_line_kr', 'upside_en', 'upside_kr', 'downside_en', 'downside_kr', 'mechnism_en', 'mechnism_kr', 'pharmacist_tips', 'pharmacist_tips_kr']

admin.site.register(drug.models.Product, ProductAdmin)
admin.site.register(drug.models.Registration, RegistrationAdmin)
admin.site.register(drug.models.Ingredient, IngredientAdmin)
admin.site.register(drug.models.IngreForm, IngreFormAdmin)
admin.site.register(drug.models.IngreDesc, IngreDescAdmin)
