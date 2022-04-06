from django import forms
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import  AppUploadForm, GuidelineForm, QnaForm
from .models import App, Guideline, QnA
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.messages import *
import accounts
from accounts.models import User
import os
from django.contrib import messages
from datetime import date, datetime, timedelta


def Index(request):
    #해당 앱이 맞는지 우선 확인 필요
    if not request.session.get('corp'):
        return redirect('/accounts/sign-in')
    #현재 로그인한 사용자가 앱의 주인이 맞는지 확인하는 것 필요
    
    all_app=App.objects.all().order_by("appId")
    all_guide=Guideline.objects.all().order_by("guideId")
    return render(request, 'support/index.html', {'app_list':all_app, 'guide_list':all_guide})

def main(request): #메인 페이지
    if request.method == "GET": #메인페이
        app=App.objects.all().order_by('-hits')[:5]
        content = {
            'media': "media",
            'sns':"sns",
            'benefit':"benefit",
            'shopping':"shopping",
            'finance':"finance",
            'health':'health',
            'map':"map",
            'others':"others",
        }
        content['app']=app
        if request.session.get('corp'): 
            corpId = request.session.get('corp')
            corp = User.objects.get(id=corpId)
            content['corp'] = corp
            content['user'] = False
            return render(request, 'support/user_home.html',content)
        elif request.session.get('user'): 
            userId = request.session.get('user')
            user = User.objects.filter(id=userId)
            content['corp'] = False
            content['user'] = user
            return render(request, 'support/user_home.html', content)
        else: 
            content['corp'] = False
            content['user'] = False
            return render(request, 'support/user_home.html',content)
    elif request.method == "POST": #검색
        app_name = request.POST.get('search_app')
        if not request.POST.get('search_app'):
            app_name=' '
        return redirect('search', app_name) 


def corp_page(request): #기업 페이지
    if request.user.is_authenticated and request.session.get('corp'): 
        if request.method == "GET":   
            corpId = request.session.get('corp')
            apps = App.objects.filter(companyId=corpId)
            return render(request, 'support/corp_home_list.html',{'apps':apps})
    else: #로그인 안되어있을 때
        return redirect('sign-in')

def my_page(request):
    if request.method=='GET':
        userId = request.session.get('user')
        if userId:
            user = User.objects.get(id=userId)
            qnas = QnA.objects.filter(q_personId=user)
            return render(request,'support/user_my_page.html',{'user':user, 'qnas':qnas})
        else:
            redirect('sign-in')

def search(request, app_name): #검색
    apps = App.objects.filter(appName__icontains=app_name) # 앱이름에 search가 포함되어 있는 레코드만 필터링
    content = {'apps': apps,
    'app_name': app_name
    }
    if request.session.get('corp'):
        corpId = request.session.get('corp')
        corp = User.objects.get(id=corpId)
        content['corp']=corp
        content['user']=False
    elif request.session.get('user'):
        userId = request.session.get('user')
        user = User.objects.filter(id=userId)
        content['corp'] = False
        content['user'] = user
    else:
        content['corp'] = False
        content['user'] = False
    return render(request, 'support/user_home_search.html', content)


def app_detail(request, app_name): 
    app = App.objects.get(appName=app_name)
    guidelines = Guideline.objects.filter(appId=app.appId)
    qnas = QnA.objects.filter(appId=app.appId)
    
    app.hits +=1
    app.save()
    
    filter_app=App.objects.filter(category=app.category).exclude(appName=app_name)
    similar_app=filter_app.order_by("?")[:3]
    
    content = {
         'app': app,
         'guidelines': guidelines,
         'qnas':qnas,
         'similar_app':similar_app,
    }
    
    if request.session.get('corp'): 
            corpId = request.session.get('corp')
            corp = User.objects.get(id=corpId)
            content['corp'] = corp
            content['user'] = False
            return render(request, 'support/app_detail.html',content)
    elif request.session.get('user'): 
            userId = request.session.get('user')
            user = User.objects.filter(id=userId)
            content['corp'] = False
            content['user'] = user
            return render(request, 'support/app_detail.html', content)
    else: 
            content['corp'] = False
            content['user'] = False
            return render(request, 'support/app_detail.html',content)

def category(request, category):
    apps = App.objects.filter(category=category).order_by('-hits')
    content = {'apps': apps,
    'category': category
    }
    if request.session.get('corp'):
        corpId = request.session.get('corp')
        corp = User.objects.get(id=corpId)
        content['corp']=corp
        content['user']=False
    elif request.session.get('user'):
        userId = request.session.get('user')
        user = User.objects.filter(id=userId)
        content['corp'] = False
        content['user'] = user
    else:
        content['corp'] = False
        content['user'] = False
    return render(request, 'support/user_home_category.html', content)


