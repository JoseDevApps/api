# Create your models here.
from django.db import models

def upload_path(instance, filename):
    return '/'.join(['GD', str(instance.archivo), filename])

class GD(models.Model):
    archivo = models.CharField(max_length=32, blank= False)
    gd01 =  models.FileField(upload_to=upload_path, blank=True, null=True)
    gd02 =  models.FileField(upload_to=upload_path, blank=True, null=True)
    def __str__(self):
        return self.archivo