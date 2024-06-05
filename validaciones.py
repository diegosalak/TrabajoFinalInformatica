import os
import xml.etree.ElementTree as ET
import pymysql
from pymongo import MongoClient
from colorama import Fore, Style
import pymongo
from getpass import getpass


def validar_login(menu_login):
    """
    Valida que la entrada del usuario para el menú de login sea un número.

    Args:
        menu_login (str): Entrada inicial del usuario para el menú de login.

    Returns:
        int: Opción válida seleccionada por el usuario (1 o 2).
    """
    while True:
        if menu_login.isdigit():
            menu_login = int(menu_login)
            break
        else:
            print("Dijite como opción el 1 o el 2")

            menu_login = input("""Que desea hacer
                  1. ingresar al sistema
                  2. cambiar contraseña
                  -> """)
    return menu_login


def validar_id(id_usuario):
    """
    Valida que el ID del usuario solo contenga dígitos.

    Args:
        id_usuario (str): ID del usuario a validar.

    Returns:
        str: ID del usuario validado.
    """
    while True:
        if id_usuario.isdigit():
            id_usuario = id_usuario
            break
        else:
            print(
                Fore.RED + "ERROR! Dijite su id SIN caracteres especiales, espacios o letras")
            id_usuario = input("Ingrese su id de usuario. \n -> ")
    return id_usuario


def cargar_administradores_xml():
    """
    Carga los administradores desde un archivo XML y devuelve una lista de diccionarios con su información.

    Returns:
        list: Lista de diccionarios con la información de los administradores.
    """
    administradores_xml = []
    ruta_archivo_xml = os.path.join("admin", "user.xml")
    arbol = ET.parse(ruta_archivo_xml)
    raiz = arbol.getroot()
    for usuario in raiz.findall("usuario"):
        id_usuario = usuario.get("documento_I")
        clave_usuario = usuario.find("contraseña").text
        nombre_usuario = usuario.find("nombre").text
        administradores_xml.append({"documento_I": id_usuario,
                                    "nombre": nombre_usuario,
                                    "contraseña": clave_usuario
                                    })
    return administradores_xml


def datos_MySQL():
    """
    Obtiene la información de los responsables de prueba desde una base de datos MySQL y la devuelve como una lista de diccionarios.

    Returns:
        list: Lista de diccionarios con la información de los responsables de prueba.
    """
    lista_MySQL = []
    mi_conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="info2024",
        db="Responsables_Pruebas"
    )
    cursor = mi_conexion.cursor()
    cursor.execute("SELECT * FROM Informacion_Responsables")

    columnas = [column[0] for column in cursor.description]
    resultados = cursor.fetchall()

    for fila in resultados:
        dict_fila = dict(zip(columnas, fila))
        dict_fila["documento_I"] = str(dict_fila["documento_I"])
        lista_MySQL.append(dict_fila)

    mi_conexion.close()
    return lista_MySQL


def datos_Mongo():
    """
    Obtiene la información de los responsables de prueba desde una base de datos MongoDB y la devuelve como una lista de diccionarios.

    Returns:
        list: Lista de diccionarios con la información de los responsables de prueba.
    """
    responsables_Mongo = []
    manipulador = MongoClient("localhost", 27017)
    base_dato = manipulador["Responsables_Pruebas_M"]
    coleccion = base_dato["Informacion_Responsables_M"]
    informacion = coleccion.find()
    for diccionarios in informacion:
        diccionarios["documento_I"] = str(diccionarios["documento_I"])
        responsables_Mongo.append(diccionarios)
    return responsables_Mongo


def validar_ingreso_usuario(id_usuario, clave_usuario, lista_usuarios_completa):
    """
    Valida el ingreso de un usuario comprobando su ID y contraseña contra una lista de usuarios.

    Args:
        id_usuario (str): ID del usuario.
        clave_usuario (str): Contraseña del usuario.
        lista_usuarios_completa (list): Lista de diccionarios con la información de los usuarios.

    Returns:
        bool: True si el usuario es válido, False en caso contrario.
    """
    for diccionario_usuarios in lista_usuarios_completa:
        if diccionario_usuarios["documento_I"] == id_usuario and diccionario_usuarios["contraseña"] == clave_usuario:
            print(Fore.CYAN + " \n VALIDACION EXITOSA. BIENVENIDO \n " + Style.RESET_ALL)
            return True
    print(Fore.RED + "\n La contraseña o el ID NO! se encontraron en las bases de datos " + Style.RESET_ALL)
    return False


