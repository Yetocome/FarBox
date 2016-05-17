from django.db import models

# Create your models here.


class RealFile(models.Model):
    file_name = models.CharField(max_length=200)
    file_hash = models.CharField(max_length=200)
    file_size = models.BigIntegerField()

class VirtualFile(models.Model):
    pass