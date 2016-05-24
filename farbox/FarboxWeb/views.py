from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout as logout_user
from django.http import HttpResponse, HttpResponseRedirect
from . import FileManager
from .models import VirtualFile
from .forms import LoginForm, RegistrationForm, UploadForm
# Create your views here.


    
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            messages.info(request, '注册成功!')
            return redirect('FarboxWeb:index')
        return render(request, 'register.html', {
            'form':form,
        })
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {
            'form':form,
        })


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if(form.is_valid()):
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)

            login_user(request, form.get_user())
            return redirect('FarboxWeb:index')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form,})


def upload(request):
    if not request.user.is_authenticated():
        return HttpResponse("you are not logged in")
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        realfilename = FileManager.handle_upload_file(request.FILES['file'])

        return HttpResponse(request.FILES['file'].name + " SIZE: " + str(request.FILES['file'].size))
    else:
        upload_form = UploadForm()
        return render(request, 'upload.html', {'upload_form':upload_form, 'username':request.user.get_username()})