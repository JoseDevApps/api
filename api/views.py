# import pandas
import pandas as pd
from .preprocessing import GD_01_excel
import json
# Create your views here.
from django.http import HttpResponse
from rest_framework.response import Response
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
        objeto = GD.objects.create(archivo=archivo, gd01=gd01, gd02=gd02)
        form_gd01 = GD_01_excel(objeto.gd01.path,objeto.gd02.path, salto_filas=0)
        form_gd01.preprocesamiento_gd01()
        form_gd01.preprocesamiento_gd02()
        df_total = form_gd01.comparativa_union()
        parsed = json.loads(df_total)
        form_gd01.comparativa_union()
        print(objeto.gd02.path)
        print(type(objeto.gd02.url))
        return Response(parsed)
    