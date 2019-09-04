# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 17:39:21 2019

@author: Hernán
"""

import pdb
#import csv
#from time import sleep, strftime
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import Select
#from random import randint
import pandas as pd
#import numpy
import os
#import time

import selenium.webdriver.support.ui as UI
from random import randint
from time import sleep

import buscar_licitacion
import datos_contrato as dt
import datos_licitacion as dl
import siguiente_pagina as sp

###### Change Download folder
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : os.getcwd() + '\\Downloads'}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)


wait = UI.WebDriverWait(driver, 5000)

#Un resultado
#ID 333763 

#Resultado de una página
#web_url = 'https://www.contrataciones.gov.py/buscador/licitaciones.html?nro_nombre_licitacion=&convocantes%5B%5D=44&fecha_desde=01-01-2018&fecha_hasta=01-09-2018&tipo_fecha=PUB&marcas%5B%5D=fonacide&convocante_tipo=&convocante_nombre_codigo=&codigo_contratacion=&catalogo%5Bcodigos_catalogo_n4%5D=&page=1&order=&convocante_codigos=44&convocante_tipo_codigo=&unidad_contratacion_codigo=&catalogo%5Bcodigos_catalogo_n4_label%5D='
#web_url ='https://www.contrataciones.gov.py/buscador/licitaciones.html?nro_nombre_licitacion=&convocantes%5B%5D=44&fecha_desde=01-01-2015&fecha_hasta=31-12-2017&tipo_fecha=ADJ&marcas%5B%5D=fonacide&convocante_tipo=&convocante_nombre_codigo=&codigo_contratacion=&catalogo%5Bcodigos_catalogo_n4%5D=&page=1&order=fecha_publicacion_convocatoria+desc&convocante_codigos=44&convocante_tipo_codigo=&unidad_contratacion_codigo=&catalogo%5Bcodigos_catalogo_n4_label%5D='
web_url = 'https://www.contrataciones.gov.py/buscador/licitaciones.html'
driver.get(web_url)
sleep(randint(5,10))


convocante = 'Municipalidad de Ciudad del Este'
#convocante = 'Municipalidad de Presidente Franco'
buscar_licitacion.buscar_licitacion(convocante, driver)
solo_contratos = [] #Lista de contratos
solo_licitacion = [] 
### Iterar sobre los resultados en licitaciones
existe_siguiente_pagina = True
while existe_siguiente_pagina == True:
    
    ### Resultado de busqueda
    xp_nombres_licit = '//*[@id="licitaciones"]/ul/li/article/header/h3/a'
    xp_etapas_licit = '//*[@id="licitaciones"]/ul/li/article/div/div[1]/div[1]/div[2]/em'
    xp_id_licit = '//*[@id="licitaciones"]/ul/li/article/div/div[1]/div[1]/div[1]/em'
    nombres_licitacion = driver.find_elements_by_xpath(xp_nombres_licit)
    etapas_licit = driver.find_elements_by_xpath(xp_etapas_licit)
    id_licit = driver.find_elements_by_xpath(xp_id_licit)
    
    
    ## Hacer esto cada vez que se vuelve a la lista de resultados
    #i = 0 #para iterar sobre resultados en nombres
    for i, etapa in enumerate(etapas_licit):
    #    print(i)
    #    print(etapa)
    #    print(etapa.text)
        
        lista_anterior = [item['id_licitacion'] for item in solo_licitacion if item['id_licitacion'] == id_licit[i].text]
        if lista_anterior != []:
            continue
    
        etapa_texto = etapa.text
        print(str(i) + ' - ' + nombres_licitacion[i].text + ' - ' + etapa_texto)
        
        sleep(randint(5,80))

        
        enlace = nombres_licitacion[i].get_attribute('href')
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(enlace)
        sleep(randint(5,10))
        ### Obtener datos de licitación
        licitacion_out = dl.obtener_datos(driver)
        solo_licitacion.append(licitacion_out)
        sleep(randint(15,30))

       
        if etapa_texto == 'Adjudicada':      
            #Navegar a proveedores adjudicados
            xp_ul_tabs = '/html/body/div[2]/ul'
            ul_tabs = driver.find_element_by_xpath(xp_ul_tabs)
            ul_tabs.find_element_by_link_text("Proveedores Adjudicados").click()
            
            xp_div_proveedores = '//*[@id="proveedores"]'
            table_id = wait.until(lambda driver: driver.find_element_by_xpath(xp_div_proveedores).find_element_by_tag_name('tbody'))
#            table_id = proveedores.find_element_by_tag_name('tbody')
            rows = table_id.find_elements_by_tag_name("tr")
            links_contratos = map(lambda row: row.find_elements_by_tag_name("td")[-1].find_element_by_tag_name("a").get_attribute('href'), rows)
            links_contratos = list(links_contratos)
            #List Comprehension
            contrato_out = [dt.entrar_guardar_datos(driver, licitacion_out, link) for link in links_contratos]
            solo_contratos.extend(contrato_out)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    xp_ul_lic = '//*[@id="licitaciones"]/div[2]/div/div[2]/div/ul' #ul resultado de busqueda de licitaciones
    existe_siguiente_pagina = sp.siguiente_pag(driver, xp_ul_lic)

driver.close()


#dff = pd.DataFrame(solo_licitacion, columns=['id_licitacion', 'nombre_licitacion', 'fecha_publicacion', 'estado', 'monto', 'sistema_adjudicacion'])
licitaciones_panda = pd.DataFrame(solo_licitacion)
contratos_panda = pd.DataFrame(solo_contratos)

file_xlsx = os.getcwd() + '\\docs\\'+ convocante + '\\' + 'resumen.xlsx'

with pd.ExcelWriter(file_xlsx) as writer:  # doctest: +SKIP
    licitaciones_panda.to_excel(writer, index = False, sheet_name = 'licitaciones')
    contratos_panda.to_excel(writer, index = False, sheet_name = 'contratos')
