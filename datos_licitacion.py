# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 11:24:05 2019

@author: Hernán
"""

import os
import re
import down_utils
import selenium.webdriver.support.ui as UI
from pathlib import Path
from random import randint
from time import sleep    
import siguiente_pagina as sp



xp_ul_steps = '/html/body/div[2]/div[2]/ul'
xp_ul_tabs = '/html/body/div[2]/ul'


def leer_tags(driver, step, tag):
    tags = []
    xp_div_tags = '//*[@id="datos_' + step + '"]/div[2]'
    try:
        div_tags = driver.find_element_by_xpath(xp_div_tags).find_elements_by_css_selector("span")
        tags = [item.text for item in div_tags]
    except:
        pass
            
    if tag in tags:
        return 'Sí'
    else:
        return 'No'
        

def guardar_datos(driver, step):
    """ 
    Guarda los datos de la licitación en la ventana activa. 
  
    Guarda los datos de la licitación (id, nombre, convocante, monto) que está
    abierta en la ventana activa. 
    
    Parameters: 
    driver (int): Driver de selenium
    step (string): Etapa en que se encuentra la licitación
  
    Returns: 
    dictionary: Datos de licitación
  
    """
    if step == 'adjudicacion':
        datos={
        'id_licitacion' : '//*[@id="datos_' + step + '"]/section/div/div/div[1]/div[2]/em',
        'nombre_licitacion' : '//*[@id="datos_' + step + '"]/section/div/div/div[2]/div[2]/em',
        'convocante' : '//*[@id="datos_' + step + '"]/section/div/div/div[3]/div[2]',
        'estado' : '//*[@id="datos_' + step + '"]/section/div/div/div[7]/div[2]/em',
        'monto' : '//*[@id="datos_' + step + '"]/section/div/div/div[9]/div[2]',
        'fecha_publicacion' : '//*[@id="datos_' + step + '"]/section/div/div/div[10]/div[2]',
        'sistema_adjudicacion' : '//*[@id="datos_' + step + '"]/section/div/div/div[8]/div[2]',
        }
    elif step == 'licitacion':
        datos={
        'id_licitacion' : '//*[@id="datos_' + step + '"]/section/div/div/div[1]/div[2]/em',
        'nombre_licitacion' : '//*[@id="datos_' + step + '"]/section/div/div/div[2]/div[2]/em',
        'convocante' : '//*[@id="datos_licitacion"]/section[1]/div/div/div[4]/div[2]',
        'estado' : '//*[@id="datos_licitacion"]/section[1]/div/div/div[8]/div[2]/em',
        'monto' : '//*[@id="datos_licitacion"]/section[2]/div/div/div[2]/div[2]',
        'fecha_publicacion' : '//*[@id="datos_' + step + '"]/section/div/div/div[10]/div[2]',
        'sistema_adjudicacion' : '//*[@id="datos_' + step + '"]/section/div/div/div[8]/div[2]',
        }
    elif step == 'convocatoria':
        datos={
        'id_licitacion' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[1]/div[2]/em',
        'nombre_licitacion' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[1]/div[4]/em',
        'convocante' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[2]/div[2]',
        'estado' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[5]/div[2]/em',
        'monto' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[4]/div[2]',
        'fecha_publicacion' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[5]/div[4]',
        'sistema_adjudicacion' : '//*[@id="datos_' + step + '"]/div[3]/div[1]/section/div/div/div[1]/div[2]',
        }
    elif step == 'planificacion':
        datos={
        'id_licitacion' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[1]/div[2]/em',
        'nombre_licitacion' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[1]/div[4]/em',
        'convocante' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[2]/div[2]',
        'estado' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[5]/div[2]/em',
        'monto' : '//*[@id="datos_' + step + '"]/div[3]/div[1]/section/div/div/div[1]/div[2]',
        'fecha_publicacion' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[5]/div[4]',
        #'sistema_adjudicacion' : '//*[@id="datos_' + step + '"]/section[1]/div/div/div[4]/div[2]',
        }    
    licitacion = {} 
    for key in datos:
        try:
            info = driver.find_element_by_xpath(datos[key]).text
            licitacion.update({key:info})
        except:
            licitacion.update({key:''})
            pass
    return(licitacion)

def PBC(driver):
    """ 
    Navega a la pestaña convocatoria y descarga el archivo de PBC
  
    Navega a la pestaña convocatoria y descarga el archivo de Pliego de
    Bases y Condiciones. Guarda en la carpeta:
        "Nombre de municipio"/"Año"/"ID de licitación"/
    
    Parameters: 
    driver (int): Driver de selenium
    step (string): etapa en que se encuentra la licitación
  
    Returns: 
    dictionary: Datos de licitación
  
    """

    wait = UI.WebDriverWait(driver, 50) #Capaz pasar a otra part
 
    try:
        ul_steps = driver.find_element_by_xpath(xp_ul_steps) #xp definido al inicio
        ul_steps.find_element_by_link_text("Convocatoria").click()
    except:
        pass

    #### Se navega a la carpeta de documentos para descargar el pliego de B y C
    # ************      Cambiar para buscar por nombre de la pestaña (documentos)
   # xp_documentos_convocatoria = '/html/body/div[2]/ul/li[4]/a'
    ul_tabs = driver.find_element_by_xpath(xp_ul_tabs) #xp definido al inicio
    ul_tabs.find_element_by_link_text("Documentos").click() 

    ##----------------- Tabla
    existe_siguiente_pagina = True
    PBC_down = False
    while existe_siguiente_pagina == True:
        sleep(5)
        table_id = wait.until(lambda driver: driver.find_element_by_tag_name('tbody'))
        rows = table_id.find_elements_by_tag_name("tr") # get all of the rows in the table
        for row in rows:
            cols = row.find_elements_by_tag_name("td") # Get the columns
            if cols[0].text == 'Pliego de bases y Condiciones':
                print('Se encontró el PBC')
                #Hacer click en checkbox
                xp_checkbox_condiciones = '//*[@id="checkboxSeccionesEstandares"]'
                driver.find_element_by_xpath(xp_checkbox_condiciones).click()
                #wait(3)
                cols[3].find_element_by_tag_name("a").click()
                PBC_down = True
                break
        xp_ul_PBC = '//*[@id="documentos"]/div[2]/div[2]/div[2]/div/ul'
        existe_siguiente_pagina = sp.siguiente_pag(driver, xp_ul_PBC)
    return PBC_down

def invitados(driver):
        ### Navegar a la pestaña de invitados en caso de que existan
    lista_invitados = []
    try:
        ul_tabs = driver.find_element_by_xpath(xp_ul_tabs) #xp definido al inicio
        ul_tabs.find_element_by_link_text("Invitados").click()
        xp_table = '//*[@id="invitados"]/div/div[1]/table'
        table_id = UI.WebDriverWait(driver, 500).until(lambda driver: driver.find_element_by_xpath(xp_table))
        rows = table_id.find_elements_by_tag_name("tbody > tr") # get all of the rows in the table
        for row in rows:
            empresa = {}
            cols = row.find_elements_by_tag_name("td") # Get the columns
            empresa.update({
                    'nombre_empresa' : cols[0].text,
                    'ruc_empresa' : cols[1].text
                    })
            lista_invitados.append(empresa)
    except:
        pass
    return lista_invitados

def oferentes_presentados(driver):
    #Se asume que se está en la pestaña de adjudicados        
    ##Navegar a oferentes presentados
#        xp_oferentes_presentados = '/html/body/div[2]/ul/li[4]/a'
        #guardar lista de oferentes presentados
        pass

def proveedores_adjudicados(driver):
    #Se asume que se está en la pestaña de adjudicados        
    ##Navegar a oferentes presentados
#        xp_oferentes_presentados = '/html/body/div[2]/ul/li[4]/a'
        #guardar lista de oferentes presentados
        pass







def obtener_datos(driver):
    
    
    
    try:
        ul_steps = driver.find_element_by_xpath(xp_ul_steps)
        step = ul_steps.find_element_by_class_name("active").text.lower()
        step = step.replace('ó','o')
    except:
        step = 'licitacion'    

    #guardar datos y termina la funcion (se hace siempre)
    licitacion = guardar_datos(driver, step)
    licitacion.update({'URL_lic' : driver.current_url})
    
    #Verificar tags
    tag = 'Plurianual'
    licitacion.update({tag : leer_tags(driver, step, tag)})
    
    tag = 'Urgencia Impostergable'
    licitacion.update({tag : leer_tags(driver, step, tag)})
    
    tag = 'Licitación sin Convocatoria Pública'
    licitacion.update({tag : leer_tags(driver, step, tag)})
    
    print('Datos de licitación guardados')
    
    dest_path = (os.getcwd() +
                 '\\docs\\' + 
                 licitacion['convocante'] + 
                 '\\' + 
                 re.search("(\d{4})", licitacion['fecha_publicacion']).group(0) +
                 '\\' +
                 licitacion['id_licitacion'] + ' ' +            
                 re.search("(\d{4})", licitacion['fecha_publicacion']).group(0) + 
                 '\\') 
    #Asegurar que la carpeta de licitacion existe
    down_utils.make_path(dest_path)
    
    if step == 'convocatoria':
        #funcion PBC: ir a documentos -> descargar PBC
        PBC_down = PBC(driver)
        if PBC_down == True:
            directory = 'Downloads' #Carpeta default para descargar archivos. Configurado también al inciar Selenium
            descarga_PBC = down_utils.wait_rename(dest_path, directory, timeout = 30)
            PBC_path = Path(dest_path)
            licitacion.update({'PBC_download' : descarga_PBC})
            licitacion.update({'PBC_path' : PBC_path})
        else:
            licitacion.update({'PBC_path' : ''})
            licitacion.update({'PBC_download' : False})

        #funcion invitados: ir a pestaña de invitados si es que existe -> guardar lista
        lista_invitados = invitados(driver)
        licitacion.update({'invitados' : lista_invitados})
        
        
    if step == 'adjudicacion':
        #funcion oferentes: ir a pestaña oferentes presentados y guardar lista
        pass
    #ir a la pestaña de convocatoria
        
        #funcion PBC
        PBC_down = PBC(driver)
        if PBC_down == True:
            directory = 'Downloads' #Carpeta default para descargar archivos. Configurado también al inciar Selenium
            descarga_PBC = down_utils.wait_rename(dest_path, directory, timeout = 30)
            PBC_path = Path(dest_path)
            licitacion.update({'PBC_download' : descarga_PBC})
            licitacion.update({'PBC_path' : PBC_path})
        else:
            licitacion.update({'PBC_path' : None})            
            licitacion.update({'PBC_download' : False})
        #funcion invitados
        lista_invitados = invitados(driver)
        licitacion.update({'invitados' : lista_invitados})
    

    if step == 'licitacion':
        #funcion oferentes: ir a pestaña oferentes presentados y guardar lista
        licitacion.update({'PBC_path' : None})            
        licitacion.update({'PBC_download' : False})
        #funcion invitados
        lista_invitados = invitados(driver)
        licitacion.update({'invitados' : lista_invitados})

    try:
        ul_steps = driver.find_element_by_xpath(xp_ul_steps) #xp definido al inicio
        ul_steps.find_element_by_link_text("Adjudicación").click()
    except:
        pass

    return licitacion       

        
        

  

   
        

        
