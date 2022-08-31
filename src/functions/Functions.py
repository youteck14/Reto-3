# -*- coding: utf-8 -*-
import allure
from selenium import webdriver
from functions.Inicializar  import Inicializar
from selenium.webdriver.ie.options import  DesiredCapabilities
from selenium.webdriver.chrome.options import Options as OpcionesChrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, NoSuchWindowException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common import by
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import openpyxl
import pytest
import time
import os
import json
import datetime
import re
import pyodbc
import shutil

#ACTUALIZACION WEBDRIVER MANAGER QUE IMPORTA LOS DRIVERS
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


Scenario = {}#INICIALIZAMMOS LA VARIABLE GLOBAL SCENARIO
horaGlobal = time.strftime(Inicializar.HourFormat)  # formato 24 houras
diaGlobal= time.strftime(Inicializar.DateFormat)  # formato aaaa/mm/dd


class Functions(Inicializar):
    ##########################################################################
    ##############   -=_INICIALIZAR DRIVERS_=-   #############################
    ##########################################################################
    def abrir_navegador(self, URL=Inicializar.URL, navegador=Inicializar.NAVEGADOR):
        print("Directorio Base: " + Inicializar.basedir)
        self.ventanas = {}
        print("----------------")
        print(navegador)
        print("---------------")

        if navegador == ("IExplorer"):
            caps = DesiredCapabilities.INTERNETEXPLORER.copy()
            caps["platform"] = "WINDOWS"
            caps["browserName"] = "internet explorer"
            caps["ignoreZoomSetting"] = True  # zoom 100%
            caps["requireWindowFocus"] = True
            caps["nativeEvents"] = True
            self.driver = webdriver.Ie(Inicializar.basedir + "\\drivers\\IEDriverServer.exe", caps)
            self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            self.driver.get(URL)  # abrimos el url
            self.ventanas = {'Principal': self.driver.window_handles[0]}  # la ventana numero 0
            print(self.ventanas)
            return self.driver

        if navegador == ("CHROME"):
            options = OpcionesChrome()
            options.add_argument('start-maximized')  # maximizamos
            # self.driver = webdriver.Chrome(chrome_options=options,
            #                               executable_path=Inicializar.basedir + "\\drivers\\chromedriver.exe")

            # la linea de abajo es una actualizacion ya que ahora lo maneja el mismo webdrivermanager directamente
            # delegamos exectuable_path al chromedrivermanager sin necesidad de darle el path
            # no instalar nada ni un binario
            self.driver = webdriver.Chrome(chrome_options=options, executable_path=ChromeDriverManager().install())
            self.driver.implicitly_wait(10)
            self.driver.get(URL)
            self.ventanas = {'Principal': self.driver.window_handles[0]}
            return self.driver

        if navegador == ("FIREFOX"):
            self.driver = webdriver.Firefox()
            self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            self.driver.get(URL)
            self.ventanas = {'Principal': self.driver.window_handles[0]}
            return self.driver

    def tearDown(self):
        print("Se cerrara el DRIVER")
        self.driver.quit()

    ##########################################################################
    ##############       -=_lOCATORS   HANDLE _=-              ###############
    ##########################################################################

    def xpath_element(self, XPATH):
        elements = self.driver.find_element(by=By.XPATH, value=XPATH)
        print("Xpath_Elements: Se interactuo con el elemento " + XPATH)
        return elements

    def _xpath_element(self, XPATH):
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.visibility_of_element_located((By.XPATH, XPATH)))
            elements = self.driver.find_element(by=By.XPATH, value=XPATH)
            print(u"Esperar_Elemento: Se visualizo el elemento " + XPATH)
            return elements

        except TimeoutException:
            print(u"Esperar_Elemento: No presente " + XPATH)
            Functions.tearDown(self)
        except NoSuchElementException:
            print(u"Esperar_Elemento: No presente " + XPATH)
            Functions.tearDown(self)

    def id_element(self, ID):
        elements = self.driver.find_element(by=By.ID, value=ID)
        print("Xpath_Elements: Se interactuo con el elemento " + ID)
        return elements

    def _id_element(self, ID):
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, ID)))
            elements = self.driver.find_element(by=By.ID, value=ID)
            print(u"Esperar_Elemento: Se visualizo el elemento " + ID)
            return elements

        except TimeoutException:
            print(u"Esperar_Elemento: No presente " + ID)
            Functions.tearDown(self)
        except NoSuchElementException:
            print(u"Esperar_Elemento: No presente " + ID)
            Functions.tearDown(self)

    def name_element(self, name):
        elements = self.driver.find_element(by=By.NAME, value=name)
        print("Xpath_Elements: Se interactuo con el elemento " + name)
        return elements

    def _name_element(self, name):
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, name)))
            elements = self.driver.find_element(by=By.NAME, value=name)
            print(u"Esperar_Elemento: Se visualizo el elemento " + name)
            return elements

        except TimeoutException:
            print(u"Esperar_Elemento: No presente " + name)
            Functions.tearDown(self)
        except NoSuchElementException:
            print(u"Esperar_Elemento: No presente " + name)
            Functions.tearDown(self)

    ##########################################################################
    ##############       -=_JSON     HANDLE _=-              #################
    ##########################################################################

    # def __init__(self):
    # self.json_GetFieldBy = None
    # almacenamos dos variables globales
    # self.json_ValueToFind = None

    def get_json_file(self, file):  # CARGAMOS EL JSON QUE VAMOS A UTILIZAR
        json_path = Inicializar.Json + "/" + file + '.json'
        try:
            with open(json_path, "r") as read_file:  # abrimos json pat en forma de lectura
                self.json_strings = json.loads(read_file.read())  # cargamos todo su contenido
                print("get_jso_file: " + json_path)  # abrimos
                print(self.json_strings)
                return self.json_strings  # agarramos en una variable global
        except FileNotFoundError:
            self.json_strings = False
            pytest.skip(u"get_json_file: No se encontro el Archivo" + file)  # ls prueba se hace un skip
            Functions.tearDown(self)

    def get_entity(self, entity):  # con el metodo getEntity obtenemos las entidades y propiedades del archivo json
        if self.json_strings is False:
            print("Define el DOM para esta prueba")
        else:
            try:
                self.json_ValueToFind = self.json_strings[entity]["ValueToFind"]  # obtenemos los datos
                self.json_GetFieldBy = self.json_strings[entity]["GetFieldBy"]  # obtenemos campo de
                # print(self.json_ValueToFind,self.json_GetFieldBy)
                return True

            except KeyError:
                pytest.skip(u"get_entity: No se encontro la key a la cual se hace referencia: " + entity)
                # self.driver.close()
                Functions.tearDown(self)
                return None

    def get_elements(self, entity, MyTextElement=None):
        Get_Entity = Functions.get_entity(self, entity)

        if Get_Entity is None:
            print("No se encontro el valor en el Json definido")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    elements = self.driver.find_element(by=By.ID, value=self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "name":
                    elements = self.driver.find_element(by=By.NAME, value=self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "xpath":
                    if MyTextElement is not None:
                        self.json_ValueToFind = self.json_ValueToFind.format(MyTextElement)
                        print(self.json_ValueToFind)
                    elements = self.driver.find_element(by=By.XPATH, value=self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "link":
                    elements = self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value=self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "css":
                    elements = self.driver.find_element(by=By.CSS_SELECTOR, value=self.json_ValueToFind)

                print("get_elements: " + self.json_ValueToFind)
                return elements

            except NoSuchElementException:
                print("get_text: No se encontró el elemento: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except TimeoutException:
                print("get_text: No se encontró el elemento: " + self.json_ValueToFind)
                Functions.tearDown(self)

    def get_text(self, entity,
                 MyTextElement=None):  # NOS SIRVE PARA COMPARAR EN UN ASSERTION OSEA NOS DA EL TEXTO PARA COMPARAR
        Get_Entity = Functions.get_entity(self, entity)

        if Get_Entity is None:
            print("No se encontro el valor en el Json definido")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    elements = self.driver.find_element(by=By.ID, value=self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "name":
                    elements = self.driver.find_element(by=By.NAME, value=self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "xpath":
                    if MyTextElement is not None:
                        self.json_ValueToFind = self.json_ValueToFind.format(MyTextElement)
                        print(self.json_ValueToFind)
                    elements = self.driver.find_element(by=By.XPATH, value=self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "link":
                    elements = self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value=self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "css":
                    elements = self.driver.find_element(by=By.CSS_SELECTOR, value=self.json_ValueToFind)

                print("get_text: " + self.json_ValueToFind)
                print("Text Value : " + elements.text)
                return elements.text

            except NoSuchElementException:
                print("get_text: No se encontró el elemento: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except TimeoutException:
                print("get_text: No se encontró el elemento: " + self.json_ValueToFind)
                Functions.tearDown(self)

    def get_select_elements(self, entity):
        Get_Entity = Functions.get_entity(self, entity)

        if Get_Entity is None:
            print("No se encontro el valor en el Json definido")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    select = Select(self.driver.find_element(by=By.ID, value=self.json_ValueToFind))

                if self.json_GetFieldBy.lower() == "name":
                    select = Select(self.driver.find_element(by=By.NAME, value=self.json_ValueToFind))

                if self.json_GetFieldBy.lower() == "xpath":
                    select = Select(self.driver.find_element(by=By.XPATH, value=self.json_ValueToFind))

                if self.json_GetFieldBy.lower() == "link":
                    select = Select(self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value=self.json_ValueToFind))

                print("get_select_elements: " + self.json_ValueToFind)
                return select

            # USO

            #       select by visible text  #       select.select_by_visible_text('Banana')

            #       select by value  #       select.select_by_value('1')

            except NoSuchElementException:
                print("No se encontró el elemento: " + self.json_ValueToFind)
                Functions.tearDown(self)

            except TimeoutException:
                print("No se encontró el elemento: " + self.json_ValueToFind)
                Functions.tearDown(self)

    ##########################################################################
    ##############       -=_TEXTBOX & COMBO HANDLE _=-   #################
    ##########################################################################

    def select_by_text(self, entity, text):  # SLEECCIONAMOS DE UN TEXTBOX UNA OPCION
        Functions.get_select_elements(self, entity).select_by_visible_text(text)

    def send_key_text(self, entity, text):  # ENVIAMOS VALORES A LOS CAMPOS
        Functions.get_elements(self, entity).clear()  # Limpia el campo correspondiente
        Functions.get_elements(self, entity).send_keys(text)  # envias los valores

    def send_especific_keys(self, element,
                            key):  # PODEMOS USAR EL ENVIO DE DIFERENTES TECLAS COMO EL ENTER, SPACIO, ETC
        if key == 'Enter':
            Functions.get_elements(self, element).send_keys(Keys.ENTER)
        if key == 'Tab':
            Functions.get_elements(self, element).send_keys(Keys.TAB)
        if key == 'Space':
            Functions.get_elements(self, element).send_keys(Keys.SPACE)
        time.sleep(3)

    def switch_to_iframe(self, Locator):  # CAMBIAR ENTRE VENTANAS
        iframe = Functions.get_elements(self, Locator)
        self.driver.switch_to.frame(iframe)
        print(f"Se realizó el switch a {Locator}")

    def switch_to_parentFrame(self):  # FRAME PADRE
        self.driver.switch_to.parent_frame()

    def switch_to_windows_name(self, ventana):
        if ventana in self.ventanas:  # APROVECHAMOS EL DICCIONARIO VENTAS
            self.driver.switch_to.window(self.ventanas[ventana])  # SI EXSITE SALTAMOS A ESA VENTANA
            Functions.page_has_loaded(self)
            print("volviendo a " + ventana + " : " + self.ventanas[ventana])
        else:
            self.nWindows = len(self.driver.window_handles) - 1  # VERIFICAMOS CUANTAS VENTANAS HAY ABIERTAS
            self.ventanas[ventana] = self.driver.window_handles[int(self.nWindows)]  # CREAMOS LA KEY
            self.driver.switch_to.window(self.ventanas[ventana])  # SWICHEA A ESA VENTANA
            self.driver.maximize_window()  # MAXIMIZA
            print(self.ventanas)  # IMPRIME LAS VENTANAS
            print("Estas en " + ventana + " : " + self.ventanas[ventana])
            Functions.page_has_loaded(self)  # CAPTURA LA VENTANA SI YA CARGO O NO

    ######################   -=_JAVASCRIPT_=-   #############################
    ##########################################################################

    def new_window(self, URL):  # ABRIMOS UNA NUEVA VENTANA
        self.driver.execute_script(f'''window.open("{URL}","_blank");''')
        Functions.page_has_loaded(self)

    def page_has_loaded(self):  # CAPTURA SI LA VENTANA YA CARGO O NO
        driver = self.driver
        print("Checking if {} page is loaded.".format(self.driver.current_url))
        page_state = driver.execute_script(
            'return document.readyState;')  # OBETENMOS EL ESTADO DE LA CARGA CON document.readyState
        yield
        WebDriverWait(driver, 30).until(lambda driver: page_state == 'complete')
        assert page_state == 'complete', "No se completo la carga"

    def scroll_to(self, locator):  # FUNCION PARA HACER SCROLL DE JAVASCRIPT
        Get_Entity = Functions.get_entity(self, locator)

        if Get_Entity is None:
            return print("No se encontro el valor en el Json definido")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    localizador = self.driver.find_element(By.ID, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].scrollIntoView();", localizador)  # EN ESTE CASO SCROLL
                    print(u"scroll_to: " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "xpath":
                    localizador = self.driver.find_element(By.XPATH, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].scrollIntoView();", localizador)
                    print(u"scroll_to: " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "link":
                    localizador = self.driver.find_element(By.PARTIAL_LINK_TEXT, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].scrollIntoView();", localizador)
                    print(u"scroll_to: " + locator)
                    return True

            except TimeoutException:
                print(u"scroll_to: No presente " + locator)
                Functions.tearDown(self)

    def js_clic(self, locator, MyTextElement=None):
        Get_Entity = Functions.get_entity(self, locator)
        Functions.esperar_elemento(self, locator, MyTextElement)
        if Get_Entity is None:
            return print("No se encontro el valor en el Json definido")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    localizador = self.driver.find_element(By.ID, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].click();", localizador)  # EN ESTE CASO CLICK
                    print(u"Se hizo click en: " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "xpath":
                    if MyTextElement is not None:
                        self.json_ValueToFind = self.json_ValueToFind.format(MyTextElement)
                        print(self.json_ValueToFind)

                    localizador = self.driver.find_element(By.XPATH, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].click();", localizador)
                    print(u"Se hizo click en: " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "link":
                    localizador = self.driver.find_element(By.PARTIAL_LINK_TEXT, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].click();", localizador)
                    print(u"Se hizo click en: " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "name":
                    localizador = self.driver.find_element(By.NAME, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].click();", localizador)
                    print(u"Se hizo click en: " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "css":
                    localizador = self.driver.find_element(By.CSS_SELECTOR, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].click();", localizador)
                    print(u"Se hizo click en: " + locator)
                    return True

            except TimeoutException:
                print(u"js_clic: No presente " + locator)
                Functions.tearDown(self)

    ##############   -=_Wait Elements_=-   #############################
    ##########################################################################
    def esperar(self, timeLoad=8):  # METODO PARA ESPERAR
        print("Esperar: Inicia (" + str(timeLoad) + ")")
        try:
            totalWait = 0
            while (totalWait < timeLoad):
                # print("Cargando ... intento: " + str(totalWait))
                time.sleep(1)
                totalWait = totalWait + 1
        finally:
            print("Esperar: Carga Finalizada ... ")

    def alert_windows(self, accept="accept"):
        try:
            wait = WebDriverWait(self.driver, 30)  # ESPERA HASTA 30 SEGUNDOS
            wait.until(EC.alert_is_present(), print("Esperando alerta..."))  # EC = ESPECTED CONDITION
            # LE DECIMOS QUE ESPERE UNA VENTANA DE ALERTA
            alert = self.driver.switch_to.alert  # CUANDO APAREZCA LA ALERTA LA CAPTURARA Y HARA UN SWITCH A DONDE ESTA ELLA

            print(alert.text)  # SE IMPRIME EL TEXTO QUE TIENE EN EL INTERIOR

            if accept.lower() == "accept":
                alert.accept()  # CLICK EN ACEPTAR
                print("Click in Accept")
            else:
                alert.dismiss()  # CLICK EN DISMISS
                print("Click in Dismiss")

        except NoAlertPresentException:
            print('Alerta no presente')
        except NoSuchWindowException:
            print('Alerta no presente')
        except TimeoutException:
            print('Alerta no presente')

    def esperar_elemento(self, locator, MyTextElement=None):
        Get_Entity = Functions.get_entity(self, locator)

        if Get_Entity is None:
            return print("No se encontro el valor en el Json definido")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.ID, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.ID, self.json_ValueToFind)))
                    print(u"Esperar_Elemento: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "name":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.NAME, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.NAME, self.json_ValueToFind)))
                    print(u"Esperar_Elemento: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "xpath":
                    wait = WebDriverWait(self.driver, 20)
                    if MyTextElement is not None:
                        self.json_ValueToFind = self.json_ValueToFind.format(MyTextElement)
                        print(self.json_ValueToFind)

                    wait.until(EC.visibility_of_element_located((By.XPATH, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.XPATH, self.json_ValueToFind)))
                    print(u"Esperar_Elemento: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "link":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                    print(u"Esperar_Elemento: Se visualizo el elemento " + locator)
                    return True

            except TimeoutException:
                print(u"Esperar_Elemento: No presente " + locator)
                Functions.tearDown(self)
            except NoSuchElementException:
                print(u"Esperar_Elemento: No presente " + locator)
                Functions.tearDown(self)

    ##########################################################################
    #################   -=_VERIFICACION _=-                ###################
    ##########################################################################

    def check_element(self, locator):  # devuelve true o false----tst_010
        Get_Entity = Functions.get_entity(self, locator)

        if Get_Entity is None:
            print("No se encontro el valor en el Json definido")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.ID, self.json_ValueToFind)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "name":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.NAME, self.json_ValueToFind)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "xpath":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.XPATH, self.json_ValueToFind)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "link":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "css":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.json_ValueToFind)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

            except NoSuchElementException:
                print("get_text: No se encontró el elemento: " + self.json_ValueToFind)
                return False
            except TimeoutException:
                print("get_text: No se encontró el elemento: " + self.json_ValueToFind)
                return False

    def assert_text(self, locator, TEXTO):#COMPARA EL VALOR DE UN TEXTO ESPERADO

        Get_Entity = Functions.get_entity(self, locator)

        if Get_Entity is None:
            print("No se encontro el valor en el Json definido")
        else:
            if self.json_GetFieldBy.lower() == "id":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.ID, self.json_ValueToFind)))
                ObjText = self.driver.find_element(by=By.ID,value=self.json_ValueToFind).text

            if self.json_GetFieldBy.lower() == "name":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.NAME, self.json_ValueToFind)))
                ObjText = self.driver.find_element(by=By.NAME,value=self.json_ValueToFind).text

            if self.json_GetFieldBy.lower() == "xpath":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.XPATH, self.json_ValueToFind)))
                ObjText = self.driver.find_element(by=By.XPATH,value=self.json_ValueToFind).text

            if self.json_GetFieldBy.lower() == "link":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                ObjText = self.driver.find_element(by=By.PARTIAL_LINK_TEXT,value=self.json_ValueToFind).text

            if self.json_GetFieldBy.lower() == "css":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.json_ValueToFind)))
                ObjText = self.driver.find_element(by=By.CSS_SELECTOR,value=self.json_ValueToFind).text

        print("Verificar Texto: el valor mostrado en: " + locator + " es: " + ObjText + " el esperado es: " + TEXTO)
        assert TEXTO == ObjText, "Los valores comparados no coinciden"
    ##########################################################################
    #################   -=DATA DE ESCENARIO=-                ################
    ##########################################################################
    # VARIABLES DE ESCENARIO
    # UNA VARIABLE DE ESCENARIO ES AQUELLA VARIABLE QUE PODEMOS OBTENER
    # DE LA MISMA EJECUCION DE UNA PANTALLA COMO TAL
    def create_variable_scenary(self, key, value):  #
        Scenario[key] = value
        print(Scenario)
        print("Se almaceno la key " + key + " : " + value)

    def save_variable_scenary(self, element, variable):  # TST 12
        Scenario[variable] = Functions.get_text(self, element)  # le extraemos el texto al elemento
        print(Scenario)
        print("Se almaceno el valor " + variable + " : " + Scenario[variable])

    def get_variable_scenary(self, variable):  # TST12
        self.variable = Scenario[variable]  # OBTENEMOS LA VARIABLE DEL DICCIONARIO DE LA FUNCION save_variable_scenary
        print(f"get_variable_scenary: {self.variable}")
        return self.variable

    def compare_with_variable_scenary(self, element, variable):  # COMPARANDO VARIABLE ESCENARIO DE DISTINTOS LUGARES
        variable_scenary = str(Scenario[variable])  # variable a la que quiero consultar y la guardo
        element_text = str(Functions.get_text(self, element))  # que lo guarde como texto y que le haga un get text
        _exist = (variable_scenary in element_text)  #
        print(_exist)
        print(
            f'Comparando los valores... verificando que si {variable_scenary} esta presente en {element_text} : {_exist}')
        assert _exist == True, f'{variable_scenary} != {element_text}'

    def textDateEnvironmentReplace(self, text):  # PROCESA UN TEXTO COMO TODAY NOS TRAE LA FECHA CORRESPONDIENTE
        if text == 'today':  # TST 14
            self.today = datetime.date.today()
            text = self.today.strftime(Inicializar.DateFormat)

        if text == 'yesterday':
            self.today = datetime.date.today() - datetime.timedelta(days=1)
            text = self.today.strftime(Inicializar.DateFormat)

        if text == 'Last Month':
            self.today = datetime.date.today() - datetime.timedelta(days=30)
            text = self.today.strftime(Inicializar.DateFormat)  # STRING FORMAT TIME

        return text

    def modificar_xml_environments(self):  # ENVIRONMENT CON XML
        print("------------------------------------------------")
        print("Establenciendo Datos del Reporte....")
        JOB_NAME = "VARIABLE DE JENKINS JOB_NAME"
        os.environ['JOB_NAME']
        NODE_NAME = 'VARIABLE DE JENKINS NODE_NAME'
        os.environ['NODE_NAME']
        NAVEGADOR = Inicializar.NAVEGADOR
        print(NODE_NAME)
        print(JOB_NAME)
        print(NAVEGADOR)
        print("------------------------------------------------")

        Environment = open('../data/environment.xml', 'w')
        Template = open('../data/environment_Template.xml', 'r')

        with Template as f:
            texto = f.read()
            texto = texto.replace("JOB_NAME", JOB_NAME)
            texto = texto.replace("NODE_NAME", NODE_NAME)
            texto = texto.replace("NAVEGADOR", NAVEGADOR)

        with Environment as f:
            f.write(texto)

        Environment.close()
        Template.close()

        time.sleep(5)

        if os.path.exists("../allure-results"):  # si no existe el directorio lo cre
            shutil.rmtree("../allure-results")

        try:
            os.makedirs("../allure-results")
        except OSError:
            print("No se pudo generar la carpeta ../allure-results")

        shutil.copy("../data/environment.xml", "../allure-results")
        # Excel

    def leer_celda(self, celda):  # descargamos OPENPYXL
        wb = openpyxl.load_workbook(Inicializar.Excel)  # CARGAMOS EL LIBRO COMPLETO
        sheet = wb["DataTest"]  # LE DECIMOS QUE A DENTRO HAY UN DATATEST, OSEA UN STYLESHEET LLAMADO DATATEST
        # ACCEDIMOS A LA HOJA
        valor = str(sheet[celda].value)  # ACCEDEMOS AL VALOR DE CADA CELDA DEL SHEET
        print(u"------------------------------------")
        print(u"El libro de excel utilizado es de es: " + Inicializar.Excel)
        print(u"El valor de la celda es: " + valor)
        print(u"------------------------------------")
        return valor  # ME RETORNA EL VALOR PARA YO PODER UTILIZAR

    def escribir_celda(self, celda, valor):
        wb = openpyxl.load_workbook(Inicializar.Excel)  # ABRO EL EXCEL
        hoja = wb["DataTest"]  # ME PONGO EN LA HOJA
        hoja[celda] = valor  # LLENAMOS EL VALOR A PASAR
        wb.save(Inicializar.Excel)  # GUARDO
        print(u"------------------------------------")
        print(u"El libro de excel utilizado es de es: " + Inicializar.Excel)
        print(u"Se escribio en la celda " + str(celda) + u" el valor: " + str(valor))
        print(u"------------------------------------")

    # -------------------------------------------------------------------------------------------#
    ########## ########## ##########  Database ########## ########## ########## ########## ########
    # -------------------------------------------------------------------------------------------#
    # TEST 15
    def pyodbc_conn(self, _host=Inicializar.DB_HOST, _port=Inicializar.DB_PORT, _dbname=Inicializar.DB_DATABASE,
                    _user=Inicializar.DB_USER, _pass=Inicializar.DB_PASS):
        # INICIALIZAMOS PARA HACER LA DATA CON EL QUERY STRING
        # print(pyodbc.drivers())
        try:
            config = dict(  # NOS ARMAMOS UN DICCIONARIO
                server=_host,
                port=_port,
                database=_dbname,
                username=_user,
                password=_pass)

            conn_str = (  # GENERAMOS LA QUERY STRING
                    'SERVER={server};'
                    'PORT={port};' +
                    'DATABASE={database};' +
                    'UID={username};' +
                    'PWD={password}')
            # INSTALAMOS PYODBC EN NUESTRO ENTORNO VIRTUAL
            conn = pyodbc.connect(  # CONECTAMOS
                r'DRIVER={PostgreSQL ANSI};' +  # SIN EL DRIVER NO NOS FUNCIONARA TENEMOS QUE INSTALAR Y PONERLO EN WINDOWS
                # HERRAMIENTAS ADMINISTRATIVAS
                conn_str.format(**config))  # FORMATEAMOS CON LA CONFIGURACION CON LA DATA DEL DICCIONARIO

            self.cursor = conn.cursor()  # CUANDO SE CONECTA EL CURSOR
            print("Always Connected")  # MANDA MENSAJE
            return self.cursor  # RETORNA EL VALOR DEL CURSOR

        except (pyodbc.OperationalError) as error:  # SI ALGUNA DATA ESTA MAL ME CAPTURA LA DATA
            self.cursor = None
            pytest.skip("Error en connection strings: " + str(error))

    def pyodbc_query(self, _query):  # HACEMOS LA CONSULTA
        self.cursor = Functions.pyodbc_conn(self)
        if self.cursor is not None:
            try:
                self.cursor.execute(_query)
                self.Result = self.cursor.fetchall()
                for row in self.Result:
                    print(row)

            except (pyodbc.Error) as error:
                print("Error en la consulta", error)

            finally:
                if (self.cursor):
                    self.cursor.close()
                    print("pyodbc Se cerró la conexion")

    ##############   -=_CAPTURA DE PANTALLA_=-   #############################
    ##########################################################################

    def hora_Actual(self):  # PARA TUILIZAR LA HORA PARA CAPTURAR EL PATH CON LA HORA
        self.hora = time.strftime(Inicializar.HourFormat)  # formato 24 horas
        return self.hora

    def crear_path(self):  # CREAMOS EL PATH, LA RUTA DONDE SE ESCRIBE LA CAPTURA DE PANTALLA
        dia = time.strftime("%d-%m-%Y")  # formato aaaa/mm/dd
        GeneralPath = Inicializar.Path_Evidencias  # URL DE LAS CAPTURAS
        DriverTest = Inicializar.NAVEGADOR  # DRIVER CON EL QUE INICIO EL NAVEGADOR
        TestCase = self.__class__.__name__  # EXTRAE  EL NOMBRE A LA CLASE
        horaAct = horaGlobal  # HORA GLOBAL
        x = re.search("Context",
                      TestCase)  # Cuando un test es en base a comportamiento pierde la pripiedad de test case
        if (x):  # si dentro del path existia la palabra context el se la eliminaria
            path = f"{GeneralPath}/{dia}/{DriverTest}/{horaAct}/"  # PS ES POR ESO QUE NO SE LE PUEDE INCORPORAR AL PATH
        else:
            path = f"{GeneralPath}/{dia}/{TestCase}/{DriverTest}/{horaAct}/"

        if not os.path.exists(path):  # si no existe el directorio lo crea
            os.makedirs(path)  # LIBRERIA OS

        return path

    def capturar_pantalla(self):  # TEST 17
        PATH = Functions.crear_path(self)  # CREAMOS EL PATH
        TestCase = self.__class__.__name__  # EXTRAE  EL NOMBRE A LA CLASE
        img = f'{PATH}/{TestCase}_(' + str(Functions.hora_Actual(self)) + ')' + '.png'
        self.driver.get_screenshot_as_file(img)
        print(img)
        return img

    def captura(self, Descripcion):  #
        allure.attach(self.driver.get_screenshot_as_png(), Descripcion, attachment_type=allure.attachment_type.PNG)
        # Se mete dentro de la ruta por eso no necesita un path

    ##############   -=_ASSERTION=-   #############################
    ##########################################################################

    def validar_elemento(self, locator):  # TEST 018

        Get_Entity = Functions.get_entity(self, locator)

        TIME_OUT = 10

        if Get_Entity is None:
            return print("No se encontro el valor en el Json definido")
        else:
            try:  # TRUE PARA ELEMENTOS VISIBLES Y CLICKEABLES
                if self.json_GetFieldBy.lower() == "id":
                    wait = WebDriverWait(self.driver, TIME_OUT)
                    wait.until(EC.visibility_of_element_located((By.ID, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.ID, self.json_ValueToFind)))
                    print(u"Esperar_Elemento: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "name":
                    wait = WebDriverWait(self.driver, TIME_OUT)
                    wait.until(EC.visibility_of_element_located((By.NAME, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.NAME, self.json_ValueToFind)))
                    print(u"Esperar_Elemento: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "xpath":
                    wait = WebDriverWait(self.driver, TIME_OUT)
                    wait.until(EC.visibility_of_element_located((By.XPATH, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.XPATH, self.json_ValueToFind)))
                    print(u"Esperar_Elemento: Se visualizo el elemento " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "link":
                    wait = WebDriverWait(self.driver, TIME_OUT)
                    wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                    print(u"Esperar_Elemento: Se visualizo el elemento " + locator)
                    return True

            except TimeoutException:
                print(u"Assert_xpath: Elemento No presente " + locator)
                return False

    def ReplaceWithContextValues(self, text):  # me remplaze el text y lo haga un expresion regular
        PatronDeBusqueda = r"(?<=Scenario:)\w+"
        variables = re.findall(str(PatronDeBusqueda), text, re.IGNORECASE)
        for variable in variables:
            if variable == 'today':
                dateToday = str(datetime.date.today().strftime("%Y-%m-%dT%H:%M:%S"))
                text = re.sub('(Scenario:)([^&.]+)', dateToday, text,
                              re.IGNORECASE)  # si continee scenario y que contiene
                continue
            text = re.sub('(Scenario:)([^.]+)', Scenario[variable], text, re.IGNORECASE)
        return text


