# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:19:13 2019

@author: Hernán
"""
import re
from time import sleep

# Ejemplo licitacion con varias paginas en PBC
# https://www.contrataciones.gov.py/licitaciones/convocatoria/359250-construccion-sanitarios-sexados-aulas-reparaciones-diferentes-escuelas-colegios-ciud-1.html#documentos

  #               '//*[@id="licitaciones"]/div[2]/div/div[2]/div/ul'
#xp_ul = '//*[@id="licitaciones"]/div[2]/div/div[2]/div/ul' #ul resultado de busqueda de licitaciones
#xp_ul_paginas = '//*[@id="documentos"]/div[2]/div[2]/div[2]/div/ul' #ul resultado de busqueda de PBC

#Hacer funciones "existe siguiente página" y "pasar a siguiente página", el segundo va a usar el primero 

def siguiente_pag(driver, xp_ul):
    existe_siguiente_pagina = False
    try:
        #xp_ul = '//*[@id="licitaciones"]/div[2]/div/div[2]/div/ul'
        
        uls = driver.find_element_by_xpath(xp_ul)
        lis = uls.find_elements_by_tag_name("li")
        
        pagina_activa = uls.find_element_by_class_name("active").text #da la página activa
        pagina_activa = re.search("\d+", pagina_activa).group(0)
        
        ultima_pagina = lis[-2].text
        ultima_pagina = re.search("\d+", ultima_pagina).group(0)

        #print('La página activa es: ' + pagina_activa)
       # print('La última página es: ' + ultima_pagina)
        
        if pagina_activa != ultima_pagina: #Si la página activa no es la última página
            lis[-1].find_element_by_tag_name("a").click() #hacer click en siguiente pagina
            #sleep(10)
#            print('La página activa es: ' + pagina_activa)
#            print('La última página es: ' + ultima_pagina)
            #print('Click en siguiente página')
            existe_siguiente_pagina = True
    except:
        #existe_siguiente_pagina = False
        pass
    return existe_siguiente_pagina
    


