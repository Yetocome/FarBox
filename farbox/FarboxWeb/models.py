from django.db import models

# Create your models here.


class RealFile:
    file_name = models.CharField(max_length=200)
    file_hash = models.CharField(max_length=200)
