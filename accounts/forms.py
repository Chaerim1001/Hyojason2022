from django import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from .models import *


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'id':'user_pw1','name':'userpwd1','required': 'true', 'placeholder': 'PASSWORD'}),
    )
    password2 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={'id':'user_pw2', 'name':'userpwd2','required': 'true', 'placeholder': 'PASSWORD', 'onchange':'check_pw()'}),
        strip=False,
    )

    class Meta: 
        model = User
        fields = ['username','age']
        labels = {"username": "", "age": ""}
        widgets = {
            'username': forms.TextInput(attrs={'class':'username_input','name':'userid','id':'userid','check_result':'fail', 'placeholder': 'ID', 'required': 'true'}),
            'age': forms.TextInput(attrs={'id':'birth','name':'birth', 'placeholder':'년(4자)', 'size':4, 'maxlength':4, 'required': 'true'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
   
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CorpForm(forms.ModelForm):
    password1 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'id':'corp_pw1','name':'corppwd1','required': 'true', 'placeholder': 'PASSWORD'}),
    )
    password2 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={'id':'corp_pw2', 'name':'corppwd2','required': 'true', 'placeholder': 'PASSWORD','onchange':'check_pw()'}),
        strip=False,
    )

    class Meta: 
        model = User
        fields = ['company_name','ceoname','dt_started','registration_number','username','email']
        labels = {"company_name":"",
        "ceoname":"",
        "dt_started":"",
        "registration_number":"",
        "username":"",
        "email":"",
         }
        widgets = {
            'company_name': forms.TextInput(attrs={'class':'username_input','name':'userid','id':'userid','check_result':'fail', 'placeholder': 'ID', 'required': 'true'}),
            'ceoname': forms.TextInput(attrs={'class':'username_input','name':'userid','id':'userid','check_result':'fail', 'placeholder': 'ID', 'required': 'true'}),

        }


