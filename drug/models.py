from django.db import models
from unittest.util import _MAX_LENGTH

MAX_SHORT_STR_DRUG  = 1500
MAX_LONG_STR_DRUG   = 10000
MAX_CODE_STR        = 9

# Create your models here.

class IngreDesc(models.Model):
    desc_id = models.CharField(primary_key = True, max_length = MAX_SHORT_STR_DRUG, default='TBD')
    ingredient_name = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD')
    translate_status = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD')
    one_liner = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD')
    one_liner_kr = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD')
    bottom_line_en = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    bottom_line_kr = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    upside_en = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    upside_kr = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    downside_en = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    downside_kr = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    mechnism_en = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    mechnism_kr = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    pharmacist_tips = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')
    pharmacist_tips_kr = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD')

    def __str__(self):
        return self.desc_id  

class IngreForm(models.Model):
    ing_form_id = models.CharField(primary_key = True, max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    ing_name_eng = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    ing_name_kr = models.CharField( max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    form = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    desc_id = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    note = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    ing_id = models.ForeignKey(IngreDesc, related_name='forms', on_delete=models.CASCADE, blank=True, null=True) 
  
    def __str__(self):
        return self.ing_form_id     

class Ingredient(models.Model):
    ing_code = models.CharField(primary_key = True, max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    ing_form_id = models.ForeignKey(IngreForm, related_name='ingres', on_delete=models.CASCADE, blank=True, null=True)
   
    def __str__(self):
        return self.ing_code     

class Registration(models.Model):
    reg_code = models.CharField(primary_key = True, max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    ing_code = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    drug_name = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD') 
    drug_class = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    storage = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    exp_date = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    attach = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD') 
    look = models.CharField(max_length = MAX_LONG_STR_DRUG, default='TBD') 
    manufac_id = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    manufacturer = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    img_file = models.CharField(max_length = MAX_SHORT_STR_DRUG, default='TBD') 
        
    def __str__(self):
        return self.reg_code     
    
class Product(models.Model):
    prod_code = models.CharField(primary_key = True, max_length = MAX_SHORT_STR_DRUG, default='TBD') 
    reg_code = models.ForeignKey(Registration, related_name='drugs', on_delete=models.CASCADE, blank=True, null=True)
    ing_code = models.ForeignKey(Ingredient, related_name='drugs', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.prod_code
