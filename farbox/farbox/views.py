from django.http import HttpResponse

def home(request):
    return HttpResponse('Welcome, <a target="_blank" href="/logout/">logout</a>')