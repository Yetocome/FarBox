from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from . import FileManager
from .models import VirtualFile
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名: ', max_length=100)
    password = forms.CharField(label='密码: ', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件: ')

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名: ', max_length=100)
    password = forms.CharField(label='密码: ', widget=forms.PasswordInput())

class UploadForm(forms.Form):
    file = forms.FileField(label='文件名', max_length=200)
    
def index(request):
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

            #创建一个用户相关的VirtulFile
            user_root_path = VirtualFile(path_name=username)
            user_root_path.save()
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
                if user.is_active:
                    auth_login(request, user)
                    msg = user.username + ' login Success'
            else:
                msg = 'Username or password wrong'
        else:
            msg = 'Internal Error'
        return render(request, 'msg.html', {'msg':msg})
    else:
        lf = LoginForm()
        return render(request, 'login.html', {'lf':lf})



def upload(request):
    if not request.user.is_authenticated():
        return HttpResponse("you are not logged in")
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        FileManager.handle_upload_file(request.FILES['file'])
        return HttpResponse(request.FILES['file'].name + " SIZE: "  + str(request.FILES['file'].size))
    else:
        upload_form = UploadForm()
        return render(request, 'upload.html', {'upload_form':upload_form, 'username':request.user.get_username()})