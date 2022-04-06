from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Meta:
        db_table = "user"
    
    username = models.CharField(max_length=128, unique=True, null=False, blank = False,default='', verbose_name='아이디')
    #password 비밀번호
    age = models.IntegerField(default=0, null = True, blank = True, verbose_name='나이')

    #기업
    #email 이메일
    ceoname = models.CharField(max_length=50, default='',null = True,blank = True,verbose_name='대표자성명',unique=False)
    company_name = models.CharField(max_length=50, default='',null = True,blank = True, verbose_name='기업이름')
    registration_number = models.CharField(max_length=10, default='',null = True,blank = True, verbose_name='사업자등록번호')
    dt_started = models.DateTimeField(null = True,blank = True,verbose_name='개업일자')
    is_company = models.BooleanField(default=False, verbose_name='기업판단')
    
    def __str__(self):
        return self.username



    