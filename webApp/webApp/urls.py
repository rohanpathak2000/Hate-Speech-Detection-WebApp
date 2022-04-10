from django.contrib import admin
from django.urls import path
from detection.views import storeValues
from Users.views import registerUser,login,logout
from detection.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('connect/',mainMethod),
    path('initialize/',storeValues),
    path('register/',registerUser),
    path('login/',login),
    path('logout/',logout),

    path('',home)

]