def qna_create(request,app_name): #질문 생성
    app = App.objects.get(appName = app_name)
    if app:
        if request.session.get('user'):
            if request.method == "GET":
                form = QnaForm()
                content = {
                    'form':form,
                    'app':app
                }
                if request.session.get('corp'):
                    corpId = request.session.get('corp')
                    corp = User.objects.get(id=corpId)
                    content['corp']=corp
                    content['user']=False
                elif request.session.get('user'):
                    userId = request.session.get('user')
                    user = User.objects.filter(id=userId)
                    content['corp'] = False
                    content['user'] = user
                else:
                    content['corp'] = False
                    content['user'] = False
                return render(request, 'support/user_question.html',content)
            elif request.method == "POST": #질문 작성
                new_qna = QnA()
                new_qna.appId = App.objects.get(appName = app_name)
                new_qna.title = request.POST.get('title')
                new_qna.question= request.POST.get('question')
                new_qna.q_personId= User.objects.get(id = request.session.get('user'))
                new_qna.save()
            return redirect('app_detail',app.appName)
            # return redirect('qna_detail', app_name, new_qna.qnaId)
        else: #로그인 안되어있으면 로그인 페이지로 이동
           
            return redirect('sign-in')


def qna_detail(request,app_name,qna_id): #질문보기
    app = App.objects.get(appName = app_name)
    if app:
        user = request.session.get('user')
        qna = QnA.objects.get(qnaId=qna_id)
        content =  {"app": app, "qna": qna, "user":True}
        if user:
            userId = User.objects.get(username=qna.q_personId).id
            if user == userId:
                if request.session.get('corp'):
                    corpId = request.session.get('corp')
                    corp = User.objects.get(id=corpId)
                    content['corp']=corp
                    content['user']=False
                elif request.session.get('user'):
                    userId = request.session.get('user')
                    user = User.objects.filter(id=userId)
                    content['corp'] = False
                    content['user'] = user
                else:
                    content['corp'] = False
                    content['user'] = False
                    return render(request, 'support/qna_detail.html',content)
        #다른 사람이 보는 질문           
        if request.session.get('corp'):
                    corpId = request.session.get('corp')
                    corp = User.objects.get(id=corpId)
                    content['corp']=corp
                    content['user']=False
        elif request.session.get('user'):
            userId = request.session.get('user')
            user = User.objects.filter(id=userId)
            content['corp'] = False
            content['user'] = user
        else:
            content['corp'] = False
            content['user'] = False 
        return render(request, 'support/qna_detail.html',content) 


def qna_delete(request,app_name,qna_id):
    app = App.objects.get(appName = app_name)
    user = request.session.get('user')
    if user:
        if app:
            qna = QnA.objects.get(qnaId = qna_id)
            qna.delete()
            return redirect('my_page')

    

def qna_update(request, app_name, qna_id):
    app = App.objects.get(appName = app_name)
    if request.method == 'GET':
        if app:
            user = request.session.get('user')
            qna = QnA.objects.get(qnaId=qna_id) 
            if user:
                userId = User.objects.get(username=qna.q_personId).id
                if user == userId:
                    content = {"app": app, "qna": qna}
                    if request.session.get('corp'):
                        corpId = request.session.get('corp')
                        corp = User.objects.get(id=corpId)
                        content['corp']=corp
                        content['user']=False
                    elif request.session.get('user'):
                        userId = request.session.get('user')
                        user = User.objects.filter(id=userId)
                        content['corp'] = False
                        content['user'] = user
                    else:
                        content['corp'] = False
                        content['user'] = False
                        return render(request, 'support/user_quest_edit.html',content)
    elif request.method == 'POST':
            qna = QnA.objects.get(qnaId=qna_id) 
            qna.title = request.POST.get('input_quest_title')
            qna.question = request.POST.get('question_text')
            qna.save()
            return redirect('qna_detail', app_name, qna_id) #수정 완료 후 답변 보기 페이지로s


def qna_manage(request):
    if request.session.get('corp'):
        corpId = request.session.get('corp')
        apps = App.objects.filter(companyId=corpId) #기업이 등록한 app 목록 불러오기
        return render(request, 'support/corp_quest_manage.html',{"apps": apps})  #앱 목록 보여주고 html에서 for문으로 앱 쭉 보여주기


