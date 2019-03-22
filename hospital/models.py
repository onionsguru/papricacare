from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Hospital(TimeStampedModel):

    #심평원정보
    ykiho = models.CharField(max_length=600)
    name = models.CharField(max_length=100, default='', blank=True)
    class_code  = models.IntegerField(null=True)
    class_name = models.CharField(max_length=100, default='', blank=True)
    sido = models.CharField(max_length=100, default='', blank=True)
    sido_code = models.IntegerField(null=True)
    sigungu = models.CharField(max_length=100, default='', blank=True)
    sigungu_code = models.IntegerField(null=True)
    bname = models.CharField(max_length=100, default='', blank=True)
    postalcode = models.IntegerField(null=True)
    address = models.CharField(max_length=1000, default='', blank=True)
    x_pos = models.CharField(max_length=50, default='', blank=True)
    y_pos = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=100, default='', blank=True)
    web = models.CharField(blank=True, default="", max_length=1000)
    est_date = models.CharField(max_length=100, default='', blank=True)
    closed_date = models.CharField(max_length=100, default='', blank=True)
    total_doctor_num = models.IntegerField(null=True)
    gp_num = models.IntegerField(null=True)
    intern_num = models.IntegerField(null=True)
    regident_num = models.IntegerField(null=True)
    specialist_num = models.IntegerField(null=True)
    exist_weekly_em = models.BooleanField(default=False)
    weekly_em_phone1 = models.CharField(max_length=100, default='', blank=True)
    weekly_em_phone1 = models.CharField(max_length=100, default='', blank=True)
    exist_night_em = models.BooleanField(default=False)
    night_em_phone1 = models.CharField(max_length=100, default='', blank=True)
    night_em_phone2 = models.CharField(max_length=100, default='', blank=True)
    weekly_rcv_time = models.CharField(max_length=100, default='', blank=True)
    sat_rcv_time = models.CharField(max_length=100, default='', blank=True)
    weekly_lunch_time = models.CharField(max_length=100, default='', blank=True)
    sat_lunch_time = models.CharField(max_length=100, default='', blank=True)
    holiday_close_info = models.CharField(max_length=100, default='', blank=True)
    sunday_close_info = models.CharField(max_length=100, default='', blank=True)
    etc_info = models.CharField(max_length=500, default='', blank=True)

    avail_parking_car_num = models.IntegerField(null=True)
    avail_parking = models.BooleanField(default=False)

    mon_open_time = models.CharField(blank=True, default="", max_length=50)
    mon_close_time = models.CharField(blank=True, default="", max_length=50)
    tue_open_time = models.CharField(blank=True, default="", max_length=50)
    tue_close_time = models.CharField(blank=True, default="", max_length=50)
    wed_open_time = models.CharField(blank=True, default="", max_length=50)
    wed_close_time = models.CharField(blank=True, default="", max_length=50)
    thu_open_time = models.CharField(blank=True, default="", max_length=50)
    thu_close_time = models.CharField(blank=True, default="", max_length=50)
    fri_open_time = models.CharField(blank=True, default="", max_length=50)
    fri_close_time = models.CharField(blank=True, default="", max_length=50)
    sat_open_time = models.CharField(blank=True, default="", max_length=50)
    sat_close_time = models.CharField(blank=True, default="", max_length=50)
    sun_open_time = models.CharField(blank=True, default="", max_length=50)
    sun_close_time = models.CharField(blank=True, default="", max_length=50)
    holi_open_time = models.CharField(blank=True, default="", max_length=50)
    holi_close_time = models.CharField(blank=True, default="", max_length=50)

    #국립중앙의료원 정보
    hpid = models.CharField(max_length=600, blank=True, null=True)
    dutydiv = models.CharField(max_length=20, blank=True, null=True)
    dutydivnam = models.CharField(max_length=100, blank=True, null=True)
    dutyemcls = models.CharField(max_length=100, blank=True, null=True)
    dutyemclsname = models.CharField(max_length=100, blank=True, null=True)
    dutyeryn = models.CharField(max_length=100, blank=True, null=True)
    dutyetc = models.CharField(max_length=300, blank=True, null=True)
    dutyinf = models.CharField(max_length=600, blank=True, null=True)
    dutymapimg = models.CharField(max_length=500, blank=True, null=True)
    dutytel3 = models.CharField(max_length=100, blank=True, null=True)
    rnum = models.CharField(max_length=50, blank=True, null=True)
    maching_flag = models.BooleanField(default=False)


    class Meta:
        verbose_name = '병원'
        verbose_name_plural = '병원 목록'

    def __str__(self):
        return self.name + '/'+ self.sigungu

class MedicalSpecialty(TimeStampedModel):
    hospital = models.ForeignKey(Hospital, related_name='hospital_specialties',on_delete=models.CASCADE)
    cdiag_dr_num = models.IntegerField()
    m_specialty_code = models.IntegerField()
    m_specialty_name = models.CharField(max_length=20)
    doctor_num = models.IntegerField()

    class Meta:
        verbose_name = '진료과목'
        verbose_name_plural = '진료과목 목록'
        ordering = ['id', ]


class Doctor(TimeStampedModel):
    doctor_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, related_name='hospital_doctors', on_delete=models.SET_NULL, null=True, blank=True)
    medical_specialty = models.CharField(max_length=100, blank=True, null=True)
    specialty_license = models.CharField(max_length=100, blank=True, null=True)
    medical_school = models.CharField(max_length=100, blank=True, null=True)
    graduate_year = models.IntegerField(blank=True, null=True)
    academic_association = models.CharField(max_length=100, blank=True, null=True)
    career = models.CharField(blank=True, default="", max_length=1000)

    class Meta:
        verbose_name = '의사'
        verbose_name_plural = '의사 목록'

    def __str__(self):
        if self.hospital != None:
            return str(self.doctor_number) + '/' + self.name + '(' + self.hospital.name + ')'
        else:
            return str(self.doctor_number) + '/' + self.name




