from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名: ', max_length=100)
    password = forms.CharField(label='密码: ', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件: ')

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名: ', max_length=100)
    password = forms.CharField(label='密码: ', widget=forms.PasswordInput())

def home(request):
    return render(request, 'index.html')
def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            #将表单写入数据库
            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()
            #返回注册成功页面
            return render(request, 'success.html',{'username':username})
    else:
        uf = UserForm()
    return render(request, 'register.html',{'uf':uf})

def login(request):
    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if(lf.is_valid()):
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['username']
            user = authenticate(username=username, password=password)
            if user is not None:
                msg = user.username + ' login Success'
            else:
                msg = 'Username or password wrong'
        else:
            msg = 'Internal Error'
        return render(request, 'msg.html', {'msg':msg})
    else:
        lf = LoginForm()
    return render(request, 'login.html', {'lf':lf})
