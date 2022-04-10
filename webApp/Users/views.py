from contextlib import redirect_stderr
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
# Create your views here.
from django.contrib import messages

def registerUser(request):
    if request.method == 'POST':
        username = request.POST['uname']
        pwd = request.POST['psw']
        email = request.POST['email']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        if User.objects.filter(username = username).exists():
            print("Username taken")
            messages.info(request,'Username already taken')
            return redirect('/register')
        elif User.objects.filter(email = email).exists():
            print("Email taken")
            messages.info(request,'Email Taken')
            return redirect('/register')
        else:
            user = User.objects.create_user(username = username,
                                        password = pwd,
                                        email = email,
                                        first_name = fname,
                                        last_name = lname
            )
            user.save()
            print("User registered")
            auth.login(request,user)
            return redirect('/')
    else:
        return render(request,'register.html')

                                        

def login(request):
    if request.method == 'POST':
        uname = request.POST['user']
        pwd = request.POST['pass']
        user = auth.authenticate(username = uname, password = pwd)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Username or Password incorrect')
            return redirect('/login')
    else:
        return render(request,'signin.html')



def logout(request):
    auth.logout(request)
    return redirect('/')


