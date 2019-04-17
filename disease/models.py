from django.db import models

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    jihog = 3

    class Meta:
        abstract = True

class DiseaseDetailDivision(TimeStampedModel):
    div_name = models.CharField(max_length=300)

    def __str__(self):
        return self.div_name

    class Meta:
        verbose_name = '질병 설명 분류'
        verbose_name_plural = '질병 설명 분류 목록'

class DiseaseDetail(TimeStampedModel):
    one_liner = models.CharField(max_length=600, default="", blank=True)
    source = models.CharField(max_length=300, default='', blank=True)
    rep_title = models.CharField(max_length=300, default='', blank=True)
    rep_title_en = models.CharField(max_length=300, default='', blank=True)
    pcare_desc = models.TextField(blank=True, null=True)
    pcare_desc_en = models.TextField(blank=True, null=True)
    disease_detail_division = models.ForeignKey(DiseaseDetailDivision, on_delete=models.SET_NULL, null=True, blank=True)
    idx = models.IntegerField(blank=True, null=True)
    title1 = models.CharField(max_length=300, blank=True, null=True)
    desc1 = models.TextField(blank=True, null=True)
    title2 = models.CharField(max_length=300, blank=True, null=True)
    desc2 = models.TextField(blank=True, null=True)
    title3 = models.CharField(max_length=300, blank=True, null=True)
    desc3 = models.TextField(blank=True, null=True)
    title4 = models.CharField(max_length=300, blank=True, null=True)
    desc4 = models.TextField(blank=True, null=True)
    title5 = models.CharField(max_length=300, blank=True, null=True)
    desc5 = models.TextField(blank=True, null=True)
    title6 = models.CharField(max_length=300, blank=True, null=True)
    desc6 = models.TextField(blank=True, null=True)
    title7 = models.CharField(max_length=300, blank=True, null=True)
    desc7 = models.TextField(blank=True, null=True)
    title8 = models.CharField(max_length=300, blank=True, null=True)
    desc8 = models.TextField(blank=True, null=True)
    title9 = models.CharField(max_length=300, blank=True, null=True)
    desc9 = models.TextField(blank=True, null=True)
    title10 = models.CharField(max_length=300, blank=True, null=True)
    desc10 = models.TextField(blank=True, null=True)
    translate_flag = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = '질병 설명'
        verbose_name_plural = '질병 설명 목록'

    def __str__(self):
        return self.rep_title

class Disease(TimeStampedModel):
    one_liner = models.CharField(max_length=600, default="", blank=True)
    diseaseDetail = models.ManyToManyField(DiseaseDetail, related_name='diseases', blank=True)
    code = models.CharField(max_length=50, db_index=True)
    rep_code = models.CharField(max_length=100, default='')
    is_rep = models.BooleanField(default=False)
    name_kr = models.CharField(max_length=600, default='', db_index=True)
    name_en = models.CharField(max_length=600, blank=True, default='')

    class Meta:
        verbose_name = '질병'
        verbose_name_plural = '질병 목록'


    def __str__(self):
        return self.code + '/' + self.name_kr