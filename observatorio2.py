from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd


driver = webdriver.Firefox()
driver.get("https://www.ofxb.ch/wx/")




elem=driver.find_elements(By.XPATH,'/html/body/div[1]/div[3]/select[1]')
years = []
years_depurado = []

datos_del_mes = {}
datos_del_mes['Fecha'] = []
datos_del_mes['Día'] = []
datos_del_mes['Temperatura Media'] = []

for year in elem:
        selected_year = year.text
        years.append(selected_year)

years_objeto = years[0]
years_depurado = years_objeto.split("\n")[:-1]
#Ahora debería recapitular todos los años 
years_short = years_depurado

max_pages = 5

numeros_tabla = ['01','02','03','04','05','06','07','08',
    '09','10','11','12','13','14','15',
'16','17','18','19','20','21','22',
'23','24','25','26','27','28','29','30',
'31','01']

diccionario_year = {}
datos_temperatura = {}

# ID del reporte en la página //*[@id="report"]

for year in years_short:
    try:
    #    if max_pages < 5:
    #        tiempo_espera = random.randint(0,3)
        driver.get(f"https://www.ofxb.ch/wx/tabular.html?report=NOAA/NOAA-{year}.txt")
        time.sleep(random.randint(2, 3))
        report = driver.find_elements(By.XPATH,'//*[@id="report"]')
        print(report[0].text)
        ### Este report list es el más depurado hasta el momento
        report_list = report[0].text.split()
        print(report_list)
        #print(report_list.index('21'))
        #indice_temperatura = report_list.index('21') + 1
        #primera_temperatura = report_list[indice_temperatura]
        #print(primera_temperatura)



        print(f'\n\n\n Mes y año de recolección = {report_list[4]+report_list[5]}\n\n\n\n')
        fecha_recolec = report_list[4]+report_list[5]


        contador_indices = 0 
        for i in numeros_tabla[:-1]:
            try:
                indice_numero_seccion = report_list.index(numeros_tabla[contador_indices])
            except:
                #Mejorar esta función. Actualmente devuelve el último elemento
                # Ver el caso de Febrero
                print('Ya no hay días para mostrar')
                pass
            indice_temperatura = indice_numero_seccion + 1
            temperatura = report_list[indice_temperatura]
            if temperatura in numeros_tabla:
                print('No hay datos para este día')
                datos_temperatura[numeros_tabla[contador_indices]] = 0
            else:
                datos_temperatura[numeros_tabla[contador_indices]] = temperatura
                print(temperatura)
            contador_indices += 1




        for key, value in datos_temperatura.items():
            datos_del_mes['Fecha'].append(fecha_recolec)
            datos_del_mes['Día'].append(key)
            datos_del_mes['Temperatura Media'].append(value)

        df = pd.DataFrame(datos_del_mes)
        df.to_csv(index=False)
    except:
        print(f'No hay datos para la página {year}')
        pass



#        time.sleep(tiempo_espera)
#        max_pages += 1
        

#print(years_depurado)

#driver.get(f"https://www.ofxb.ch/wx/tabular.html?report=NOAA/NOAA-{selected_year}.txt")
#time.sleep(random_time)

#DataFrame Final
df = pd.DataFrame(datos_del_mes)
print(df)

df.to_csv('temperatura_media.csv', encoding='utf-8')


#driver.close()

print(f"\n \n \n Diccionario de datos temperatura: {datos_del_mes}")