def validar_menu_principal(menu_principal):
    """
    Valida la selección del usuario en el menú principal, asegurándose de que sea un número.

    Args:
        menu_principal (str): Entrada inicial del usuario para el menú principal.

    Returns:
        int: Opción válida seleccionada por el usuario.
    """
    while True:
        if menu_principal.isdigit():
            menu_principal = int(menu_principal)
            break
        else:
            print(
                "Los procesos disponibles a ejecutar estan referenciados con los numerales")
            menu_principal = input(""" que informacion desea gestionar:
                           #1. Gestionar informacion de administradores
                           #2. Gestionar informacion de responsables de prueba
                           #3. Gestionar resultados de prueba
                           #4. Salir
                           -> """)
    return menu_principal


def validar_administrador(administradores_xml, id_usuario, clave_usuario):
    """
    Valida el ingreso de un administrador comprobando su ID y contraseña contra una lista de administradores.

    Args:
        administradores_xml (list): Lista de diccionarios con la información de los administradores.
        id_usuario (str): ID del administrador.
        clave_usuario (str): Contraseña del administrador.

    Returns:
        bool: True si el administrador es válido, False en caso contrario.
    """
    for diccionarios_administradores_xml in administradores_xml:
        if diccionarios_administradores_xml["documento_I"] == id_usuario and diccionarios_administradores_xml["contraseña"] == clave_usuario:
            print(Fore.YELLOW + " \n !BIENVENIDO ADMINISTRADOR¡ \n " + Style.RESET_ALL)
            return True
    return False