def qnaboard(request,app_name):
    app = App.objects.get(appName = app_name)
    if app:
        if request.method == "GET":
            qnas = QnA.objects.filter(appId=app)
            content = {
                'app':app,
                'qnas':qnas
            }
            if request.session.get('corp'):
                corpId = request.session.get('corp')
                corp = User.objects.get(id=corpId)
                content['corp']=corp
                content['user']=False
            elif request.session.get('user'):
                userId = request.session.get('user')
                user = User.objects.filter(id=userId)
                content['corp'] = False
                content['user'] = user
            else:
                content['corp'] = False
                content['user'] = False
            return render(request, 'support/home_quest_board.html',content)
        elif request.method == "POST":
            search = request.POST.get('quest_search')
            return redirect('qnaboard_search', app_name,search) 


def qnaboard_search(request,app_name,search):
    app = App.objects.get(appName=app_name)
    qnas = QnA.objects.filter(title__icontains=search)
    content = {'qnas':qnas, 'app':app}
    if request.session.get('corp'):
        corpId = request.session.get('corp')
        corp = User.objects.get(id=corpId)
        content['corp']=corp
        content['user']=False
    elif request.session.get('user'):
        userId = request.session.get('user')
        user = User.objects.filter(id=userId)
        content['corp'] = False
        content['user'] = user
    else:
        content['corp'] = False
        content['user'] = False
    return render(request, 'support/qna_search.html', content)


def answer(request):
    if request.session.get('corp'):
        corpId = request.session.get('corp')
        apps = App.objects.filter(companyId=corpId) #기업이 등록한 app 목록 불러오기
        return render(request, 'support/corp_quest_manage.html',{"apps": apps})  #앱 목록 보여주고 html에서 for문으로 앱 쭉 보여주기


def answer_before(request, app_name):
    corpId = App.objects.get(appName = app_name).companyId
    print(corpId)
    if request.session.get('corp'):
        if request.method == 'GET':
            appId = App.objects.get(appName = app_name)
            qnas = QnA.objects.filter(appId=appId)
            qna = qnas.filter(checkAnswer=False)
            app = App.objects.get(appName = app_name)
            context = {
                "qnas":qna,
                "app":app
            }
            return render(request, 'support/answer_before.html',context)  #앱에 해당하는 질문목록 


def answer_after(request, app_name):
    if request.session.get('corp'):
        appId = App.objects.get(appName = app_name)
        qnas = QnA.objects.filter(appId=appId)
        qna = qnas.filter(checkAnswer=True)
        app = App.objects.get(appName = app_name)
        context = {
            "qnas":qna,
            "app":app
        }
        return render(request, 'support/answer_after.html',context)  #앱에 해당하는 질문목록 


def answer_create(request,app_name,qna_id):
        if request.session.get('corp'):
            if request.method == 'POST':
                qna = QnA.objects.get(qnaId=qna_id)
                qna.answer = request.POST.get('answer')
                qna.checkAnswer = True
                qna.save()
                return redirect('answer_detail', app_name, qna.qnaId)
            else: #GET
                qna = QnA.objects.get(qnaId=qna_id)
                if qna.checkAnswer == False: #질문 답변이 없을 때
                    app = App.objects.get(appName = app_name)
                    context = {
                        "qna":qna,
                        "app":app
                    }
                    return render(request, 'support/answer_create.html',context) #답변 적을수있는 페이지 주기
               

def answer_detail(request,app_name,qna_id):
    if request.session.get('corp'): 
        if request.method == 'GET':
            qna = QnA.objects.get(qnaId=qna_id) #해당 질문 데이터 가져오기
            app = App.objects.get(appName = app_name)
            context = {
                        "qna":qna,
                        "app":app
                    }
            return render(request, 'support/answer_detail.html',context)


def answer_update(request,app_name,qna_id):
    if request.session.get('corp'):
        qna = QnA.objects.get(qnaId=qna_id) #해당 질문 데이터 가져오기 
        app = App.objects.get(appName = app_name)
        context = {
                    "qna":qna,
                    "app":app
                }
        if request.method == 'GET': #수정하기 버튼 클릭해서 넘어왔을 때
            return render(request, 'support/answer_update.html', context)
        elif request.method == 'POST': #수정된 내용 저장할 때
            qna.answer = request.POST.get('answer')
            qna.save()
            return redirect('answer_detail', app_name, qna_id) #수정 완료 후 답변 보기 페이지로
            

def answer_delete(request,app_name,qna_id):
    if request.session.get('corp'):
        qna = QnA.objects.get(qnaId=qna_id) #해당 질문 데이터 가져오기 
        qna.answer = ' '
        qna.checkAnswer = False
        qna.save()
        return redirect('answer_after', app_name)


