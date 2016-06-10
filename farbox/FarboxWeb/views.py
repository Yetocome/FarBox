from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout as logout_user
from django.http import HttpResponse, HttpResponseRedirect
from . import FileManager
from .models import VirtualFile, ShareInfo, RealFile
from .forms import LoginForm, RegistrationForm, UploadForm
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
from . import ShareManager
import mimetypes
from django.utils.encoding import smart_str
import os
# Create your views here.


    
def index(request):
    if request.user.is_authenticated():
        return redirect('FarboxWeb:home')
    else:
        return redirect('FarboxWeb:login')


def register(request):
    if request.user.is_authenticated():
        logout_user(request)
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            FileManager.create_user_root_dir(user.username)
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
    if request.user.is_authenticated():
        logout_user(request)
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if(form.is_valid()):
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            login_user(request, form.get_user())
            return redirect(request.GET['next'])
        else:
            msg = "用户名和密码不匹配!"
            return render(request, 'login.html', {
                'form':form,
                'msg':msg,
            })
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form,})


@login_required
def home(request):
    username = request.user.get_username()
    try:
        files = VirtualFile.objects.get(parent_id=0, path_name=username)
    except:
        files = VirtualFile(parent_id=0, path_name=username)
        files.save()
    files = VirtualFile.objects.filter(parent_id=files.path_id)
    return render(request, 'home.html', {
        'username': username,
        'files':files,
    })


@login_required
def share_file(request):
    username = request.user.get_username()
    fileid = request.GET['fileid']
    share_info = ShareManager.generate_share_info(fileid)
    share_info.save()
    return render(request, 'share_key.html', {
        'username': username,
        'share_key':share_info.share_key,
    })


@login_required
def share_page(request):
    share_key = request.GET['share_key']
    share_info = ShareInfo.objects.get(pk=share_key)
    file = VirtualFile.objects.get(path_id=share_info.path_id)
    return render(request, 'share_page.html', {
        'username':request.user.get_username(),
        'file':file,
        'share_key':share_key
    })


@login_required
def save_to_mine(request):
    share_key = request.GET['share_key']
    share_info = ShareInfo.objects.get(pk=share_key)
    virtualfile = VirtualFile.objects.get(path_id=share_info.path_id)
    realfile = RealFile.objects.get(file_hash=virtualfile.realfilename)
    FileManager.save_virtual_file(realfile, request.user.get_username())
    return redirect('FarboxWeb:home')


@login_required
def logout(request):
    logout_user(request)
    return redirect('FarboxWeb:index')


@login_required
def upload(request):

    if not request.user.is_authenticated():
        return HttpResponse("you are not logged in")
    if request.method == 'POST':
        try:
            f = request.FILES['file']
        except:
            return redirect('FarboxWeb:upload')
        FileManager.handle_upload_file(f, request.user.get_username())

        return redirect('FarboxWeb:home')
        #return HttpResponse(request.FILES['file'].name + " SIZE: " + str(request.FILES['file'].size))
    else:
        upload_form = UploadForm()
        return render(request, 'upload.html', {'upload_form':upload_form, 'username':request.user.get_username()})


@login_required
def delete_file(request):
    FileManager.delete_file(request.GET['fileid'])
    return redirect('FarboxWeb:home')


def download(request):
    FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'UPLOAD_FILES')
    rf = VirtualFile.objects.get(path_id=request.GET['fileid'])
    filename = os.path.join(FILE_PATH, rf.realfilename)
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = ('attachment; filename=%s' % rf.path_name).encode('utf-8')
    return response
