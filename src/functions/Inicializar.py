import os

class Inicializar():
    # Directorio Base
    basedir = os.path.abspath(os.path.join(__file__, "../.."))#EL PATH DE ACA ME LLEVA HASTA "SRC" POR ESO ESTA COMO BASE PARA TODOS
    DateFormat = '%d/%m/%Y'   #ACA PODEMOS CAMBIAR EL FORMATO DE LA FECHA
    HourFormat = "%H%M%S"

    # JsonData
    Json = basedir + u"/pages"

    Environment = 'Dev'

    # BROWSER DE PRUEBAS
    NAVEGADOR = u'CHROME'

    # DIRECTORIO DE LA EVIDENCIA
    Path_Evidencias = basedir + u'/data/capturas'

    # HOJA DE DATOS EXCEL
    Excel = basedir + u'/data/perfiles/DataTest.xlsx'

    if Environment == 'Dev':
        URL = 'http://opencart.abstracta.us/'
        User = 'postgres'
        Pass = 'para'

        Scenario = {#variables de contexto tercera mejora, ultimo video
            "ENV_ID":"74",
            "TBASE": "BASE DEV EDWIN",
            "Proceso": "Review 170",
        }
        #DATABASE CATALOG
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_DATABASE = 'curso_api'
        DB_USER = 'postgres'
        DB_PASS = 'para14'



    if Environment == 'Test':
        URL = 'http://opencart.abstracta.us/'
        User = 'myohan'
        Pass = 'paraco14'

        Scenario = {  # variables de contexto tercera mejora, ultimo video
            "ENV_ID": "74",
            "TBASE": "BASE TEST YOHAN",
            "Proceso": "Review 170",
            "email": "yohanrr86@gmail.com"
        }
        # DATABASE CATALOG
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_DATABASE = 'curso_api'
        DB_USER = 'postgres'
        DB_PASS = 'para14'

