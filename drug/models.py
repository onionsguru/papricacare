from django.db import models
from unittest.util import _MAX_LENGTH

MAX_SHORT_STR_DRUG  = 200
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
    name = models.CharField(max_length = MAX_SHORT_STR_DRUG)
    form = models.CharField(max_length = MAX_SHORT_STR_DRUG)
    desc = models.ForeignKey(IngreDesc, on_delete=models.CASCADE)
  
    def __str__(self):
        return self.name     

class Ingredient(models.Model):
    code = models.CharField(primary_key=True, max_length = MAX_CODE_STR)
    form = models.ForeignKey(IngreForm, on_delete=models.CASCADE)
  
    def __str__(self):
        return self.code     

class Registration(models.Model):
    code = models.CharField(primary_key=True, max_length = MAX_CODE_STR)
    drug_name = models.CharField(max_length = MAX_SHORT_STR_DRUG)
    drug_class = models.CharField(max_length = MAX_SHORT_STR_DRUG)
 
    def __str__(self):
        return self.code     

class Product(models.Model):
    code = models.CharField(primary_key=True, max_length = MAX_CODE_STR)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    def __str__(self):
        return self.code