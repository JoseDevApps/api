from numpy import character
import pandas as pd
from collections import Counter
#  Lectura de informacion excel
COLUMNAS = ['Date', 'Time', 'Control - Voltaje de Bateria (V)', 'Viento - Velocidad (km/h)',
            'Viento - Direccion (�)', 'TIPO_MEDICION', 'MEDIDOR_1',
            'MEDIDOR_2', 'NOMBRE', 'NRO_DOCUMENTO','CATEGORIA',
            'CLASIFICACION_GD', 'NIVEL_CALIDAD', 'TIPO_SUM',
            'PUNTO_MEDICION', 'TIPO_SUMINISTRO', 
            'TIPO_GENERACION', 'COORDENADAS', 'POT_GEN_DIS',
            'POT_MAX_GEN', 'FUN_PRIM', 'NUM_AGEN', 'NUM_MOD',
            'NUM_INV', 'MAR_INV', 'SUP_OCU','FECHA_PSR',
            'FAC_PLANTA']
# TIPO = [str, str, str, str]
class GD_01_excel:
    def __init__(self, archivo, columnas=COLUMNAS,salto_filas=0, ) -> None:
        self.archivo_ , self.columnas, self.sal_filas= archivo, columnas, salto_filas
        pass
    
    def preprocesamiento_gd01(self,):
        print(self.archivo_)
        self.df_gd01 = pd.read_csv(self.archivo_ ,sep=';',skiprows=self.sal_filas, encoding='ISO-8859-1')
        # cambiando el formato de fecha
        self.df_gd01[self.columnas[0]] = pd.to_datetime(self.df_gd01[self.columnas[0]], format='%d/%m/%y')
        self.df_gd01[self.columnas[1]] = pd.to_timedelta(self.df_gd01[self.columnas[1]])
        self.df_gd01['Datetime'] = self.df_gd01[self.columnas[0]] + self.df_gd01[self.columnas[1]]
        self.df_gd01.index = self.df_gd01['Datetime']
        del self.df_gd01[self.columnas[0]]
        del self.df_gd01[self.columnas[1]]
        del self.df_gd01['Datetime']
        # reemplazando la coma por punto
        self.df_gd01 = self.df_gd01.apply(lambda x:x.str.replace(',','.'))
        self.df_gd01 = self.df_gd01.astype(float)
        
        print(self.df_gd01.info())
        print(self.df_gd01.head())
        return self.df_gd01.columns
        # validos = "0123456789-"
        # mensaje_completo = ''
        # for i,cliente in enumerate(self.df_gd01[self.columnas[0]]):
        #     condicion = ''.join(x for x in cliente if x in validos)
        #     if not (condicion==cliente):
        #         mensaje = ('Caracter no valido en la columna: '+self.columnas[0]+' y fila: '+str(i+4))
        #         mensaje_completo += '\n'+ str(mensaje)
        #         print(mensaje)
        # print(mensaje_completo)
        # # eliminacion de '-'
        # # arreglo = prueba.replace('-','')
        # # print(arreglo)
        # if (self.df_gd01[self.columnas[0]].dtypes == object):
        #     print('cumple con el tipo object')
        # else:
        #     print('error en la fila xx y columna xx')
        
    