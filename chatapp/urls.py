from django.urls import path,include
from django.conf.urls import url
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('',views.login, name="login"),
    path('enter',views.enter, name="enter"),
    path('signup',views.signup,name="signup"),
    path('register',views.register, name="register"),
    path('index',views.index,name="index"),
    path('logout',views.logout,name='logout'),
    path('searching',views.searching,name='searching'),
    path('edit_user/<int:id>',views.edit_user,name="edit_user"),
    path('update_user/<int:id>',views.update_user,name="update_user"),
    path('chatroom/index1',views.index1,name='index1'),
    path('chatroom/logout1',views.logout1,name='logout1'),
    path('<str:room_name>/',views.room,name='room'),
    path('personal/<str:username>/',views.room1,name='room1'),
    path('chatroom/<int:pk>/', views.deletemessage,name="deletemessage"),
    path('personal/<str:username>/<int:pk>/', views.deletepersonalmessage,name="deletepersonalmessage"),
    #path('mediaupload')
]