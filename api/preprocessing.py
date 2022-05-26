from numpy import character
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
#  Lectura de informacion excel
COLUMNAS = ['Date', 'Time', 'Control - Voltaje de Bateria (V)', 'Viento - Velocidad (km/h)',
            'Viento - Direccion (°)', 'Temperatura (°C)', 'Humedad Relativa (% RH)',
            'Presion Barometrica (hPa)', 'Precipitation (mm)']
# TIPO = [str, str, str, str]
class GD_01_excel:
    def __init__(self, archivo, archivo_cperv, columnas=COLUMNAS,salto_filas=0, ) -> None:
        self.archivo_, self.archivo_cperv_ , self.columnas, self.sal_filas= archivo, archivo_cperv, columnas, salto_filas
        pass
    
    def preprocesamiento_gd01(self,):
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
        return self.df_gd01
    def preprocesamiento_gd02(self,):
        self.df_gd02 = pd.read_csv(self.archivo_cperv_, sep = ',')
        self.df_gd02['Time'] = pd.to_datetime(self.df_gd02['Time'])
        self.df_gd02.index = self.df_gd02['Time']
        self.pronostico = self.df_gd02[['W10s_1s','Wds_1s','T2s_1s','Rh2_1s','SLP_1s']]
        print(self.pronostico.head()) 
        print(self.pronostico.tail()) 
        return self.pronostico
    def comparativa_union(self,):
        self.pronostico.index = self.pronostico.index.floor('5min')
        self.df_total = self.df_gd01.merge(self.pronostico, left_index=True, right_index=True)
        self.df_total['Viento - Velocidad (m/s)'] = self.df_total['Viento - Velocidad (km/h)'] * (10/36)
        print(self.df_total)
        # return self.df_total.to_json(orient="records")
        return self.df_total.to_json(orient="split")
    def comp_ws(self,):
        fig, ax =plt.subplots(figsize=(5,4))
        plt.plot(self.df_total.index, self.df_total['Viento - Velocidad (m/s)'], '--', label ='SCADA')
        plt.plot(self.df_total.index, self.df_total['W10s_1s'], '--', label ='Pronostico')
        plt.grid(True)
        plt.legend()
        plt.savefig('./prueba.jpg')
        pass