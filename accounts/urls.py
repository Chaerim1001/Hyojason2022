from django.urls import path
from . import views


urlpatterns = [
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('sign_up/company', views.sign_up_com_view, name='sign-up-company'),
    path('sign_up/user', views.sign_up_user_view, name='sign-up-user'),
    path('id_check/', views.id_check, name='id-check'),  
    path('corpnum_check/',views.corp_check, name='corpnum-check'),
    path('logout/', views.logout, name='logout'),
    path('my_page/', views.my_page, name='my_page'),
]