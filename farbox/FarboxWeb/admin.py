from django.contrib import admin

# Register your models here.

from .models import RealFile, VirtualFile


admin.site.register(RealFile)
admin.site.register(VirtualFile)