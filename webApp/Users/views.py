from django.shortcuts import render
from django.contrib.auth.models import User,auth
# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['uname']
        pwd = request.POST['psw']
        email = request.POST['email']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        user = User.objects.create_user(username = uname,
                                        
                                        )
    return render(request,'register.html')




