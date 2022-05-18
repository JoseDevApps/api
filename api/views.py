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

    def post(self, request, *args, **kwargs):
        gd01 = request.data['gd01']
        gd02 = request.data['gd02']
        archivo = request.data['archivo']
        GD.objects.create(archivo=archivo, gd01=gd01, gd02=gd02)
        return HttpResponse({'mensage': 'Archivo guardado'}, status=200)
