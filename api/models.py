# Create your models here.
from email.policy import default
from django.db import models
from datetime import date, timedelta
def upload_path(instance, filename):
    return '/'.join(['GD', str(instance.archivo), filename])

def meteo_default():
    return {
        "rmse": 0,
        "mb": 0,
        "ioa": 0,
        "stde": 0,
        "mae": 0,
        "pearson": 0,
    }
class GD(models.Model):
    archivo = models.CharField(max_length=32, blank= False)
    gd01 =  models.FileField(upload_to=upload_path, blank=True, null=True)
    gd02 =  models.FileField(upload_to=upload_path, blank=True, null=True)
    def __str__(self):
        return str(self.id)
class Resultados(models.Model):
    metricas_ws = models.JSONField('wind_speed')
    metricas_wd = models.JSONField('wind_direction')
    metricas_rh = models.JSONField('humedad_relativa')
    metricas_tmp = models.JSONField('temperatura')
    data_comp = models.JSONField('meteorologia', default= meteo_default) 