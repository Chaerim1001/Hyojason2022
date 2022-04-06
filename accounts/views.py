from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
import requests

from support.models import *
from support.forms import *

from .models import User
from django.contrib.auth import authenticate, get_user_model, login 
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
import json
from .forms import *
from django.contrib import messages


def sign_up_user_view(request): #사용자 회원가입
        if request.method == "GET":
            if request.user.is_authenticated and request.session.get('user'): #로그인 상태인지 확인
                return redirect('mainpage') #로그인 상태이면 메인페이지로 이동
            else:
                return render(request, 'accounts/register_user.html')
        elif request.method == "POST":
            username = request.POST.get('userid', None)
            password = request.POST.get('userpwd1', None)
            age = request.POST.get('birth', None)
            dt_started = request.POST.get('dt_started', None)
            is_company = False

            new_user = User.objects.create_user(
                username=username,
                password=password,
                age=age,
                dt_started=dt_started,
                is_company=is_company
                )
            new_user.save()
            return redirect('sign-in')


def sign_up_com_view(request): #기업 회원가입
        if request.method == "GET":
            if request.user.is_authenticated and request.session.get('corp'): #로그인 상태인지 확인
                return redirect('mainpage') #로그인 상태이면 메인페이지로 이동
            else: 
                return render(request, 'accounts/register_corp.html')
        elif request.method == "POST":
            username = request.POST.get('corpid', None)
            password = request.POST.get('corppwd1', None)
            company_name = request.POST.get('corp_app_name', None)
            ceoname = request.POST.get('corp_ceo', None)
            dt_started = request.POST.get('corp_date', None)
            registration_number = request.POST.get('corp_num', None)
            is_company = True

            new_user = User.objects.create_user(
                username=username,
                password=password,
                company_name=company_name,
                ceoname=ceoname,
                dt_started=dt_started,
                registration_number=registration_number,
                is_company=is_company
                )
            new_user.save()

            return redirect('sign-in')


def sign_in_view(request): #로그인
    if request.method == "GET":
        user_pk = request.session.get('user')
        if user_pk:
            return redirect('mainpage')
        return render(request, 'accounts/login.html')
    elif request.method == "POST" and 'sign_user' in request.POST: #사용자 로그임
        username = request.POST.get('userid', None) #get은 name 값으로 해야함
        password = request.POST.get('userpw', None)
        try: 
            exit_user = User.objects.get(username=username)
        except:
            messages.info(request, '아이디 및 비밀번호를 확인해주세요')
            return redirect('sign-in')
        if exit_user.is_company == False:
            user = auth.authenticate(request,
                username=username,
                password=password)
            if user is not None:
                request.session['user'] = user.id
                auth.login(request, user)
                messages.info(request, '로그인 성공')
                return redirect('mainpage')
            else:
                messages.error(request,'아이디 및 비밀번호를 확인해주세요')
                return redirect('sign-in')
        else: 
            messages.error(request,'아이디 및 비밀번호를 확인해주세요')
            return redirect('sign-in')


    elif request.method == "POST" and 'sign_corp' in request.POST: #기업 로그인

        username = request.POST.get('corpid', None) #get은 name 값으로 해야함
        password = request.POST.get('corpwd', None)
        try: 
            exit_user = User.objects.get(username=username)
        except:
            messages.info(request, '아이디 및 비밀번호를 확인해주세요')
            return redirect('sign-in')
        if exit_user.is_company: #기업 권한이 있는지 확인
            user = auth.authenticate(request,
                username=username,
                password=password)
            if user is not None:
                request.session['corp'] = user.id #세션 적용
                auth.login(request, user)
                messages.info(request, '로그인 성공!')
                return redirect('mainpage')
            else:
                messages.info(request, '아이디 및 비밀번호를 확인해주세요')
                return redirect('sign-in')
        else: 
            messages.info(request, '아이디 및 비밀번호를 확인해주세요')
            return redirect('sign-in')
    


def id_check(request): #id 중복확인
    try:
        user = User.objects.get(username=request.GET['userid'])
    except Exception as e:
        user = None
    result = {
        'result':'success',
        'data' : "not exist" if user is None else "exist"
    }
    print(result)
    return JsonResponse(result)


def corp_check(request): #사업자등록번호 확인 
    p_nm=request.GET.get('corp_ceo') #대표자성명
    dt_started=request.GET.get('corp_date') #개업일자
    corp_num=request.GET.get('corp_num') #사업자등록번호
    
    date = dt_started.split('-')
    dt_started = date[0] + date[1] + date[2]

    key="N0NCPrYe%2BLQCuhkVG8QzeUP3xSQH%2BLX381f2IOQe6Ky1JRp%2FbW3AQldf2ZGoNkvwlQmcPFhoHBv%2Bxex18MaTnw%3D%3D"
    url = "http://api.odcloud.kr/api/nts-businessman/v1/validate?serviceKey={}&returnType=JSON".format(key)
    headers = {'Content-type':'application/json; charset=utf-8'}
    data = {
    "businesses": [
        {
      "b_no": corp_num,
      "start_dt": dt_started,
      "p_nm": p_nm,
      "p_nm2": "",
      "b_nm": "",
      "corp_no": "",
      "b_sector": "",
      "b_type": ""
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    res = response.json()
    data = res['data'][0]
    print(data)
    result = {
        'result':'success',
        'data' : "not exist" if data['valid'] == '02' else "exist"
    }
    print(result)
    return JsonResponse(result)


def my_page(request): #사용자 마이 페이지
    if request.method == "GET":
        if request.session.get('user'): #로그인 상태인지 확인
            return render(request, 'accounts/mypage.html')
        else:
            return redirect('sign-in')

@login_required
def logout(request): #로그아웃
    auth.logout(request) #로그아웃하면 알아서 세션 삭제됨.
    return redirect('mainpage')