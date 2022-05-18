from numpy import character
import pandas as pd
from collections import Counter
#  Lectura de informacion excel
COLUMNAS = ['CLIENTE', 'DIRECCION', 'TELEFONO', 'COD_LOCALIDAD',
            'COD_ZONA', 'TIPO_MEDICION', 'MEDIDOR_1',
            'MEDIDOR_2', 'NOMBRE', 'NRO_DOCUMENTO','CATEGORIA',
            'CLASIFICACION_GD', 'NIVEL_CALIDAD', 'TIPO_SUM',
            'PUNTO_MEDICION', 'TIPO_SUMINISTRO', 
            'TIPO_GENERACION', 'COORDENADAS', 'POT_GEN_DIS',
            'POT_MAX_GEN', 'FUN_PRIM', 'NUM_AGEN', 'NUM_MOD',
            'NUM_INV', 'MAR_INV', 'SUP_OCU','FECHA_PSR',
            'FAC_PLANTA']
# TIPO = [str, str, str, str]
class GD_01_excel:
    def __init__(self, archivo, columnas=COLUMNAS,salto_filas=2, ) -> None:
        self.archivo_ , self.columnas, self.sal_filas= archivo, columnas, salto_filas
        pass
    
    def preprocesamiento_gd01(self,):
        self.df_gd01 = pd.read_excel(self.archivo_,skiprows=self.sal_filas)
        # analisis del campo - CLIENTE
        validos = "0123456789-"
        mensaje_completo = ''
        for i,cliente in enumerate(self.df_gd01[self.columnas[0]]):
            condicion = ''.join(x for x in cliente if x in validos)
            if not (condicion==cliente):
                mensaje = ('Caracter no valido en la columna: '+self.columnas[0]+' y fila: '+str(i+4))
                mensaje_completo += '\n'+ str(mensaje)
                print(mensaje)
        print(mensaje_completo)
        # eliminacion de '-'
        # arreglo = prueba.replace('-','')
        # print(arreglo)
        if (self.df_gd01[self.columnas[0]].dtypes == object):
            print('cumple con el tipo object')
        else:
            print('error en la fila xx y columna xx')
        
    