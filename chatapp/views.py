from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from chatapp.forms import Userform
from django.contrib import messages
from .models import Message
import random
global s_num1,s_num2,s_num3
# Create your views here.
def login(request):
    num1=random.randrange(1,101)
    num2=random.randrange(1,101)
    num3=num1+num2
    global s_num1,s_num2,s_num3
    s_num1=str(num1)
    s_num2=str(num2)
    s_num3=str(num3)

    return render(request,'login.html',{'cap1':s_num1,'cap2':s_num2})

def enter(request):
    username=request.POST['username']
    passw=request.POST['password']
    captcha=request.POST.get('captcha')

    if s_num3==str(captcha):
        user =auth.authenticate(username=username,password=passw)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,"Sorry! Account does not Exist.")
            return redirect('/')
    else:
        messages.info(request,"OOPS! Wrong Captcha")
        return redirect('/')

def signup(request):
    return render(request,'signup.html')


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
                
                messages.info(request,"Congratulations your account is created successfully. !")
                return redirect("/")

        else:
            messages.info(request,"OOPS! Password is not matching.")
    return redirect('login')
@login_required
def index(request):
    details=request.user
  
    return render (request,"index.html",{'details':details})
@login_required
def index1(request):
    return redirect('index')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
@login_required
def logout1(request):
    return redirect('logout')
@login_required
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
@login_required
def edit_user(request,id):
    
    object=request.user
    return render(request,'edit_user.html',{'object':object})
@login_required
def update_user(request,id):
    object=User.objects.get(id=id)
    form=Userform(request.POST,instance=object)
    if form.is_valid():
        form.save()
        return redirect('index')
    else:
        messages.info(request,"Sorry !! Data didn't validate")
        return redirect('index')


@login_required
def room(request,room_name):
    
    messages=Message.objects.all()[0:50]
    return render(request,'chatroom.html',{
      
        'room_name':room_name,
        'messages':messages
    })


