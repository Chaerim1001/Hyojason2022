from django.conf import settings
from django.db import models
from accounts import models as accounts_models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

#앱 테이블
class App(models.Model):

    CATEGORY_NAME= (
    ('media', '동영상 및 사진 서비스'),
    ('sns', '소통 서비스'),
    ('benefit', '혜택 서비스'),
    ('shopping','쇼핑 서비스'),
    ('finance', '금융 서비스'),
    ('health','건강 서비스'),
    ('map','지도 서비스'),
    ('others','기타 서비스')
)
    class Meta:
        db_table='app'
    appId=models.AutoField(primary_key=True)
    companyId=models.ForeignKey(accounts_models.User, on_delete=models.CASCADE, db_column='id', default='')
    appName=models.CharField(max_length=128, null=True, default='',db_column='appName')
    appImage=models.ImageField(blank=True, upload_to='', null=True, db_column='appImage')
    appExplain=models.TextField(db_column='explain', null=True)
    category=models.CharField(max_length=50, choices=CATEGORY_NAME)
    hits=models.PositiveIntegerField(default=0, verbose_name='조회수', db_column='hits')

    def __str__(self):
        return self.appName
    
    def get_image_url(self):
        return '%s%s' %(settings.MEDIA_URL, self.appImage)




#가이드라인 테이블
class Guideline(models.Model):
    class Meta:
        db_table= 'guideline'
    
    guideId=models.AutoField(primary_key=True)
    appId=models.ForeignKey(App, on_delete=models.CASCADE, db_column='appId',default='')
    images=models.ImageField(blank=True, upload_to="", null=True, db_column='images') #파일 업로드
    explain=models.TextField(db_column='explain', null=True)
    uploadDate=models.DateTimeField(auto_now_add=True, db_column='uploadDate')
    is_Basic= models.BooleanField(default=True)
    order=models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(255)])
    funcName=models.TextField(db_column='funcName', default='')
    orderName=models.TextField(db_column='orderName', default='')

    def __str__(self):
        return self.explain
    
    def get_image_url(self):
        return '%s%s' %(settings.MEDIA_URL, self.images)


#질문 테이블
class QnA(models.Model):
    class Meta:
        db_table='qna'
    qnaId=models.AutoField(primary_key=True)
    title=models.TextField(db_column='title', default='') 
    appId=models.ForeignKey(App, on_delete=models.CASCADE, db_column='appId',default='') #SET_NULL설정 맞을지 고민
    q_personId=models.ForeignKey(accounts_models.User, on_delete=models.CASCADE, db_column='personId')
    question=models.TextField(db_column='question') #음성 혹은 텍스트인데..
    answer=models.TextField(db_column='answer', null=True)
    qDate=models.DateTimeField(auto_now_add=True, db_column='qDate')
    # aDate=models.DateTimeField(db_column='aDate', null=True)
    checkAnswer=models.BooleanField(db_column='checkAnswer', default=0)