@login_required
def appUpload(request):
    if not request.session.get('corp'):
        return redirect('/accounts/sign-in')
    else:
        if request.method == 'POST':
            company=request.session.get('corp')
            appName=request.POST['appName']
            category=request.POST['category']
            appExplain=request.POST['appExplain']
            appImage=request.FILES.get('appImage')
            companyId=User.objects.get(id=company)
            app_upload_form=App(
                appName=appName,
                category=category,
                appExplain=appExplain,
                appImage=appImage,
                companyId=companyId
            )
            app_upload_form.save()
            return redirect('corp_page')
        else:
            app_upload_form=AppUploadForm()
            return render(request, 'support/appupload.html', {'app_upload_form':app_upload_form})
    
    
@login_required
def updateApp(request, pk):
    if request.session.get('corp') or request.user.is_authenticated:
        app=App.objects.get(appId=pk)
        if request.method == 'POST':
            if len(request.FILES) != 0:
                if len(app.appImage) >0:
                    os.remove(app.appImage.path)
                app.appImage=request.FILES['appimage']
            app.appName=request.POST.get('appName')
            app.category=request.POST.get('category')
            app.appExplain=request.POST.get('appExplain')
            app.save()
            return redirect('corp_page')
        context={'app':app, 'pk':pk}
        return render(request, 'support/corp_app_edit.html', context)
    else:
        return redirect('/accounts/sign-in')
    

def deleteApp(request, pk):
    if not request.session.get('corp'):
        return redirect('/accounts/sign-in')
    app=get_object_or_404(App, appId=pk)
    app.delete()
    return redirect('corp_page')


@login_required
def fileUpload(request):
    corpId = request.session.get('corp')
    if not corpId:
        return redirect('/accounts/sign-in')
    else:
        if request.method =='GET':
            apps = App.objects.filter(companyId = corpId)
            context={
                'apps': apps
            }
            return render(request, 'support/fileupload.html', context)
        else:  #post
            #반복문 사용
            count = 1
            while count <= 10:
                name = 'level_name' + str(count)
                explain = 'level_sent' + str(count)
                image = 'app_logo_upload_btn' + str(count)
                
                if request.POST.get(name):
                    guideline=Guideline()
                    appName = request.POST.get('app_select')
                    guideline.appId = App.objects.get(appName = appName)
                    try: 
                        guideline.images = request.FILES[image]
                    except: 
                        guideline.images=''
                    guideline.explain = request.POST.get(explain)
                    is_basic = request.POST.get('func_select')
                    if is_basic == 'basic_fun':
                        guideline.is_Basic = 0
                    else:
                        guideline.is_Basic = 1
                    guideline.order = 1
                    guideline.funcName = request.POST.get('func_name')
                    guideline.orderName = request.POST.get(name)
                    guideline.order = count
                    guideline.save()
                    print('완료')

                count += 1
        return redirect('mainpage')


def showGuide(request, appId):
    if request.user.is_authenticated and request.session.get('corp'): 
        if request.method == "GET":
            guideline=Guideline.objects.filter(appId=appId)
            app=App.objects.get(appId=appId)
            return render(request, 'support/corp_item_management.html',{'guideline':guideline, 'app':app, 'appId':appId})
    else: #로그인 안되어있을 때
        return redirect('sign-in')

    
def deleteFile(request, funcName):
    if request.user.is_authenticated and request.session.get('corp'): 
            guideline=Guideline.objects.filter(funcName=funcName)
            guideline.delete()
            return redirect('corp_page')
    else: #로그인 안되어있을 때
        return redirect('sign-in')

def preview(request, appId, funcName):
    if request.user.is_authenticated and request.session.get('corp'): 
        if request.method == "GET":
            guidelines=Guideline.objects.filter(appId=appId,funcName=funcName)
            app=App.objects.get(appId=appId)
            return render(request, 'support/corp_item_preview.html',{'guidelines':guidelines, 'app':app, 'funcName':funcName})
    else: #로그인 안되어있을 때
        return redirect('sign-in')

def guidelineview(request, appId, funcName):
    guidelines=Guideline.objects.filter(appId=appId,funcName=funcName)
    app=App.objects.get(appId=appId)
    content = {
        'app': app,
        'guidelines': guidelines,
    }
    if request.session.get('corp'): 
            corpId = request.session.get('corp')
            corp = User.objects.get(id=corpId)
            content['corp'] = corp
            content['user'] = False
            return render(request, 'support/user_guideline.html',content)
    elif request.session.get('user'): 
            userId = request.session.get('user')
            user = User.objects.filter(id=userId)
            content['corp'] = False
            content['user'] = user
            return render(request, 'support/user_guideline.html', content)
    else: 
            content['corp'] = False
            content['user'] = False
            return render(request, 'support/user_guideline.html',content)