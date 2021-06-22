from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from chatapp.forms import Userform
from django.contrib import messages
from .models import Message

# Create your views here.
def login(request):
    return render(request,'login.html')

def enter(request):
    username=request.POST['username']
    passw=request.POST['password']

    user =auth.authenticate(username=username,password=passw)
    if user is not None:
        auth.login(request,user)
        return redirect('index')
    else:
        messages.info(request,"Sorry! Account does not Exist.")
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
                return render (request,"login.html")

        else:
            messages.info(request,"OOPS! Password is not matching.")
    return redirect('login')

def index(request):
    details=request.user
  
    return render (request,"index.html",{'details':details})

def index1(request):
    return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def logout1(request):
    return redirect('logout')
    
def searching(request):
    if request.method=='GET':
        user=request.GET['search']
        details=User.objects.filter(username__icontains=user)
     
        if details:

            return render (request,"asearch.html",{'details':details})
        else:
            messages.info(request,"Sorry !! No such User Exist")
            return redirect('index')

def edit_user(request,id):
    
    object=request.user
    return render(request,'edit_user.html',{'object':object})

def update_user(request,id):
    object=User.objects.get(id=id)
    form=Userform(request.POST,instance=object)
    if form.is_valid():
        form.save()
        return redirect('index')
    else:
        messages.info(request,"Sorry !! Data didn't validate")
        return redirect('index')



def room(request,room_name):
    
    messages=Message.objects.all()[0:25]
    return render(request,'chatroom.html',{
      
        'room_name':room_name,
        'messages':messages
    })


