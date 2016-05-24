from django.db import models

# Create your models here.


class RealFile(models.Model):
    file_name = models.CharField(max_length=200)
    file_hash = models.CharField(max_length=200)
    file_size = models.BigIntegerField()

class VirtualFile(models.Model):
    realfilename = models.CharField(max_length=200, null=True)
    path_id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField(default=0)
    path_name = models.CharField(max_length=200)
    is_file = models.BooleanField(default=False)