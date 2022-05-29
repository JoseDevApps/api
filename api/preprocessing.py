from numpy import character
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import json
#  Lectura de informacion excel
COLUMNAS = ['Date', 'Time', 'Control - Voltaje de Bateria (V)', 'Viento - Velocidad (km/h)',
            'Viento - Direccion (°)', 'Temperatura (°C)', 'Humedad Relativa (% RH)',
            'Presion Barometrica (hPa)', 'Precipitation (mm)']
# TIPO = [str, str, str, str]
def RMSE(observados, simulados, WD=False):
    N = len(observados)
    if WD == False:
        Phi = []
        Phi = simulados-observados
        Sum = sum(Phi**2)
        rmse = np.sqrt((1/N)* Sum)
    if WD == True:
        Phi = np.zeros(N)
        i = 0
        for a,b in zip(simulados,observados):
            if np.abs(a-b)>180:
                Phi[i] = a-b*(1-(360/np.abs(a-b)))
            else:
                Phi[i] = a-b
            i = i +1
        np.array(Phi)
        # print(Phi)
        Sum = sum(Phi**2)
        rmse = np.sqrt((1/N)* Sum)
    return rmse
def MAE(observados,simulados,WD =False):
    N = len(observados)

    if WD == False:
        Phi = []
        Phi = np.abs(simulados-observados)
        Sum = sum(Phi**1)
        rmse = (1/N)* Sum
    if WD == True:
        Phi = np.zeros(N)
        i = 0
        for a,b in zip(simulados,observados):
            if np.abs(a-b)>180:
                Phi[i] = a-b*(1-(360/np.abs(a-b)))
                # print(Phi[i])
            else:
                Phi[i] =np.abs(a-b)
            i = i +1
        np.array(Phi)
        # print(Phi)
        Sum = sum(Phi**1)
        rmse = (1/N)* Sum

    return rmse

def MB(observados,simulados,WD =False):
    N = len(observados)
    if WD == False:
        Phi = []
        Phi = simulados-observados
        Sum = sum(Phi)
        bias = (1/N)*Sum
    if WD == True:
        Phi = np.zeros(N)
        i = 0
        for a,b in zip(simulados,observados):
            if np.abs(a-b)>180:
                Phi[i] = a-b*(1-(360/np.abs(a-b)))
                # print(Phi[i])
            else:
                Phi[i] = a-b
            i = i +1
        np.array(Phi)
        Sum = sum(Phi)
        bias = (1/N)*Sum
    return bias
def IOA(observados,simulados,WD =False):
    N = len(observados)
    M = sum(observados)/N
    x = np.ones(N) * M
    a = np.abs(simulados - x)
    b = np.abs(observados - x)

    IA = 1- (sum((simulados-observados)**2))/sum((a+b)**2)
    return IA

def STDE(observados,simulados):
    rmse = RMSE(observados,simulados)
    mb = MB(observados,simulados)
    return np.sqrt((rmse*rmse)-(mb*mb))

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
    def metricas_ws(self):
        RMSE_WS = RMSE(self.df_total['Viento - Velocidad (m/s)'], self.df_total['W10s_1s'])
        MB_WS = MB(self.df_total['Viento - Velocidad (m/s)'],self.df_total['W10s_1s'])
        IOA_WS = IOA(self.df_total['Viento - Velocidad (m/s)'],self.df_total['W10s_1s'])
        STDE_WS = STDE(self.df_total['Viento - Velocidad (m/s)'],self.df_total['W10s_1s'])
        MAE_WS = MAE(self.df_total['Viento - Velocidad (m/s)'],self.df_total['W10s_1s'])
        R2_WS = stats.pearsonr(self.df_total['Viento - Velocidad (m/s)'],self.df_total['W10s_1s'])
        data = {}
        data['rmse'] = RMSE_WS
        data['mb'] = MB_WS
        data['ioa'] = IOA_WS
        data['stde'] = STDE_WS
        data['mae'] = MAE_WS
        data['pearson'] = R2_WS
        json_data = json.dumps(data)
        return json_data
    def metricas_tmp(self):
        RMSE = RMSE(self.df_total['Temperatura (°C)'], self.df_total['T2s_1s'])
        MB = MB(self.df_total['Temperatura (°C)'],self.df_total['T2s_1s'])
        IOA = IOA(self.df_total['Temperatura (°C)'],self.df_total['T2s_1s'])
        STDE = STDE(self.df_total['Temperatura (°C)'],self.df_total['T2s_1s'])
        MAE = MAE(self.df_total['Temperatura (°C)'],self.df_total['T2s_1s'])
        R2 = stats.pearsonr(self.df_total['Temperatura (°C)'],self.df_total['T2s_1s'])
        data = {}
        data['rmse'] = RMSE
        data['mb'] = MB
        data['ioa'] = IOA
        data['stde'] = STDE
        data['mae'] = MAE
        data['pearson'] = R2
        json_data = json.dumps(data)
        return json_data
    def metricas_rh(self):
        RMSE = RMSE(self.df_total['Humedad Relativa (% RH)'], self.df_total['Rh2_1s'])
        MB = MB(self.df_total['Humedad Relativa (% RH)'],self.df_total['Rh2_1s'])
        IOA = IOA(self.df_total['Humedad Relativa (% RH)'],self.df_total['Rh2_1s'])
        STDE = STDE(self.df_total['Humedad Relativa (% RH)'],self.df_total['Rh2_1s'])
        MAE = MAE(self.df_total['Humedad Relativa (% RH)'],self.df_total['Rh2_1s'])
        R2 = stats.pearsonr(self.df_total['Humedad Relativa (% RH)'],self.df_total['Rh2_1s'])
        data = {}
        data['rmse'] = RMSE
        data['mb'] = MB
        data['ioa'] = IOA
        data['stde'] = STDE
        data['mae'] = MAE
        data['pearson'] = R2
        json_data = json.dumps(data)
        return json_data
    def metricas_wd(self):
        RMSE = RMSE(self.df_total['Viento - Direccion (°)'], self.df_total['Wds_1s'])
        MB = MB(self.df_total['Viento - Direccion (°)'],self.df_total['Wds_1s'])
        IOA = IOA(self.df_total['Viento - Direccion (°)'],self.df_total['Wds_1s'])
        STDE = STDE(self.df_total['Viento - Direccion (°)'],self.df_total['Wds_1s'])
        MAE = MAE(self.df_total['Viento - Direccion (°)'],self.df_total['Wds_1s'])
        R2 = stats.pearsonr(self.df_total['Viento - Direccion (°)'],self.df_total['Wds_1s'])
        data = {}
        data['rmse'] = RMSE
        data['mb'] = MB
        data['ioa'] = IOA
        data['stde'] = STDE
        data['mae'] = MAE
        data['pearson'] = R2
        json_data = json.dumps(data)
        return json_data