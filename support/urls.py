from django.conf.urls import url
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('appupload/', views.appUpload, name='appupload'),
    path('fileupload/', views.fileUpload, name='fileupload'),
    path('mainpage/', views.main, name='mainpage'),
    path('my_page/',views.my_page,name="my_page"),
    path('corp_page/',views.corp_page, name='corp_page'),
    path('qna_manage/',views.qna_manage,name='qna_manage'),
    path('search/<str:app_name>/', views.search, name='search'),
    path('detail/<str:app_name>/', views.app_detail, name='app_detail'),
    path('qna/write/<str:app_name>/',views.qna_create,name='qna_create'), #질문 작성
    path('qna/detail/<str:app_name>/<int:qna_id>/',views.qna_detail,name='qna_detail'), #질문 상세 페이지
    path('qna/update/<str:app_name>/<int:qna_id>/',views.qna_update,name='qna_update'), #질문 수정 페이지    
    path('qna/delete/<str:app_name>/<int:qna_id>/',views.qna_delete,name='qna_delete'), #질문 수정 페이지    
    path('qnaboard/<str:app_name>/',views.qnaboard,name='qnaboard'),
    path('qnaboard/<str:app_name>/<str:search>',views.qnaboard_search,name='qnaboard_search'),
    path('qna/answer/',views.answer,name='answer'), #들어온 질문 관리 페이지    
    path('qna/answer/before/<str:app_name>/',views.answer_before,name='answer_before'), #답변 대기 목록 페이지    
    path('qna/answer/after/<str:app_name>/',views.answer_after,name='answer_after'), #답변 완료 목록 페이지    
    path('qna/answer/create/<str:app_name>/<int:qna_id>/',views.answer_create,name='answer_create'), # 답변 작성 페이지
    path('qna/answer/detail/<str:app_name>/<int:qna_id>/',views.answer_detail,name='answer_detail'), # 답변 볼 수 있는 페이지    
    path('qna/answer/update/<str:app_name>/<int:qna_id>/',views.answer_update,name='answer_update'), # 답변 수정    
    path('qna/answer/delete/<str:app_name>/<int:qna_id>/',views.answer_delete,name='answer_delete'), # 답변 삭제 
    path('category/<str:category>', views.category, name='category'),
    path('corp_page/edit<int:pk>',views.updateApp, name='appedit'),
    path('guideitem/<int:appId>', views.showGuide, name='guideitem'),
    path('filedelete/<str:funcName>/',views.deleteFile, name='filedelete'),
    path('guideline_preview/<int:appId>/<str:funcName>/',views.preview, name='preview'),
    path('user_guideline/<int:appId>/<str:funcName>/',views.guidelineview, name='guidelineview'),
    # path('appdetail/<int:app_id>/', views.appdetail, name='appdetail'),
    # path('appupdate/<int:app_id>/',views.updateApp, name='appupdate'),
    path('appdelete/<int:pk>/', views.deleteApp, name='appdelete'),
    # path('fileupdate/<int:guideline_id>/',views.updateFile, name='fileupdate'),
    # path('filedelete/<int:guideline_id>/', views.deleteFile, name='filedelete'),
]