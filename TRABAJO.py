# INTEGRANTES: Diego Mario Salamanca Cardenas
#              Salomé Rodríguez Vélez


from validaciones import *
from funciones_admin import *
from funciones_responsables import *
import pymysql
from pymongo import MongoClient
from colorama import Fore, Style
import datetime
import pymongo


while True:
    print("="*40)
    menu_login = input(""" Que desea hacer
    #1. ingresar al sistema
    #2. cambiar contraseña
    #3. Salir
    -> """)
    print("="*40)
    menu_login = validar_login(menu_login)
    if menu_login == 1:
        print("\n VALIDACIÓN DE USUARIO !!! \n")
        # vamos a crear una varibale que tenga la informacion de los usuarios en xml
        administradores_xml = cargar_administradores_xml()
        id_usuario = input("Ingrese su id de usuario. \n -> ")
        id_usuario = validar_id(id_usuario)
        clave_usuario = input("cual es la clave de su usuario \n -> ")
        responsables_MySQL = datos_MySQL()
        responsables_Mongo = datos_Mongo()
        lista_usuarios_completa = administradores_xml + \
            responsables_MySQL + responsables_Mongo
        if validar_ingreso_usuario(id_usuario, clave_usuario, lista_usuarios_completa):
            while True:
                print("=" * 40)
                print("\nINGRESO A LA SECCION DE GESTION DE INFORMACION ")
                menu_principal = input("""Que informacion desea gestionar:
                            #1. Gestionar informacion de administradores.
                            #2. Gestionar informacion de responsables de prueba.
                            #3. Salir.
                            ->  """)
                menu_principal = validar_menu_principal(menu_principal)
                if menu_principal == 1:
                    if validar_administrador(administradores_xml, id_usuario, clave_usuario):
                        menu_administrador = input("""Que desea hacer usted como administrador:
                                                #1. Crear un usuario de tipo administrativo
                                                #2. Ver un administrador
                                                #3. Actualizar informacion de un administrador (busque por la cedula)
                                                #4. Eliminar a un administrador (busqueda por cedula)
                                                #5. Ingresar un responsable de prueba
                                                #6. Ver informacion de un responsable de prueba (busqueda por la cedula)
                                                #7. Actualizar la informacion de un responsable (busqueda por cedula)
                                                #8. Ver la informacion de todas las pruebas echas por un responsable (busqueda por cedula)
                                                #9. Ver los materiales estudiados por todos los responsables
                                                #10. Eliminar a un responsable de prueba (busqueda por cedula )
                                                #11. volver al menu principal
                                                ->  """)
                        print("=" * 80)
                        menu_administrador = validar_menu(
                            menu_administrador)
                        if menu_administrador == 1:
                            def validar_alfabetico(cadena):
                                return bool(re.match(r'^[a-zA-Z ]+$', cadena))
                            while True:
                                nombre_nuevo_admin = input(
                                    "Cual es nombre del nuevo administrador \n -> ")
                                if not validar_alfabetico(nombre_nuevo_admin):
                                    print(
                                        Fore.RED + "ERROR! El nombre debe contener solo letras y espacios." + Style.RESET_ALL)
                                    continue
                                else:
                                    break
                            while True:
                                try:
                                    clave_nuevo_admin = int(
                                        input("Ingrese su contraseña para ingresar como administrador \n -> "))
                                    id_nuevo_admin = int(
                                        input("Cual es el id del nuevo administrador \n-> "))
                                    break
                                except ValueError:
                                    print(
                                        Fore.RED + "ERROR! la clave como el id deben ser extrictamente numericos" + Style.RESET_ALL)
                            clave_nuevo_admin = str(clave_nuevo_admin)
                            id_nuevo_admin = str(id_nuevo_admin)
                            id_nuevo_admin = nueve_cifras(id_nuevo_admin)
                            id_nuevo_admin = str(id_nuevo_admin)
                            usuarios = crear_usuarios(
                                clave_nuevo_admin, nombre_nuevo_admin, id_nuevo_admin)
                            crear_admin(usuarios)
                        elif menu_administrador == 2:
                            while True:
                                try:
                                    id_busqueda = int(
                                        input("Cual es el id del administrador a buscar \n -> "))
                                    print("="*40)
                                    break
                                except ValueError:
                                    print(
                                        Fore.RED + "ERROR! el id deben ser extrictamente numerico" + Style.RESET_ALL)
                            id_busqueda = str(id_busqueda)
                            if buscar_usuario_por_clave(id_busqueda):
                                diccionario_admin = buscar_usuario_por_clave(
                                    id_busqueda)
                                for clave, valor in diccionario_admin.items():
                                    print(f"{Fore.GREEN + clave.upper() +
                                          Style.RESET_ALL}: {valor}")
                            else:
                                print(
                                    Fore.CYAN + "No se encontro ningun administrador con ese id" + Style.RESET_ALL)
                                continue
                        elif menu_administrador == 3:
                            def validar_alfabetico(cadena):
                                return bool(re.match(r'^[a-zA-Z ]+$', cadena))
                            while True:
                                try:
                                    id_busqueda = int(
                                        input("Cual es el id del administrador a buscar \n -> "))
                                    break
                                except ValueError:
                                    print(
                                        Fore.RED + "ERROR! el id deben ser extrictamente numerico" + Style.RESET_ALL)
                            id_busqueda = str(id_busqueda)
                            if buscador_cedula(id_busqueda):
                                while True:
                                    nuevo_nombre = input(
                                        "Cual es el nuevo nombre del usuario: \n -> ")
                                    if not validar_alfabetico(nuevo_nombre):
                                        print(
                                            Fore.RED + "ERROR! El nombre debe contener solo letras y espacios." + Style.RESET_ALL)
                                        continue
                                    else:
                                        break
                                nueva_clave = input(
                                    " Cual es la nueva clave del usuario: \n -> ")
                                nueva_clave = es_numero(nueva_clave)
                                modificar_usuario_admin(
                                    id_busqueda, nuevo_nombre, nueva_clave)
                            else:
                                print(
                                    Fore.CYAN + "\nNo se encontro el administrador al que pretendia editar su informacion." + Style.RESET_ALL)
                                continue
                        elif menu_administrador == 4:
                            id_busqueda = input(
                                "Cual es el id del administrador a eliminar \n -> ")
                            id_busqueda = es_numero(id_busqueda)
                            if eliminar_admin(id_busqueda):
                                print(Fore.CYAN + f"Usuario con ID {
                                      id_busqueda} eliminado correctamente." + Style.RESET_ALL)
                            else:
                                print(Fore.RED + f"Usuario con ID {
                                      id_busqueda} NO  se encontro." + Style.RESET_ALL)
                        elif menu_administrador == 5:
                            tupla_info = solicitar_informacion()
                            insertar_informacion_MySQL(tupla_info)
                            insertar_informacion_mongodb(tupla_info)
                            print(
                                Fore.CYAN + "\nLISTO, se cargo la informacion en ambas bases de datos." + Style.RESET_ALL)
                            print("="*80)
                        elif menu_administrador == 6:
                            documento_I = input(
                                "Escriba el documento del responsable de prueba para ver su informacion. \n-> ")
                            print(" ")
                            documento_I = nueve_cifras(documento_I)
                            documento_I = es_numero(documento_I)
                            ver_informacion(documento_I)
                        elif menu_administrador == 7:
                            print("\n PROCESO DE ACTUALIZACION RESPONSABLE. \n")
                            print("=" * 40)
                            print("SOLICITUD DE INFORMACION NUEVA\n")
                            diccionario_info = solicitar_informacion_nueva()
                            print(
                                Fore.CYAN + "\nListo, ya se cargo la informacion del responsable a actualizar. \n " + Style.RESET_ALL)
                            actualizar_informacion(diccionario_info)
                        elif menu_administrador == 8:
                            documento_I = input(
                                "Cual es documento del responsable del cual quiere saber los resultados \n ->  ")
                            print(" ")
                            print("="*40)
                            documento_I = nueve_cifras(documento_I)
                            obtener_resultados_pruebas(documento_I)
                            buscar_responsable_y_resultados_por_documento(
                                documento_I, uri="mongodb://localhost:27017/")
                        elif menu_administrador == 9:
                            materiales_estudiados = obtener_materiales_responsables(
                                uri_mongo="mongodb://localhost:27017/")
                            for i in materiales_estudiados:
                                print(f" MATERIAL - FECHA - RESPONSABLE: {i}")
                        elif menu_administrador == 10:
                            cedula = input(
                                "Ingrese la cedula del responsable a eliminar de la tabla o coleccion \n-> ")
                            cedula = nueve_cifras(cedula)
                            nuevo_codigo = int(input(
                                "digite el nuevo codigo del responsbale que se hara cargo de esa prueba \n -> "))
                            print("="*40)
                            eliminar_sustitucion_responsable_mongo(
                                cedula, nuevo_codigo, uri_mongo="mongodb://localhost:27017/")
                            eliminar_sustitucion_responsable(
                                cedula, nuevo_codigo)
                        elif menu_administrador == 11:
                            print(
                                Fore.CYAN + "USTED DECIDIO SALIR DEL MENU PARA ADMINISTRADORES " + Style.RESET_ALL)
                            break
                        elif menu_administrador == "out":
                            print(
                                Fore.RED + "Por exceso de errores usted fue expulsado de las funciones como administrador, por favor loguese" + Style.RESET_ALL)
                            break

                    else:
                        print(
                            Fore.RED + "Usted no puede ingresar. Su informacion no corresponde con algun administrador" + Style.RESET_ALL)
                        break

                elif menu_principal == 2:
                    menu_responsable = input(""" Que opcion desea ejecutar como responsable
                                            1.Cambiar contraseña
                                            2.Ver datos personales
                                            3.Actualizar datos personales
                                            4.Ingresar nuevo resultado de prueba de material
                                            5.Importar resultados de prueba. 
                                            6.Actualizar  la  información  de resultados  de  pruebas.
                                            7.Ver  la  información  del resultado de una de  las  pruebas de  material.  
                                            8.Ver todos los resultados de todas la pruebas realizadas.
                                            9.Eliminar un resultado de prueba. 
                                            10.Volver al menú principal 
                                             -> """)
                    print(" ")
                    menu_responsable = validar_menu(menu_responsable)
                    print("="*40)
                    if menu_responsable == 1:
                        nueva_contraseña = input(
                            "cual sera su  nueva contraseña \n -> ")
                        print("="*40)
                        cambiar_contraseñas(id_usuario, nueva_contraseña)
                    elif menu_responsable == 2:
                        id_usuario = int(id_usuario)
                        ver_informacion_responsable(id_usuario)
                    elif menu_responsable == 3:
                        editar_responsable(id_usuario)
                    elif menu_responsable == 4:
                        agregar_prueba()
                    elif menu_responsable == 5:
                        nombre_archivo = input(
                            "Nombre del archivo con las pruebas que usted hizo \n -> ")
                        print("="*40)
                        importar_resultados_prueba(nombre_archivo)
                    elif menu_responsable == 6:
                        numero_serie = input(
                            "Digite el serial de la probeta que quiere analizar.\n -> ")
                        actualizar_resultados_pruebas(numero_serie)
                    elif menu_responsable == 7:
                        serial_probeta = input(
                            "Cual es el numero serial que corresponde a la probeta donde analizo el material \n -> ")
                        ver_informacion_prueba(serial_probeta)
                    elif menu_responsable == 8:
                        ver_todos_los_resultados()
                    elif menu_responsable == 9:
                        serial_probeta = input(
                            "Ingrese el serial de la probeta a eliminar. \n -> ")
                        print("")
                        eliminar_resultado_prueba(serial_probeta)
                    elif menu_responsable == 10:
                        print(
                            Fore.CYAN + "USTED DECIDIO SALIR DEL MENU PARA RESPONSABLES " + Style.RESET_ALL)
                        break
                    elif menu_responsable == "out":
                        print("="*40)
                        print(
                            Fore.RED + "Por exceso de errores usted fue expulsado de las funciones como responsable por favor loguese" + Style.RESET_ALL)
                        print("="*40)
                        break
                elif menu_principal == 3:
                    break

                else:
                    print(
                        Fore.RED + "DIGITE EL NUMERO QUE CORRESPONDE A UNA DE LAS TRES OPCIONES DISPONIBLES" + Style.RESET_ALL)
        else:
            print(
                Fore.RED + "No se le permitio el acceso al programa \n " + Style.RESET_ALL)
            print("=" * 40)
            continue
    elif menu_login == 2:
        id_usuario = input("Cual es su documento de identidad. \n -> ")
        id_usuario = nueve_cifras(id_usuario)
        nueva_contraseña = input(
            "Cual es la nueva contraseña para ingresar al sistema. \n -> ")
        actualizar_contraseña(id_usuario, nueva_contraseña)

    elif menu_login == 3:
        administradores_xml = cargar_administradores_xml()
        responsables_MySQL = datos_MySQL()
        responsables_Mongo = datos_Mongo()
        lista_usuarios_completa = administradores_xml + \
            responsables_MySQL + responsables_Mongo
        id_usuario = input("Ingrese su id de usuario para salir. \n -> ")
        id_usuario = validar_id(id_usuario)
        if salir_del_menu(id_usuario, lista_usuarios_completa):
            print(Fore.CYAN + "USTED SALIO DEL PROGRAMA " + Style.RESET_ALL)
            break
        else:
            print(Fore.CYAN + "PERMANECE EN EL PROGRAMA" + Style.RESET_ALL)
