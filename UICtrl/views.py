from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth,AnonymousUser
from django.contrib import messages
def home(request):
    return render(request,'home.html',{'user':request.user})


def loginn(request):
    if request.method=='POST':
        username,password=request.POST['email'],request.POST['password1']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.info(request,'Authenticated!')
            return render(request,'home.html')
        else:
            messages.info(request,'invalid credentials')
        return redirect('/')
    else:
        return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        print(f'data => {request.POST}')
        firstName,lastName,password1,password2,email=request.POST['fname'],request.POST['lastname'],request.POST['password1'],request.POST['password2'],request.POST['email']
        print(f'signup called man',firstName,lastName,password1,password2,email)
        if password1==password2:
            if User.objects.filter(username=email).exists():
                messages.info(request,'username taken')
            else:
                user = User.objects.create_user(first_name=firstName,last_name=lastName,password=password1,username=email)
                user.save()
                return redirect('login')
                
                
        else:
            messages.info(request,'Password not matching!')


def Logout(request):
    auth.logout(request)
    return render(request,'home.html')

def is_logn(request):
    if request.user!=AnonymousUser():
        return True
    return False