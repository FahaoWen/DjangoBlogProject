from django.http.response import JsonResponse
from django.shortcuts import render, redirect
import string
import random
from django.core.mail import send_mail
from django.urls import reverse

from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .form import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User
# Create your views here.

User = get_user_model()
@require_http_methods(['GET', 'POST'])
def bloglogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                #login
                login(request, user)

                # check if remember
                if not remember:
                    #if did not set remember, set expire date be 0, session will expire after webpage close
                    request.session.set_expiry(0)
                    # if yes on remember, the session default expire in 2 week
                return redirect('/')
            else:
                print("Email or password error")

                return redirect(reverse('blogauth:login'))
        else:
            print(form.errors)
            print('form is not valid')
            return redirect(reverse('blogauth:login'))

def bloglogout(request):
    logout(request)
    return redirect('/')

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('blogauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('blogauth:register'))
            # go back to the register page after failed
            # return render(request, 'register.html', context={'form': form})

def send_email_capcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, "message": "You have to enter an email"})
    captcha = "".join(random.sample(string.digits, 4))
    # save the captcha to database, find the data with email, if email exist then update captcha, if not, then create
    CaptchaModel.objects .update_or_create(email = email, defaults = {'captcha': captcha})
    send_mail("Verify Code from Nick's Blog", message=f"Your verify code is: {captcha}", recipient_list=[email],
              from_email="NONE")
    return JsonResponse({'code': 200, 'message': 'Successfully sent email'})