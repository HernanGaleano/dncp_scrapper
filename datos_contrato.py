# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:44:30 2019

@author: Hernán
"""

##Lo que se pide en doc reAc:
#No. N° - No hace falta
#No. Año - Se estira de fecha
#Si. N° de contrato
#Si. Empresa
#Si. Fecha de contrato
#Si. Monto total (₲)
#Si. Titulo de contrato
#No. Institución beneficiada
#No. Nº Instituciones beneficiadas
#No. Barrio/Localidad
#No. Monto FONACIDE
#No. Monto Individual (₲)
#No. Puesto en lista de priorización, Aula, Sanitario, Otros espacios
#No. Descripción de obra según título de contrato. 
#
#Guardar:
#    ID de licitacion
#    Fecha de firma de contrato
#    N° de contrato
#    nombre de empresa
#    ruc
#    monto de contrato
#    titulo de contrato


#Falta descargar items adjudicados si es por lote

#from selenium import webdriver
import os
import re
import down_utils
import selenium.webdriver.support.ui as UI
from random import randint
from time import sleep

def copiar_PBC(driver):
    pass

def modf_contrato(driver):
    xp_ul_tabs = '/html/body/div[2]/ul'
    ul_tabs = driver.find_element_by_xpath(xp_ul_tabs)
    try:
        modificaciones = ul_tabs.find_element_by_link_text("Modificaciones al Contrato").get_attribute('href')
        modificaciones = modificaciones.replace('/modificaciones-contrato.html','.html#modificaciones')
        return modificaciones       
    except:
        return ''

def rescision_contrato(driver):
    xp_ul_tabs = '/html/body/div[2]/ul'
    ul_tabs = driver.find_element_by_xpath(xp_ul_tabs)
    try:
        rescisiones = ul_tabs.find_element_by_link_text("Rescisiones de Contrato").get_attribute('href')
        rescisiones = rescisiones.replace('/rescisiones-contrato.html','.html#rescisiones')
        return rescisiones  
    except:
        return None
        
def entrar_guardar_datos(driver, licitacion, link_contrato):
    wait = UI.WebDriverWait(driver, 5000) #Capaz pasar a otra parte

    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(link_contrato)
    sleep(randint(5,30))
    
    
    
    datos={
    'id_licitacion' : '//*[@id="datos_contrato"]/section[2]/div/div/div[1]/div[2]/em', 
    'fecha_firma_contrato' : '//*[@id="datos_contrato"]/section[1]/div/div/div[4]/div[2]',
    'num_contrato' : '//*[@id="datos_contrato"]/section[1]/div/div/div[3]/div[4]',
    'nombre_empresa' : '//*[@id="datos_contrato"]/section[1]/div/div/div[1]/div[2]/em',
    'ruc_empresa' : '//*[@id="datos_contrato"]/section[1]/div/div/div[1]/div[4]',
    'monto_adjudicado' : '//*[@id="datos_contrato"]/section[1]/div/div/div[3]/div[2]',
    'titulo_contrato' : '/html/body/div[2]/div[1]/h1',
    'convocante' : '//*[@id="datos_contrato"]/section[2]/div/div/div[3]/div[2]',
    }
    
    
    contrato = {}

    for key in datos:
        try:
          info = driver.find_element_by_xpath(datos[key]).text
          contrato.update({key:info})
        except:
            contrato.update({key:''})
            pass
    
    #Descarga del código de contratación
    #xp_codigo_contratacion = '//*[@id="datos_contrato"]/div[1]/div/div/ul/li[5]/a'
    #driver.find_element_by_xpath(xp_codigo_contratacion).click() 
    print(contrato)
    
    try:
        xp_acciones = '//*[@id="datos_contrato"]/div[1]/div/div/ul'
        ul_tabs = driver.find_element_by_xpath(xp_acciones)
        ul_tabs.find_element_by_link_text("Descargar Código de Contratación (CC)").click()
    except:
        pass
    
    #Para casos dónde no se carga el número de contrato
    try:
        num_contrato = re.search("^(\d{2,3})", contrato['num_contrato']).group(1)
    except:
        num_contrato = '00'
        
    dest_path = (os.getcwd() +
                 '\\docs\\' + 
                 contrato['convocante'] + 
                 '\\' + 
                 contrato['fecha_firma_contrato'][-4:] + 
                 '\\' +
                 num_contrato + 
                 ' ' +
                 contrato['fecha_firma_contrato'][-4:] + 
                 ' ' +            
                 contrato['id_licitacion'] + ' ' +            
                 contrato['nombre_empresa'].title() +
                 '\\')
    
    #Asegurar que la carpeta de contrato existe
    down_utils.make_path(dest_path)
    
    directory = 'Downloads' #Carpeta default para descargar archivos. Configurado también al inciar Selenium
    descarga = down_utils.wait_rename(dest_path, directory, timeout = 30)
    contrato.update({'codigo_contratacion' : descarga})

    sleep(randint(2,10))
            
    ### Navegar a la pestaña de documentos
    xp_ul_tabs = '/html/body/div[2]/ul'
    ul_tabs = driver.find_element_by_xpath(xp_ul_tabs)
    ul_tabs.find_element_by_link_text("Documentos").click()#.get_attribute('href')
    
   
    #def downl_from_table(down):
    contrato_down = False
    table_id = wait.until(
            lambda driver: driver.find_element_by_tag_name('tbody'))
    # get all of the rows in the table
    rows = table_id.find_elements_by_tag_name("tr") 
    for row in rows:
        cols = row.find_elements_by_tag_name("td")
        #print('test')
        if cols[0].text == 'Orden de Compra o Contrato':
            contrato_down = True
            link = cols[3].find_element_by_tag_name("a")
            link.click()
            break
    
    if contrato_down == True:
        directory = 'Downloads' #Carpeta default para descargar archivos. Configurado también al inciar Selenium
        contrato_down = down_utils.wait_rename(dest_path, directory, timeout = 30)
        contrato.update({'contrato_download' : contrato_down})
    else:
        contrato.update({'contrato_download' : False})
                
    #Pasar a la página 2 de la tabla de documentos
    #xp_pagina2 = '//*[@id="documentos"]/div[2]/div[2]/div[2]/div/ul/li[3]/a'
    #driver.find_element_by_xpath(xp_pagina2).click()

    #Verificar si existen modificaciones al contrato
    contrato.update({'modificaciones_contrato' : modf_contrato(driver)})
    contrato.update({'rescision_contrato' : rescision_contrato(driver)})
    
    #Copiar PBC a carpeta del contrato
    if licitacion['PBC_path'] != None:
        PBC_copiado =  down_utils.copiar_PBC(licitacion['PBC_path'], dest_path)
        print('Se copió el PBC a la carpeta contrato: ' + str(PBC_copiado))



    print('Contrato:' + contrato['num_contrato'] + ' - ' + contrato['nombre_empresa'] + ': Datos guardados')





    sleep(randint(15,30))



    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    return(contrato)