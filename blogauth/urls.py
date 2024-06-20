from django.urls import path

from . import views

app_name = 'blogauth'
urlpatterns = [
    path('login', views.bloglogin, name='login'),
    path('logout', views.bloglogout, name='logout'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_capcha, name='email')

]