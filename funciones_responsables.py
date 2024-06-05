import datetime
import xml.etree.ElementTree as ET
import os
import pymysql
from pymongo import MongoClient
import json
import pymongo
from colorama import Fore, Style
from funciones_admin import *
import re


def conectar_mysql():
    """
    Conecta a la base de datos MySQL y devuelve la conexión y el cursor.

    Returns:
        tuple: Una tupla que contiene la conexión y el cursor de MySQL.
    """
    conexion = pymysql.connect(
        host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
    cursor = conexion.cursor()
    return conexion, cursor


def conectar_mongo():
    """
    Conecta a la base de datos MongoDB y devuelve el cliente y la colección.

    Returns:
        tuple: Una tupla que contiene el cliente de MongoDB y la colección.
               Devuelve (None, None) en caso de error.
    """
    try:
        cliente = pymongo.MongoClient("localhost", 27017)
        base_datos = cliente["Responsables_Pruebas_M"]
        coleccion = base_datos["Informacion_Responsables_M"]
        return cliente, coleccion
    except Exception as e:
        print(f"Error al conectar a la base de datos MongoDB: {e}")
        return None, None


def cambiar_contraseñas(documento, nueva_contraseña):
    """
    Cambia la contraseña de un usuario en las bases de datos MySQL y MongoDB.

    Args:
        documento (str): Documento de identidad del usuario.
        nueva_contraseña (str): Nueva contraseña del usuario.

    Returns:
        None
    """
    conexion_mysql = pymysql.connect(
        host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
    cursor_mysql = conexion_mysql.cursor()

    consulta_mysql = f"UPDATE Informacion_Responsables SET contraseña = '{
        nueva_contraseña}' WHERE documento_I = '{documento}'"
    cursor_mysql.execute(consulta_mysql)
    conexion_mysql.commit()

    cliente_mongo = pymongo.MongoClient("localhost", 27017)
    base_datos = cliente_mongo["Responsables_Pruebas_M"]
    coleccion = base_datos["Informacion_Responsables_M"]

    documento_int = int(documento)
    filtro = {"documento_I": documento_int}
    actualizacion = {"$set": {"contraseña": nueva_contraseña}}
    resultado = coleccion.update_one(filtro, actualizacion)

    if resultado.matched_count > 0:
        print(Fore.CYAN + "La contraseña ha sido cambiada correctamente en MongoDB." + Style.RESET_ALL)
        print(Fore.CYAN + "La contraseña ha sido cambiada correctamente en MYSQL. \n" + Style.RESET_ALL)
    else:
        print(
            Fore.CYAN + "\nEl responsable no fue encontrado en MongoDB." + Style.RESET_ALL)

    conexion_mysql.close()
    cliente_mongo.close()


def ver_informacion_responsable(id_usuario):
    """
    Muestra la información de un responsable desde MySQL o MongoDB.

    Args:
        id_usuario (str): ID del usuario cuya información se desea ver.

    Returns:
        None
    """
    conexion_mysql = pymysql.connect(
        host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
    cursor_mysql = conexion_mysql.cursor()

    consulta_mysql = f"SELECT * FROM Informacion_Responsables WHERE documento_I = '{
        id_usuario}'"
    cursor_mysql.execute(consulta_mysql)
    responsable_mysql = cursor_mysql.fetchone()

    conexion_mysql.close()

    if responsable_mysql:
        print("="*40)
        print(Fore.CYAN + "\nInformación del responsable en MySQL:" + Style.RESET_ALL)
        print(f"ID: {responsable_mysql[0]}")
        print(f"Nombre: {responsable_mysql[1]}")
        print(f"Apellido: {responsable_mysql[2]}")
        print(f"Documento de Identidad: {responsable_mysql[3]}")
        print(f"Cargo: {responsable_mysql[4]}")
        print(f"Contraseña: {responsable_mysql[5]}\n")
        print("="*40)
    else:
        cliente_mongo = pymongo.MongoClient("localhost", 27017)
        base_datos = cliente_mongo["Responsables_Pruebas_M"]
        coleccion = base_datos["Informacion_Responsables_M"]

        responsable_mongo = coleccion.find_one({"documento_I": id_usuario})
        cliente_mongo.close()

        if responsable_mongo:
            print("="*40)
            print(
                Fore.CYAN + "\nInformación del responsable en MongoDB:" + Style.RESET_ALL)
            print(f"ID: {responsable_mongo['_id']}")
            print(f"Nombre: {responsable_mongo['nombre']}")
            print(f"Apellido: {responsable_mongo['apellido']}")
            print(f"Documento de Identidad: {
                  responsable_mongo['documento_I']}")
            print(f"Cargo: {responsable_mongo['cargo']}")
            print(f"Contraseña: {responsable_mongo['contraseña']}\n")
            print("="*40)
        else:
            print(
                Fore.CYAN + "No se encontró información para el documento especificado." + Style.RESET_ALL)


def editar_responsable(id_usuario):
    """
    Edita la información de un responsable en las bases de datos MySQL y MongoDB.

    Args:
        id_usuario (str): ID del usuario cuya información se desea editar.

    Returns:
        None
    """
    def validar_alfabetico(cadena):
        return bool(re.match(r'^[a-zA-Z ]+$', cadena))

    def validar_alfanumerico(cadena):
        return bool(re.match(r'^[a-zA-Z0-9]+$', cadena))

    def nueve_cifras(documento):
        if len(documento) != 9 or not documento.isdigit():
            raise ValueError("El documento debe tener exactamente 9 cifras.")
        return documento
    conexion_mysql = pymysql.connect(
        host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
    cursor_mysql = conexion_mysql.cursor()

    consulta_mysql = f"SELECT * FROM Informacion_Responsables WHERE documento_I = '{
        id_usuario}'"
    cursor_mysql.execute(consulta_mysql)
    responsable_mysql = cursor_mysql.fetchone()

    cursor_mysql.close()
    conexion_mysql.close()

    while True:
        print("="*40)
        nuevo_apellido = input("\nIngrese el nuevo apellido: ").strip()
        nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
        nueva_contraseña = input("Ingrese la nueva contraseña: ").strip()
        nuevo_cargo = input("Ingrese el nuevo cargo: ").strip()
        nuevo_documento_i = input("Ingrese el nuevo documento: ").strip()
        print("="*40)

        if not validar_alfabetico(nuevo_apellido):
            print(
                Fore.RED + "ERROR! El apellido debe contener solo letras y espacios." + Style.RESET_ALL)
            continue

        if not validar_alfabetico(nuevo_nombre):
            print(
                Fore.RED + "ERROR! El nombre debe contener solo letras y espacios." + Style.RESET_ALL)
            continue

        if not validar_alfanumerico(nueva_contraseña):
            print(
                Fore.RED + "ERROR! La contraseña debe ser alfanumérica." + Style.RESET_ALL)
            continue

        if not validar_alfabetico(nuevo_cargo):
            print(
                Fore.RED + "ERROR! El cargo debe contener solo letras y espacios." + Style.RESET_ALL)
            continue

        try:
            nuevo_documento_i = nueve_cifras(nuevo_documento_i)
        except ValueError as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
            continue

        break

    cliente_mongo = pymongo.MongoClient("localhost", 27017)
    base_datos = cliente_mongo["Responsables_Pruebas_M"]
    coleccion = base_datos["Informacion_Responsables_M"]

    nuevo_valor = {
        "$set": {
            "apellido": nuevo_apellido,
            "nombre": nuevo_nombre,
            "contraseña": nueva_contraseña,
            "cargo": nuevo_cargo,
            "documento_I": int(nuevo_documento_i)
        }
    }
    resultado = coleccion.update_one(
        {"documento_I": int(id_usuario)}, nuevo_valor, upsert=True)

    if resultado.matched_count > 0:
        print(Fore.CYAN + "La información del responsable ha sido actualizada en MongoDB." + Style.RESET_ALL)
    else:
        print(Fore.CYAN + "El responsable no fue encontrado en MongoDB." + Style.RESET_ALL)
    print("="*40)

    cliente_mongo.close()

    if responsable_mysql:
        conexion_mysql = pymysql.connect(
            host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
        cursor_mysql = conexion_mysql.cursor()

        consulta_actualizar_mysql = f"UPDATE Informacion_Responsables SET apellido = '{nuevo_apellido}', nombre = '{nuevo_nombre}', contraseña = '{
            nueva_contraseña}', cargo = '{nuevo_cargo}', documento_I = '{nuevo_documento_i}' WHERE documento_I = '{id_usuario}'"
        cursor_mysql.execute(consulta_actualizar_mysql)
        conexion_mysql.commit()

        print(Fore.CYAN + "La información del responsable ha sido actualizada en MySQL." + Style.RESET_ALL)


def agregar_prueba():
    """
    Permite agregar una nueva prueba tanto a la base de datos MySQL como a MongoDB.

    Returns:
        None
    """
    while True:
        # Conexión a MySQL
        conexion_mysql, cursor_mysql = conectar_mysql()

        # Conexión a MongoDB
        cliente = pymongo.MongoClient("localhost", 27017)
        base_datos = cliente["Responsables_Pruebas_M"]
        coleccion_responsables = base_datos["Informacion_Responsables_M"]
        coleccion_pruebas = base_datos["informacion_pruebas"]

        # Solicitar los datos de la prueba al usuario
        print("=" * 40)
        serial_probeta = input("Ingrese el serial de la probeta.\n ->  ")
        nombre_material = input("Ingrese el nombre del material.\n ->  ")

        # Validar el resultado de tracción
        while True:
            try:
                resultado_traccion = float(
                    input("Ingrese el resultado de ensayo de tracción (deformación).\n ->  "))
                break
            except ValueError:
                print(
                    Fore.RED + "Error: Debe ingresar un valor numérico para el resultado de tracción." + Style.RESET_ALL)

        # Validar el resultado de dureza
        while True:
            try:
                resultado_dureza = float(
                    input("Ingrese el resultado de la prueba de dureza.\n->  "))
                break
            except ValueError:
                print(
                    Fore.RED + "Error: Debe ingresar un valor numérico para el resultado de dureza." + Style.RESET_ALL)

        resultado_hemocompatibilidad = input(
            "¿La prueba de hemocompatibilidad fue exitosa? (Si/No).\n->  ").lower()
        resultado_inflamabilidad = input(
            "¿La prueba de inflamabilidad fue exitosa? (Sí/No).\n->  ").lower()

        # Validar los resultados de hemocompatibilidad e inflamabilidad
        while resultado_hemocompatibilidad not in ['si', 'no'] or resultado_inflamabilidad not in ['si', 'no']:
            print(
                Fore.RED + "Error: Los resultados de hemocompatibilidad e inflamabilidad deben ser 'Si' o 'No'." + Style.RESET_ALL)
            resultado_hemocompatibilidad = input(
                "¿La prueba de hemocompatibilidad fue exitosa? (Si/No).\n->  ").lower()
            resultado_inflamabilidad = input(
                "¿La prueba de inflamabilidad fue exitosa? (Sí/No).\n->  ").lower()

        # Validar el resultado de densidad
        while True:
            try:
                densidad = float(
                    input("Ingrese el resultado de densidad.\n->  "))
                break
            except ValueError:
                print(
                    Fore.RED + "Error: Debe ingresar un valor numérico para el resultado de densidad." + Style.RESET_ALL)

        # Validar el resultado de temperatura de fusión
        while True:
            try:
                temperatura_fusion = float(
                    input("Ingrese el resultado de temperatura de fusión.\n-> "))
                break
            except ValueError:
                print(
                    Fore.RED + "Error: Debe ingresar un valor numérico para el resultado de temperatura de fusión." + Style.RESET_ALL)

        fecha_realizacion = datetime.datetime.now().strftime("%d/%m/%Y")

        # Validar el código del responsable
        while True:
            try:
                codigo_responsable = int(
                    input("Ingrese el código del responsable. \n -> "))
                break
            except ValueError:
                print(
                    Fore.RED + "Error: Debe ingresar un valor numérico para el código del responsable." + Style.RESET_ALL)
        print("="*40)

        # Validar si el código del responsable existe en MySQL
        consulta_responsable_mysql = "SELECT * FROM Informacion_Responsables WHERE codigo_responsable = %s"
        cursor_mysql.execute(consulta_responsable_mysql, (codigo_responsable,))
        responsable_mysql = cursor_mysql.fetchone()

        # Validar si el código del responsable existe en MongoDB
        responsable_mongo = coleccion_responsables.find_one(
            {"_id": codigo_responsable})

        # Insertar en MySQL si el responsable existe
        if responsable_mysql:
            consulta_mysql = """INSERT INTO Informacion_Pruebas (serial_probeta, nombre_material, Rp_traccion, Rp_dureza, Rp_hemocompatibilidad, Rp_inflamabilidad, Rp_densidad, RT_fusion, fecha_realizacion, codigo_responsable) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores_mysql = (serial_probeta, nombre_material, resultado_traccion, resultado_dureza,
                             resultado_hemocompatibilidad, resultado_inflamabilidad, densidad,
                             temperatura_fusion, fecha_realizacion, codigo_responsable)
            cursor_mysql.execute(consulta_mysql, valores_mysql)
            conexion_mysql.commit()
            print(
                Fore.CYAN + "'\nLos datos de la prueba han sido agregados en MySQL." + Style.RESET_ALL)

        # Insertar en MongoDB si el responsable existe
        if responsable_mongo:
            prueba_mongo = {
                "serial_probeta": serial_probeta,
                "nombre_material": nombre_material,
                "Rp_traccion": resultado_traccion,
                "Rp_dureza": resultado_dureza,
                "Rp_hemocompatibilidad": resultado_hemocompatibilidad,
                "Rp_inflamabilidad": resultado_inflamabilidad,
                "Rp_densidad": densidad,
                "RT_fusion": temperatura_fusion,
                "fecha_realizacion": fecha_realizacion,
                "codigo_responsable": codigo_responsable
            }
            coleccion_pruebas.insert_one(prueba_mongo)
            print(
                Fore.CYAN + "\nLos datos de la prueba han sido agregados en MongoDB." + Style.RESET_ALL)

        # Mensaje si no se encontró el responsable en ninguna base de datos
        if not responsable_mysql and not responsable_mongo:
            print(Fore.CYAN + "\nNo existe un responsable con el código ingresado en ninguna base de datos. No se agregaron datos de la prueba." + Style.RESET_ALL)

        # Cerrar conexiones
        cursor_mysql.close()
        conexion_mysql.close()
        cliente.close()

        # Preguntar si se desea agregar otra prueba
        continuar = input("\n¿Desea agregar otra prueba? (Si/No): ").lower()
        if continuar != "si":
            break

def actualizar_resultados_pruebas(numero_serie):
    """
    Actualiza los resultados de una prueba en las bases de datos MySQL y MongoDB.

    Args:
        numero_serie (str): El número de serie de la prueba que se va a actualizar.

    Returns:
        None
    """
    while True:
        # Conexión a MySQL
        conexion_mysql = pymysql.connect(
            host='localhost',
            user='root',
            password='info2024',
            db='Responsables_Pruebas'
        )

        cursor_mysql = conexion_mysql.cursor()

        # Consulta para obtener la información de la prueba en MySQL
        consulta_mysql = f"SELECT * FROM Informacion_Pruebas WHERE serial_probeta = '{numero_serie}'"
        cursor_mysql.execute(consulta_mysql)
        resultados_mysql = cursor_mysql.fetchone()

        # Conexión a MongoDB
        cliente = pymongo.MongoClient("localhost", 27017)
        base_datos = cliente["Responsables_Pruebas_M"]
        coleccion_pruebas = base_datos["informacion_pruebas"]

        # Consulta para obtener la información de la prueba en MongoDB
        resultados_mongo = coleccion_pruebas.find_one({"serial_probeta": numero_serie})

        # Verificar si la probeta está presente en ambas bases de datos
        if resultados_mysql and resultados_mongo:
            print(Fore.CYAN +"La probeta está presente en ambas bases de datos."+ Style.RESET_ALL)
        elif resultados_mysql:
            print(Fore.CYAN +"La probeta solo está presente en MySQL."+ Style.RESET_ALL)
        elif resultados_mongo:
            print(Fore.CYAN + "La probeta solo está presente en MongoDB." + Style.RESET_ALL)
        else:
            print(Fore.RED + "No se encontró ninguna prueba con el número de serie especificado." + Style.RESET_ALL)
            break
        
        # Solicitar los nuevos valores al usuario
        print("=" * 40)
        serial_probeta = input(
            "\nIngrese el NUEVO serial de la probeta que quiere actualizar: ")
        nombre_material = input("Ingrese el NUEVO nombre del material: ")
        resultado_traccion = input(
            "Ingrese el NUEVO resultado de ensayo de tracción (deformación) en MPa: ") + " MPa"
        resultado_dureza = input(
            "Ingrese el NUEVO resultado de la prueba de dureza en HB: ") + " HB"
        resultado_hemocompatibilidad = input(
            "¿La prueba de hemocompatibilidad fue exitosa? (Sí/No): ").lower()
        resultado_inflamabilidad = input(
            "¿La prueba de inflamabilidad fue exitosa? (Sí/No): ").lower()
        densidad = input("Ingrese el NUEVO resultado de densidad en g/cm³: ") + " g/cm³"
        temperatura_fusion = input(
            "Ingrese el NUEVO resultado de temperatura de fusión en °C: ") + " °C"
        fecha_realizacion = datetime.datetime.now().strftime("%Y-%m-%d")
        codigo_responsable = input("Ingrese el NUEVO código del responsable: ")

        # Validar los tipos de datos
        if not all(x.replace('.', '', 1).isdigit() for x in [resultado_traccion.split()[0], resultado_dureza.split()[0], densidad.split()[0], temperatura_fusion.split()[0]]):
            print(Fore.RED + "Los resultados de tracción, dureza, densidad y temperatura de fusión deben ser valores numéricos." + Style.RESET_ALL)
            continue

        if resultado_hemocompatibilidad not in ['si', 'no'] or resultado_inflamabilidad not in ['si', 'no']:
            print(Fore.RED + "ERROR! Los resultados de hemocompatibilidad e inflamabilidad deben ser 'Sí' o 'No'." + Style.RESET_ALL)
            continue

        # Actualizar la información en MySQL si existe
        if resultados_mysql:
            # Actualizar la información en MySQL
            consulta_actualizar_mysql = f"UPDATE Informacion_Pruebas SET serial_probeta = '{serial_probeta}', nombre_material = '{nombre_material}', Rp_traccion = '{resultado_traccion}', Rp_dureza = '{resultado_dureza}', Rp_hemocompatibilidad = '{
                resultado_hemocompatibilidad}', Rp_inflamabilidad = '{resultado_inflamabilidad}', Rp_densidad = '{densidad}', RT_fusion = '{temperatura_fusion}', fecha_realizacion = '{fecha_realizacion}', codigo_responsable = {codigo_responsable} WHERE serial_probeta = '{numero_serie}'"
            cursor_mysql.execute(consulta_actualizar_mysql)
            conexion_mysql.commit()
            print(
                Fore.CYAN + "La información de la prueba ha sido actualizada en MySQL." + Style.RESET_ALL)

        # Actualizar la información en MongoDB si existe
        if resultados_mongo:
            # Actualizar la información en MongoDB
            nuevo_valor = {
                "$set": {
                    "serial_probeta": serial_probeta,
                    "nombre_material": nombre_material,
                    "Rp_traccion": resultado_traccion,
                    "Rp_dureza": resultado_dureza,
                    "Rp_hemocompatibilidad": resultado_hemocompatibilidad,
                    "Rp_inflamabilidad": resultado_inflamabilidad,
                    "Rp_densidad": densidad,
                    "RT_fusion": temperatura_fusion,
                    "fecha_realizacion": fecha_realizacion,
                    "codigo_responsable": int(codigo_responsable)
                }
            }
            coleccion_pruebas.update_one({"serial_probeta": numero_serie}, nuevo_valor)
            print(
                Fore.CYAN + "La información de la prueba ha sido actualizada en MongoDB." + Style.RESET_ALL)

        # Cerrar conexiones
        cursor_mysql.close()
        conexion_mysql.close()
        cliente.close()
        break
               
def importar_resultados_prueba_mysql():
    """
    Importa los resultados de las pruebas desde un archivo JSON a una base de datos MySQL.

    Se espera que el archivo JSON tenga el siguiente formato:
    [
        {
            "serial_probeta": "valor",
            "nombre_material": "valor",
            "Rp_traccion": valor,
            "Rp_dureza": valor,
            "Rp_hemocompatibilidad": "valor",
            "Rp_inflamabilidad": "valor",
            "Rp_densidad": valor,
            "RT_fusion": valor,
            "fecha_realizacion": "valor",
            "codigo_responsable": valor
        },
        ...
    ]

    Returns:
        None
    """
    try:
        # Conexión a la base de datos MySQL
        conexion = pymysql.connect(
            host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
        cursor = conexion.cursor()

        # Leer el archivo JSON
        with open('informacion_pruebas.json', 'r') as file:
            datos_pruebas = json.load(file)

        # Insertar los datos en la tabla de MySQL
        for prueba in datos_pruebas:
            sql = "INSERT INTO Informacion_Pruebas (serial_probeta, nombre_material, Rp_traccion, Rp_dureza, Rp_hemocompatibilidad, Rp_inflamabilidad, Rp_densidad, RT_fusion, fecha_realizacion, codigo_responsable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (
                prueba['serial_probeta'],
                prueba['nombre_material'],
                prueba['Rp_traccion'],
                prueba['Rp_dureza'],
                prueba['Rp_hemocompatibilidad'],
                prueba['Rp_inflamabilidad'],
                prueba['Rp_densidad'],
                prueba['RT_fusion'],
                prueba['fecha_realizacion'],
                prueba['codigo_responsable']
            )
            cursor.execute(sql, valores)

        # Confirmar cambios y cerrar conexión
        conexion.commit()
        conexion.close()
        print(Fore.CYAN + "Datos de pruebas importados a MySQL correctamente." + Style.RESET_ALL)

    except Exception as e:
        print(
            Fore.RED + f"Error al importar datos de pruebas a MySQL: {e}" + Style.RESET_ALL)


def importar_resultados_prueba_mongo():
    """
    Importa los resultados de las pruebas desde un archivo JSON a una colección en MongoDB.

    Se espera que el archivo JSON tenga el siguiente formato:
    [
        {
            "serial_probeta": "valor",
            "nombre_material": "valor",
            "Rp_traccion": valor,
            "Rp_dureza": valor,
            "Rp_hemocompatibilidad": "valor",
            "Rp_inflamabilidad": "valor",
            "Rp_densidad": valor,
            "RT_fusion": valor,
            "fecha_realizacion": "valor",
            "codigo_responsable": valor
        },
        ...
    ]

    Returns:
        None
    """
    try:
        # Conexión a MongoDB
        cliente = MongoClient("localhost", 27017)
        db = cliente["Responsables_Pruebas_M"]
        coleccion = db["informacion_pruebas"]

        # Leer el archivo JSON
        with open('informacion_pruebas.json', 'r') as file:
            datos_pruebas = json.load(file)

        # Insertar los datos en la colección de MongoDB
        coleccion.insert_many(datos_pruebas)

        print("Datos de pruebas importados a MongoDB correctamente.")
    except Exception as e:
        print(f"Error al importar datos de pruebas a MongoDB: {e}")


def importar_resultados_prueba(nombre_archivo):
    """
    Importa los resultados de las pruebas desde un archivo JSON a las bases de datos MySQL y MongoDB.

    Args:
        nombre_archivo (str): El nombre del archivo JSON que contiene los datos de las pruebas.

    Returns:
        None
    """
    try:
        # Conexión a la base de datos MySQL
        conexion_mysql = pymysql.connect(
            host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
        cursor_mysql = conexion_mysql.cursor()

        # Conexión a MongoDB
        cliente_mongo = MongoClient("localhost", 27017)
        db = cliente_mongo["Responsables_Pruebas_M"]
        coleccion = db["informacion_pruebas"]

        # Leer el archivo JSON
        nombre_archivo += ".json"
        with open(nombre_archivo, 'r') as file:
            datos_pruebas = json.load(file)

        # Insertar los datos en MySQL y MongoDB
        for prueba in datos_pruebas:
            # MySQL
            sql_mysql = "INSERT INTO Informacion_Pruebas (serial_probeta, nombre_material, Rp_traccion, Rp_dureza, Rp_hemocompatibilidad, Rp_inflamabilidad, Rp_densidad, RT_fusion, fecha_realizacion, codigo_responsable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores_mysql = (
                prueba['serial_probeta'],
                prueba['nombre_material'],
                prueba['Rp_traccion'],
                prueba['Rp_dureza'],
                prueba['Rp_hemocompatibilidad'],
                prueba['Rp_inflamabilidad'],
                prueba['Rp_densidad'],
                prueba['RT_fusion'],
                prueba['fecha_realizacion'],
                prueba['codigo_responsable']
            )
            cursor_mysql.execute(sql_mysql, valores_mysql)

            # MongoDB
            coleccion.insert_one(prueba)

        # Confirmar cambios y cerrar conexiones
        conexion_mysql.commit()
        conexion_mysql.close()
        cliente_mongo.close()

        print(Fore.CYAN + "Datos de pruebas importados correctamente." + Style.RESET_ALL)
    except Exception as e:
        print(
            Fore.RED + f"Error al importar datos de pruebas: {e}" + Style.RESET_ALL)


def ver_informacion_prueba(serial_probeta):
    """
    Muestra la información de una prueba específica identificada por su serial de probeta tanto desde MySQL como desde MongoDB.

    Args:
        serial_probeta (str): El serial de la probeta de la prueba que se desea visualizar.

    Returns:
        None
    """
    try:
        # Conexión a la base de datos MySQL
        conexion_mysql, cursor_mysql = conectar_mysql()

        # Conexión a MongoDB
        cliente = pymongo.MongoClient("localhost", 27017)
        base_datos = cliente["Responsables_Pruebas_M"]
        coleccion = base_datos["informacion_pruebas"]

        # Buscar la información en MySQL
        consulta_mysql = "SELECT * FROM Informacion_Pruebas WHERE serial_probeta = %s"
        cursor_mysql.execute(consulta_mysql, (serial_probeta,))
        resultado_mysql = cursor_mysql.fetchone()

        # Buscar la información en MongoDB
        resultado_mongo = coleccion.find_one(
            {"serial_probeta": serial_probeta})

        # Mostrar resultados
        if resultado_mysql:
            columnas_mysql = [column[0] for column in cursor_mysql.description]
            resultado_mysql = dict(zip(columnas_mysql, resultado_mysql))

            print(Fore.CYAN + "\n Información de la prueba en MySQL:" + Style.RESET_ALL)
            print(f"Serial de la probeta: {resultado_mysql['serial_probeta']}")
            print(f"Nombre del material: {resultado_mysql['nombre_material']}")
            print(f"Resultado de ensayo de tracción: {
                  resultado_mysql['Rp_traccion']}")
            print(f"Resultado de prueba de dureza: {
                  resultado_mysql['Rp_dureza']}")
            print(f"Resultado de prueba de hemocompatibilidad: {
                  resultado_mysql['Rp_hemocompatibilidad']}")
            print(f"Resultado de prueba de inflamabilidad: {
                  resultado_mysql['Rp_inflamabilidad']}")
            print(f"Resultado de densidad: {resultado_mysql['Rp_densidad']}")
            print(f"Resultado de temperatura de fusión: {
                  resultado_mysql['RT_fusion']}")
            print(f"Fecha de realización: {
                  resultado_mysql['fecha_realizacion']}")
            print(f"Código del responsable: {
                  resultado_mysql['codigo_responsable']}")
        else:
            print(
                Fore.CYAN + "\nNo se encontró información de la prueba en MySQL." + Style.RESET_ALL)

        if resultado_mongo:
            print(Fore.CYAN + "\nInformación de la prueba en MongoDB:" + Style.RESET_ALL)
            print(f"Serial de la probeta: {resultado_mongo['serial_probeta']}")
            print(f"Nombre del material: {resultado_mongo['nombre_material']}")
            print(f"Resultado de ensayo de tracción: {
                  resultado_mongo['Rp_traccion']}")
            print(f"Resultado de prueba de dureza: {
                  resultado_mongo['Rp_dureza']}")
            print(f"Resultado de prueba de hemocompatibilidad: {
                  resultado_mongo['Rp_hemocompatibilidad']}")
            print(f"Resultado de prueba de inflamabilidad: {
                  resultado_mongo['Rp_inflamabilidad']}")
            print(f"Resultado de densidad: {resultado_mongo['Rp_densidad']}")
            print(f"Resultado de temperatura de fusión: {
                  resultado_mongo['RT_fusion']}")
            print(f"Fecha de realización: {
                  resultado_mongo['fecha_realizacion']}")
            print(f"Código del responsable: {
                  resultado_mongo['codigo_responsable']}")
        else:
            print(
                Fore.CYAN + "\nNo se encontró información de la prueba en MongoDB." + Style.RESET_ALL)

        # Cerrar conexiones
        cursor_mysql.close()
        conexion_mysql.close()
        cliente.close()

    except Exception as e:
        print(
            Fore.RED + f"Error al visualizar información de la prueba: {e}" + Style.RESET_ALL)


def ver_todos_los_resultados():
    """
    Muestra todos los resultados de las pruebas almacenadas en las bases de datos MySQL y MongoDB.

    Args:
        None

    Returns:
        None
    """
    try:
        # Conexión a la base de datos MySQL
        conexion_mysql, cursor_mysql = conectar_mysql()

        # Conexión a MongoDB
        cliente = pymongo.MongoClient("localhost", 27017)
        base_datos = cliente["Responsables_Pruebas_M"]
        coleccion = base_datos["informacion_pruebas"]

        # Obtener todos los resultados de las pruebas en MySQL
        consulta_mysql = "SELECT serial_probeta, fecha_realizacion FROM Informacion_Pruebas ORDER BY serial_probeta"
        cursor_mysql.execute(consulta_mysql)
        columnas_mysql = [column[0] for column in cursor_mysql.description]
        resultados_mysql = [dict(zip(columnas_mysql, fila))
                            for fila in cursor_mysql.fetchall()]

        # Obtener todos los resultados de las pruebas en MongoDB
        resultados_mongo = list(coleccion.find(
            {}, {"serial_probeta": 1, "fecha_realizacion": 1}).sort("serial_probeta"))

        # Mostrar resultados de MySQL
        print(Fore.CYAN + "Resultados de pruebas en MySQL:" + Style.RESET_ALL)
        print(f"{'Serial de la Probeta':<10}{' / Fecha de Realización':<20}")
        print("="*40)
        for resultado in resultados_mysql:
            print(f"{resultado['serial_probeta']:<20}{
                  resultado['fecha_realizacion']:<20}")

        # Mostrar resultados de MongoDB
        print(Fore.CYAN + "\nResultados de pruebas en MongoDB:" + Style.RESET_ALL)
        print(f"{'Serial de la Probeta':<10}{' / Fecha de Realización':<20}")
        print("="*40)
        for resultado in resultados_mongo:
            print(f"{resultado['serial_probeta']:<20}{
                  resultado['fecha_realizacion']:<20}")

    except Exception as e:
        print(
            Fore.RED + f"Error al mostrar todos los resultados de las pruebas: {e}" + Style.RESET_ALL)

    # Cerrar conexiones
    if cursor_mysql:
        cursor_mysql.close()
    if conexion_mysql:
        conexion_mysql.close()
    if cliente:
        cliente.close()


def eliminar_resultado_prueba(serial_probeta):
    """
    Elimina el resultado de la prueba identificado por el serial de la probeta tanto de la base de datos MySQL como de MongoDB.

    Args:
        serial_probeta (str): El serial de la probeta del resultado de la prueba que se desea eliminar.

    Returns:
        None
    """
    try:
        # Conexión a la base de datos MySQL
        conexion_mysql, cursor_mysql = conectar_mysql()

        # Conexión a MongoDB
        cliente = pymongo.MongoClient("localhost", 27017)
        base_datos = cliente["Responsables_Pruebas_M"]
        coleccion = base_datos["informacion_pruebas"]

        # Eliminar resultado en MySQL
        consulta_eliminar_mysql = "DELETE FROM Informacion_Pruebas WHERE serial_probeta = %s"
        cursor_mysql.execute(consulta_eliminar_mysql, (serial_probeta,))
        filas_afectadas_mysql = cursor_mysql.rowcount

        if filas_afectadas_mysql > 0:
            print(Fore.CYAN + f"El resultado de la prueba con serial {
                  serial_probeta} ha sido eliminado en MySQL." + Style.RESET_ALL)
        else:
            print(Fore.CYAN + f"No se encontró ningún resultado de prueba con serial {
                  serial_probeta} en MySQL." + Style.RESET_ALL)

        # Eliminar resultado en MongoDB
        resultado_eliminar_mongo = coleccion.delete_one(
            {"serial_probeta": serial_probeta})

        if resultado_eliminar_mongo.deleted_count > 0:
            print(Fore.CYAN + f"El resultado de la prueba con serial {
                  serial_probeta} ha sido eliminado en MongoDB." + Style.RESET_ALL)
        else:
            print(Fore.CYAN + f"No se encontró ningún resultado de prueba con serial {
                  serial_probeta} en MongoDB." + Style.RESET_ALL)

    except Exception as e:
        print(
            Fore.RED + f"Error al eliminar el resultado de la prueba: {e}" + Style.RESET_ALL)

    # Cerrar conexiones
    if cursor_mysql:
        cursor_mysql.close()
    if conexion_mysql:
        conexion_mysql.commit()
        conexion_mysql.close()
    if cliente:
        cliente.close()
