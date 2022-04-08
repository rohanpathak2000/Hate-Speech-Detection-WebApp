from django.shortcuts import render

# Create your views here.

def register(request):
    ## Register code
    ## If username already exists
        ## Redirect back to signin with message
    ## else
        ## Redirect to home

    return render(request,'register.html')




