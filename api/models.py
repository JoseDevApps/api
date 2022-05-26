# Create your models here.
from django.db import models
from datetime import date, timedelta
def upload_path(instance, filename):
    return '/'.join(['GD', str(instance.archivo), filename])


class GD(models.Model):
    archivo = models.CharField(max_length=32, blank= False)
    gd01 =  models.FileField(upload_to=upload_path, blank=True, null=True)
    gd02 =  models.FileField(upload_to=upload_path, blank=True, null=True)
    def __str__(self):
        return str(self.id)
class Resultados(models.Model):
    metricas_ws = models.FloatField(null=True, default=0)
    metricas_wd = models.FloatField(null=True, default=0)
    metricas_rh = models.FloatField(null=True, default=0)
    metricas_tmp = models.FloatField(null=True, default=0)
    image_ws = models.FileField(upload_to='resultados', blank=True, null=True)
    image_wd = models.FileField(upload_to='resultados', blank=True, null=True)
    image_rh = models.FileField(upload_to='resultados', blank=True, null=True)
    image_tmp = models.FileField(upload_to='resultados', blank=True, null=True)