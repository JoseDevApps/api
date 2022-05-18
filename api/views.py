# import pandas
import pandas as pd
from .preprocessing import GD_01_excel
# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets
# Serializers
from .serializers import GDSerializer
# Models
from .models import GD

class GDViewSet(viewsets.ModelViewSet):
    queryset = GD.objects.all()
    serializer_class = GDSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        gd01 = request.data['gd01']
        gd02 = request.data['gd02']
        archivo = request.data['archivo']
        GD.objects.create(archivo=archivo, gd01=gd01, gd02=gd02)
        form_gd01 = GD_01_excel(gd01, salto_filas=2)
        form_gd01.preprocesamiento_gd01()
        return HttpResponse({'message':'Archivo guardado'}, status=200)
