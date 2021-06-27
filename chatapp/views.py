from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from chatapp.forms import Profileform, Userform
from django.contrib import messages
from .models import Messagepublic,Message, Profile,Thread
import random
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
from django.db.models import Count
import os
global s_num1,s_num2,s_num3,arr,arr1
arr=[[0,0,0]]
# Create your views here.
def getcaptcha():
    global arr,arr1
    arr1=arr.pop(0)
    num1=random.randrange(1,10)
    num2=random.randrange(1,10)
    num3=num1+num2
    global s_num1,s_num2,s_num3
    s_num1=num1
    s_num2=num2
    s_num3=num3
   
    
    return s_num1,s_num2,s_num3,arr1
def login(request):
    
    x,y,z,arr1=getcaptcha()
    arr.append([x,y,z])
    print(x,y,z,arr,arr1,'first--------------------------------------------------')
    return render(request,'login.html',{'cap1':s_num1,'cap2':s_num2})

def signup(request):
    return render(request,'signup.html')

def enter(request):
    username=request.POST['username']
    passw=request.POST['password']
    captcha=request.POST.get('captcha')
    global arr1
    print(s_num1,s_num2,s_num3, arr1 ,'second--------------------------------------------------')
    if int(captcha)==arr1[2]:
        arr=[]
        user =auth.authenticate(username=username,password=passw)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,"Sorry! Account does not Exist.")
            return redirect('/')
    else:
        arr=[]
        messages.info(request,"OOPS! Wrong Captcha")
        return redirect('/')


def register(request):
    if request.method=="POST":
        email=request.POST['email']
        pass1=request.POST['password']
        pass2=request.POST['password1']
        username=request.POST['username']
        

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                 messages.info(request,"Username already used. !!")
                 return render (request,"signup.html")
            
            if User.objects.filter(email=email).exists():
                    messages.info(request,"Email address already used. !!")
                    return render (request,"signup.html")
                
            else:
                user=User.objects.create_user(email=email,password=pass1,username=username)
                
                user.save()
                profile=Profile(user=user,status='False')
                profile.save()
                messages.info(request,"Congratulations your account is created successfully. !")
                return redirect("/")

        else:
            messages.info(request,"OOPS! Password is not matching.")
    return redirect('login')
@login_required(login_url="login")
def index(request):
    details=request.user
    
  
    return render (request,"index.html",{'details':details})
@login_required(login_url="login")
def index1(request):
    return redirect('index')

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect('/')
@login_required(login_url="login")
def logout1(request):
    return redirect('logout')
@login_required(login_url="login")
def searching(request):
    if request.method=='GET':
        user=request.GET['search']
        details=User.objects.filter(username__icontains=user)

        if details:

            return render (request,"asearch.html",{'details':details})
        else:
            details1=User.objects.filter(email__exact=user)
            
            if details1:
                
                return render (request,"asearch.html",{'details':details1})
            else:
                messages.info(request,"Sorry !! No such User Exist")
                return redirect('index')
@login_required(login_url="login")
def edit_user(request,id):
    user1=request.user
    object=Profile.objects.get(user=user1)
    return render(request,'edit_user.html',{'object':object})


@login_required(login_url="login")
def update_user(request,id):
    user1=request.user
    object=Profile.objects.get(user=user1)
    
    if request.method=='POST':
        form=Userform(request.POST,instance=user1)
        form1=Profileform(request.POST,request.FILES,instance=object)
        if form.is_valid():
            if form1.is_valid():
                form1.save()
            else:
                messages.info(request,"Sorry !! Data didn't validate for form1")
            form.save()

        return redirect('index')
    else:
        messages.info(request,"Sorry !! Data didn't validate")
        return redirect('index')


@login_required(login_url="login")
def room(request,room_name):
    
    messages=reversed(Messagepublic.objects.all().order_by('-date')[0:2])
    return render(request,'chatroom.html',{
      
        'room_name':room_name,
        'messages':messages
    })

@login_required(login_url="login")
def deletemessage(request,pk):
        
        Messagepublic.objects.filter(id=pk).delete()
        return redirect(room,room_name="chatroom")



@login_required(login_url="login")
def room1(request,username):
    
    user2=User.objects.get(username=username)
    user1=request.user
    threads=Thread.objects.get_or_create_personal_thread(user1, user2)
    count=Count('users')
    
    profile2=Profile.objects.get(user=user2)
    #print(threads,threads.id,count,profile2.status,'---------------------------------------------------------------------------------------------------------')
    if profile2.status == False:

        #room_name='personal_thread_'+str(obj.id)
        messages=reversed(Message.objects.filter(thread=threads.id).order_by('-date')[0:2])
        return render(request,'personal_chatroom.html',{'seconduser':username,'messages':messages,'status':'Offline'})
    else:
        messages=reversed(Message.objects.filter(thread=threads.id).order_by('-date')[0:2])
        return render(request,'personal_chatroom.html',{'seconduser':username,'messages':messages,'status':'Online'})
@login_required(login_url="login")
def deletepersonalmessage(request,username,pk):
        
        Message.objects.filter(id=pk).delete()
        return redirect(room1,username=username)