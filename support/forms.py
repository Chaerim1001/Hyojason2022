from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxInput, RadioSelect, Select
from .models import Guideline, QnA,App


class GuidelineForm(ModelForm):
    
    class Meta:
        model=Guideline
        fields=['images', 'explain','funcName','orderName']
        widgets={
            'funcName': forms.TextInput(attrs={'id':'app_func_input', 'name':'func_name','placeholder':'Ex.채팅보내기'}),
            'orderName': forms.TextInput(attrs={'class':'level_name_input','placeholder':'Ex.네모박스를 클릭'}),
            'explain': forms.Textarea(attrs={'class':'level_input','style':'width: 190%; height: 70%;','placeholder':'단계에 대한 설명을 입력해주세요.'}),
            'images': forms.FileInput(attrs={}),
        }

class AppUploadForm(forms.ModelForm):
    class Meta:
        model=App
        category_Choices=(('media', '동영상 및 사진 서비스'), ('sns', '소통 서비스'), ('benefit', '혜택 서비스'), ('shopping', '쇼핑 서비스')
    , ('fincance', '금융 서비스'), ('health', '건강 서비스'), ('map', '지도 서비스'), ('etc', '기타 서비스'))
    
        fields=[
            'appName',
            'category',
            'appExplain',
            'appImage',
        ]
        widgets={
            'appName': forms.TextInput(attrs={'id':'app_name_input', 'name':'app_name', 'placeholder':'어플 이름 입력', 'required':'true'}),
            'appExplain':forms.TextInput(attrs={'id':'app_service_input','name':'app_explain', 'placeholder':'간단한 서비스 설명을 입력해주세요'}),
            'category':forms.Select(choices=category_Choices, attrs={'id':'category', 'name':'category'}),
            'appImaege':forms.FileInput(attrs={'id':'app_logo_upload_btn','name':'app_logo_upload_btn'})
        }
    
    # class Meta:
    #     model=App
        category_Choices=(('media', '동영상 및 사진 서비스'), ('sns', '소통 서비스'), ('benefit', '혜택 서비스'), ('shopping', '쇼핑 서비스')
    , ('fincance', '금융 서비스'), ('health', '건강 서비스'), ('map', '지도 서비스'), ('etc', '기타 서비스'))
    
    #     fields=[
    #         'appName',
    #         'category',
    #         'appExplain',
    #         'appImage',
    #     ]
    #     widgets={
    #         'category':Select(choices=category_Choices),
    #     }

class QnaForm(ModelForm):
    class Meta:
        model=QnA
        fields=['title','question']
        labels = {"title": "제목", "question": "질문내용"}
        widgets = {
            'title': forms.TextInput(attrs={'id':'input_quest_title','name':'input_quest_title','placeholder':'제목을 입력해주세요','style':'margin-bottom:10px', 'required': 'true'}),
            'question': forms.Textarea(attrs={'name':'question_text','style':'width:100%;font-size:30px; border:0;word-break: keep-all;','rows':'13', 'required': 'true'}),
        }