def validar_menu(menu_administrador):
    """
    Valida la selección del administrador en el menú de administración, asegurándose de que sea un número.

    Args:
        menu_administrador (str): Entrada inicial del usuario para el menú de administración.

    Returns:
        int/str: Opción válida seleccionada por el administrador, o "out" si se excedieron los intentos.
    """
    salida = 0
    while salida < 2:
        if menu_administrador.isdigit():
            menu_administrador = int(menu_administrador)
            return menu_administrador
        else:
            print(
                "Los procesos disponibles a ejecutar estan referenciados con los numerales")
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
                                                #10. Eliminar a un responsable (busqueda por cedula )
                                                #11. volver al menu principal
                                                -> """)
            print(" ")
            salida += 1
    salida = "out"
    return salida


def validar_menu_responsable(menu_responsable):
    """
    Valida la selección del usuario responsable en el menú de responsabilidades, asegurándose de que sea un número.

    Args:
        menu_responsable (str): Entrada inicial del usuario para el menú de responsabilidades.

    Returns:
        int/str: Opción válida seleccionada por el usuario responsable, o "out" si se excedieron los intentos.
    """
    salida = 0
    while salida < 2:
        if menu_responsable.isdigit():
            menu_responsable = int(menu_responsable)
            return menu_responsable
        else:
            print(
                "Los procesos disponibles a ejecutar estan referenciados con los numerales")
            menu_responsable = input(""" Que opcion desea ejecutar como responsable
                                            1.Cambiar contraseña
                                            2.Ver datos personales
                                            3.Actualizar datos personales
                                            4.Ingresar nuevo resultado de prueba de material
                                            5.Importar resultados de prueba 
                                            6.Actualizar  la  información  de resultados  de  pruebas. 
                                            7.Ver  la  información
                                            8.Ver todos los resultados de todas la pruebas realizadas.
                                            9.Eliminar un resultado de prueba. 
                                            10.Volver al menú principal  
                                            -> """)
            print(" ")


def actualizar_contraseña_xml(id_usuario, nueva_contraseña):
    ruta_archivo_xml = os.path.join("admin", "user.xml")
    arbol = ET.parse(ruta_archivo_xml)
    raiz = arbol.getroot()

    for usuario in raiz.findall("usuario"):
        if usuario.get("documento_I") == str(id_usuario):
            usuario.find("contraseña").text = nueva_contraseña
            ET.indent(arbol)
            arbol.write(ruta_archivo_xml, encoding="utf-8",
                        xml_declaration=True)
            print(
                Fore.CYAN + "La contraseña ha sido actualizada en el archivo XML." + Style.RESET_ALL)
            return True

    print(Fore.CYAN + "El responsable no fue encontrado en el archivo XML." + Style.RESET_ALL)
    return False


def actualizar_contraseña(id_usuario, nueva_contraseña):
    """
    Actualiza la contraseña de un usuario en las bases de datos MySQL, MongoDB y el archivo XML.

    Args:
        id_usuario (str): ID del usuario cuya contraseña se va a actualizar.
        nueva_contraseña (str): Nueva contraseña del usuario.

    Returns:
        None
    """
    # Actualizar en MySQL
    conexion_mysql = pymysql.connect(
        host="localhost", user="root", password="info2024", db="Responsables_Pruebas"
    )
    cursor_mysql = conexion_mysql.cursor()

    consulta_mysql = f"SELECT * FROM Informacion_Responsables WHERE documento_I = '{
        id_usuario}'"
    cursor_mysql.execute(consulta_mysql)
    responsable_mysql = cursor_mysql.fetchone()

    if responsable_mysql:
        consulta_actualizar_mysql = f"UPDATE Informacion_Responsables SET contraseña = '{
            nueva_contraseña}' WHERE documento_I = '{id_usuario}'"
        cursor_mysql.execute(consulta_actualizar_mysql)
        conexion_mysql.commit()
        print(Fore.CYAN + "La contraseña ha sido actualizada en MySQL." + Style.RESET_ALL)
    else:
        print(Fore.CYAN + "El responsable no fue encontrado en MySQL." + Style.RESET_ALL)

    cursor_mysql.close()
    conexion_mysql.close()

    # Actualizar en MongoDB
    cliente_mongo = pymongo.MongoClient("localhost", 27017)
    base_datos = cliente_mongo["Responsables_Pruebas_M"]
    coleccion = base_datos["Informacion_Responsables_M"]

    resultado = coleccion.update_one(
        {"documento_I": int(id_usuario)},
        {"$set": {"contraseña": nueva_contraseña}}
    )

    if resultado.matched_count > 0:
        print(Fore.CYAN + "La contraseña ha sido actualizada en MongoDB." + Style.RESET_ALL)
    else:
        print(Fore.CYAN + "El responsable no fue encontrado en MongoDB." + Style.RESET_ALL)

    cliente_mongo.close()

    # Actualizar en XML
    actualizar_contraseña_xml(id_usuario, nueva_contraseña)


def obtener_contraseña_actual(id_usuario, lista_usuarios):
    """
    Obtiene la contraseña actual de un usuario a partir de una lista de usuarios.

    Args:
        id_usuario (str): ID del usuario cuya contraseña se quiere obtener.
        lista_usuarios (list): Lista de diccionarios con la información de los usuarios.

    Returns:
        str: La contraseña actual del usuario, o None si no se encuentra el usuario.
    """
    for usuario in lista_usuarios:
        if usuario["documento_I"] == id_usuario:
            return usuario["contraseña"]
    return None


def salir_del_menu(id_usuario, lista_usuarios):
    """
    Permite salir del programa después de validar la contraseña del usuario.

    Args:
        id_usuario (str): ID del usuario que quiere salir del programa.
        lista_usuarios (list): Lista de diccionarios con la información de los usuarios.

    Returns:
        bool: True si la contraseña es correcta y el usuario puede salir del programa, False en caso contrario.
    """
    contraseña_actual = obtener_contraseña_actual(id_usuario, lista_usuarios)
    if not contraseña_actual:
        print(Fore.RED + "Usuario no encontrado." + Style.RESET_ALL)
        return False

    intentos_restantes = 3
    while intentos_restantes > 0:
        contraseña_ingresada = input(
            "Ingrese su contraseña para salir del programa. \n-> ").strip()
        if contraseña_ingresada == contraseña_actual:
            print("Contraseña correcta. Saliendo del programa...")
            return True
        else:
            intentos_restantes -= 1
            print(Fore.RED + f"Contraseña incorrecta. Te quedan {
                  intentos_restantes} intentos." + Style.RESET_ALL)

    print(Fore.RED + "Has excedido el número de intentos permitidos. No se puede salir del programa." + Style.RESET_ALL)
    return False
