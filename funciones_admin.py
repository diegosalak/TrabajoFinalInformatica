import xml.etree.ElementTree as ET
import os
import pymysql
from pymongo import MongoClient
import json
import pymongo
from colorama import init, Fore, Style
import datetime
import re

init()


def es_numero(nueva_clave):
    """
    Comprueba si una cadena es un número entero.

    Args:
        nueva_clave (str): La cadena a comprobar.

    Returns:
        Union[str, bool]: Devuelve la cadena si es un número entero, de lo contrario, devuelve False.
    """
    try:
        int(nueva_clave)
        return nueva_clave
    except ValueError:
        return False


def nueve_cifras(x):
    """
    Verifica si una cadena es un número de 9 dígitos.

    Args:
        x (str): La cadena a comprobar.

    Returns:
        int: El número de 9 dígitos si es válido.

    Raises:
        ValueError: Si la cadena no es un número de 9 dígitos.
    """
    while True:
        if not x.isdigit() or len(x) != 9:
            print(Fore.RED + "ERROR! El número de documento debe ser numérico y tener exactamente 9 dígitos." + Style.RESET_ALL)
            x = input(
                "Ingrese el número de documento de identidad nuevamente \n ->  ")
            continue
        else:
            x = int(x)
            break
    return x


def crear_usuarios(clave_nuevo_admin, nombre_nuevo_admin, id_nuevo_admin):
    """
    Crea un diccionario de usuario con los detalles proporcionados.

    Args:
        clave_nuevo_admin (str): La contraseña del nuevo administrador.
        nombre_nuevo_admin (str): El nombre del nuevo administrador.
        id_nuevo_admin (int): El número de documento de identidad del nuevo administrador.

    Returns:
        list: Lista que contiene el diccionario de usuario creado.

    """

    usuarios = []
    diccionario_usuarios = {}
    diccionario_usuarios["contraseña"] = clave_nuevo_admin
    diccionario_usuarios["nombre"] = nombre_nuevo_admin
    diccionario_usuarios["documento_I"] = id_nuevo_admin
    usuarios.append(diccionario_usuarios)
    return usuarios


def crear_admin(usuarios):
    """
    Crea nuevos administradores y los agrega al archivo XML.

    Args:
        usuarios (list): Lista de diccionarios de usuarios a crear.

    Returns:
        None
    """
    ruta_archivo_xml = os.path.join("admin", "user.xml")
    # Parsear el archivo XML existente
    arbol = ET.parse(ruta_archivo_xml)
    raiz = arbol.getroot()
    # Crear un nuevo lemento "usuario"
    for usuario in usuarios:
        nuevo_usuario = ET.SubElement(
            raiz, "usuario", documento_I=str(usuario["documento_I"]))
        nombre = ET.SubElement(nuevo_usuario, "nombre")
        nombre.text = usuario["nombre"]
        clave = ET.SubElement(nuevo_usuario, "contraseña")
        clave.text = usuario["contraseña"]
    ET.indent(arbol)

    # Escribir la estructura XML actualizada de vuelta al archivo
    arbol.write(ruta_archivo_xml, encoding="utf-8", xml_declaration=True, )
    print(Fore.CYAN + "\nUsuarios añadidos correctamente. \n" + Style.RESET_ALL)


def buscar_usuario_por_clave(id_busqueda):
    """
    Busca un usuario por su número de documento de identidad.

    Args:
        id_busqueda (str): El número de documento de identidad a buscar.

    Returns:
        Union[dict, bool]: Devuelve el diccionario de usuario si se encuentra, de lo contrario, devuelve False.
    """
    # Ruta del archivo XML
    ruta_archivo_xml = ruta_archivo_xml = os.path.join("admin", "user.xml")
    # Parsear el archivo XML existente
    arbol = ET.parse(ruta_archivo_xml)
    raiz = arbol.getroot()
    for usuario in raiz.findall("usuario"):
        id_usuario = usuario.get("documento_I")  # Obtener el atributo "id"
        if id_usuario == id_busqueda:
            clave_usuario = usuario.find("contraseña").text
            nombre_usuario = usuario.find("nombre").text
            diccionario_admin = {
                "documento_I": id_usuario,
                "nombre": nombre_usuario,
                "contraseña": clave_usuario
            }
            return diccionario_admin
    # Si no se encuentra el usuario, retornar False
    return False


def buscador_cedula(id_busqueda):
    """
    Busca un usuario por su número de documento de identidad.

    Args:
        id_busqueda (str): El número de documento de identidad a buscar.

    Returns:
        Union[bool, None]: Devuelve True si se encuentra el usuario, de lo contrario, devuelve None.
    """
    # Parsear el archivo XML
    ruta_archivo_xml = ruta_archivo_xml = os.path.join("admin", "user.xml")
    arbol = ET.parse(ruta_archivo_xml)
    raiz = arbol.getroot()
    # Buscar el usuario con el id especificado
    for usuario in raiz.findall("usuario"):
        if usuario.get("documento_I") == id_busqueda:
            nombre = usuario.find("nombre").text
            clave = usuario.find("contraseña").text
            return True
    # Si no se encuentra el usuario
    return None


def modificar_usuario_admin(id_busqueda, nuevo_nombre, nueva_clave):
    """
    Modifica los detalles de un usuario existente en el archivo XML.

    Args:
        id_busqueda (str): El número de documento de identidad del usuario a modificar.
        nuevo_nombre (str): El nuevo nombre del usuario.
        nueva_clave (str): La nueva contraseña del usuario.

    Returns:
        bool: True si se modifica el usuario correctamente, False si no se encuentra el usuario.
    """
    nuevo_documento = input(
        "Digite el nuevo documento del administrador. \n-> ")
    nuevo_documento = nueve_cifras(nuevo_documento)
    nuevo_documento = str(nuevo_documento)
    ruta_archivo_xml = os.path.join("admin", "user.xml")
    arbol = ET.parse(ruta_archivo_xml)
    raiz = arbol.getroot()

    # Buscar el usuario con el id especificado
    usuario_info = buscador_cedula(id_busqueda)
    if usuario_info:
        for usuario in raiz.findall("usuario"):
            if usuario.get("documento_I") == str(id_busqueda):
                if nuevo_nombre:
                    usuario.find("nombre").text = nuevo_nombre
                if nueva_clave:
                    usuario.find("contraseña").text = nueva_clave
                if nuevo_documento:
                    usuario.set("documento_I", nuevo_documento)
                # Guardar los cambios en el archivo XML
                ET.indent(arbol)
                arbol.write(ruta_archivo_xml, encoding="utf-8",
                            xml_declaration=True)
                print(
                    Fore.CYAN + f"Usuario con ID {id_busqueda} modificado correctamente." + Style.RESET_ALL)
                return True
    else:
        print(Fore.RED + "ERROR! NO se encontró ningún usuario con ID:" +
              str(id_busqueda) + Style.RESET_ALL)
        return False


def eliminar_admin(id_busqueda):
    """
    Elimina un usuario del archivo XML según su número de documento de identidad.

    Args:
        id_busqueda (str): El número de documento de identidad del usuario a eliminar.

    Returns:
        bool: True si se elimina el usuario correctamente, False si no se encuentra el usuario.
    """
    ruta_archivo_xml = os.path.join("admin", "user.xml")
    arbol = ET.parse(ruta_archivo_xml)
    raiz = arbol.getroot()

    # Buscar el usuario con el id especificado usando la función buscador_cedula
    usuario_info = buscador_cedula(id_busqueda)
    if usuario_info:
        # Si el usuario es encontrado, eliminarlo
        for usuario in raiz.findall("usuario"):
            if usuario.get("documento_I") == id_busqueda:
                raiz.remove(usuario)
                break
        # Escribir la estructura XML actualizada de vuelta al archivo
        ET.indent(arbol)
        arbol.write(ruta_archivo_xml, encoding="utf-8", xml_declaration=True)
        return True
    else:
        return False


def solicitar_informacion():
    """
    Solicita información del usuario (nombre, apellido, contraseña, documento de identidad y cargo) desde la entrada estándar.

    Returns:
        tuple: Una tupla que contiene la información del usuario en el orden siguiente: contraseña, apellido, nombre, documento_I, cargo.
    """
    def validar_alfabetico(cadena):
        return bool(re.match(r'^[a-zA-Z]+$', cadena))

    def validar_alfanumerico(cadena):
        return bool(re.match(r'^[a-zA-Z0-9]+$', cadena))

    while True:
        # Validar que el apellido y el nombre contengan solo caracteres alfabéticos
        nombre = input(
            "Ingrese el nombre del nuevo responsable. \n -> ").strip()
        if not validar_alfabetico(nombre.replace(" ", "")):
            print(
                Fore.RED + "ERROR! el nombre deben contener solo letras." + Style.RESET_ALL)
            continue
        # Validar que el apellido y el nombre contengan solo caracteres alfabéticos
        apellido = input(
            "Ingrese el apellido del nuevo responsable \n -> ").strip()
        if not validar_alfabetico(apellido.replace(" ", "")):
            print(
                Fore.RED + "ERROR! El apellido deben contener solo letras." + Style.RESET_ALL)
            continue
        # Validar que la contraseña contenga caracteres alfanuméricos
        contraseña = input(
            "Ingrese la contraseña del nuevo responsable. \n -> ").strip()
        if not validar_alfanumerico(contraseña):
            print(
                Fore.RED + "ERROR! La contraseña debe ser alfanumérica." + Style.RESET_ALL)
            continue
        documento_I = input(
            "Ingrese el documento de identidad del nuevo responsable. \n -> ").strip()
        # Validar que el documento de identidad sea un número de 9 cifras
        try:
            documento_I = es_numero(documento_I)
            documento_I = str(documento_I)
            documento_I = nueve_cifras(documento_I)
            documento_I = int(documento_I)
        except ValueError as e:
            print(e)
            continue

        cargo = input("Ingrese el cargo del nuevo responsable \n -> ").strip()

        if not validar_alfabetico(cargo.replace(" ", "")):
            print(
                Fore.RED + "ERROR! El cargo debe contener solo letras." + Style.RESET_ALL)
            continue

        # Validar que el cargo contenga solo caracteres alfabéticos

        # Si todas las validaciones pasan, retornar la información
        tupla_info = (contraseña, apellido, nombre, documento_I, cargo)
        print("="*40)
        return tupla_info


def insertar_informacion_MySQL(tupla_info):
    """
    Inserta la información del usuario en la base de datos MySQL.

    Args:
        tupla_info (tuple): Una tupla que contiene la información del usuario en el orden siguiente: contraseña, apellido, nombre, documento_I, cargo.
    """

    contraseña, apellido, nombre, documento_I, cargo = tupla_info

    # Conectarse a la base de datos MySQL
    conexion = pymysql.connect(host="localhost",
                               user="root",
                               password="info2024",
                               database="Responsables_Pruebas")

    # Crear un cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    consulta_mysql = "SELECT * FROM informacion_responsables WHERE documento_I = %s"
    cursor.execute(consulta_mysql, (documento_I,))
    responsable_mysql = cursor.fetchone()

    if not responsable_mysql:
        # Consulta SQL para insertar información en la tabla
        consulta = "INSERT INTO informacion_responsables (contraseña, apellido, nombre, documento_I, cargo) VALUES (%s, %s, %s, %s, %s)"

    # Ejecutar la consulta SQL con los valores proporcionados
        cursor.execute(consulta, (contraseña, apellido,
                                  nombre, documento_I, cargo))

    # Confirmar la transacción
        conexion.commit()
        print(Fore.CYAN + "Información insertada correctamente en la tabla de MySQL." + Style.RESET_ALL)
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conexion.close()
    else:
        print(Fore.RED + "\nYA SE ENCUENTRA UN RESPONSABLE CON ESE DOCUMENTO EN MYSQL" + Style.RESET_ALL)


def insertar_informacion_mongodb(tupla_info):
    """
    Inserta la información del usuario en la base de datos MongoDB.

    Args:
        tupla_info (tuple): Una tupla que contiene la información del usuario en el orden siguiente: contraseña, apellido, nombre, documento_I, cargo.
    """
    contraseña, apellido, nombre, documento_I, cargo = tupla_info

    # Conexión al cliente de MongoDB
    cliente = pymongo.MongoClient("localhost", 27017)
    # Acceso a la base de datos
    db = cliente["Responsables_Pruebas_M"]
    # Acceso a la colección
    coleccion = db["Informacion_Responsables_M"]
    responsable_mongo = coleccion.find_one({"documento_I": documento_I})
    if not responsable_mongo:
        # Obtener el último _id en MongoDB para determinar el siguiente
        ultimo_documento = list(coleccion.find().sort(
            "_id", pymongo.DESCENDING).limit(1))
        if len(ultimo_documento) > 0:
            ultimo_id = ultimo_documento[0]["_id"]
            nuevo_id = ultimo_id + 1
        else:
            nuevo_id = 1

        # Crear un diccionario con la información
        datos = {
            "_id": nuevo_id,
            "contraseña": contraseña,
            "apellido": apellido,
            "nombre": nombre,
            "documento_I": documento_I,
            "cargo": cargo
        }

        # Insertar el documento en la colección
        coleccion.insert_one(datos)

        print(Fore.CYAN + "Información insertada correctamente en la colección de MongoDB." + Style.RESET_ALL)

        # Cerrar la conexión al cliente de MongoDB
        cliente.close()
    else:
        print(Fore.RED + "\nYA SE ENCUENTRA UN RESPONSABLE CON ESE DOCUMENTO EN MONGO" + Style.RESET_ALL)


def ver_informacion(documento_I):
    """
    Muestra la información de un usuario según su número de documento de identidad, buscando en las bases de datos MySQL y MongoDB.

    Args:
        documento_I (str): El número de documento de identidad del usuario.
    """
    # Buscar en la base de datos MySQL
    conexion_mysql = pymysql.connect(
        host="localhost", user="root", password="info2024", database="Responsables_Pruebas")
    cursor_mysql = conexion_mysql.cursor()
    consulta_mysql = "SELECT * FROM informacion_responsables WHERE documento_I = %s"
    cursor_mysql.execute(consulta_mysql, (documento_I,))
    responsable_mysql = cursor_mysql.fetchone()
    cursor_mysql.close()
    conexion_mysql.close()

    if responsable_mysql:
        print(
            Fore.CYAN + "Información del responsable encontrado en MySQL:" + Style.RESET_ALL)
        print("="*80)
        columnas = [desc[0] for desc in cursor_mysql.description]
        for clave, valor in zip(columnas, responsable_mysql):
            print(f"{Fore.GREEN + clave.upper() + Style.RESET_ALL}: {valor}")
    else:
        print(
            Fore.RED + "\nERROR! No se encontró al responsable en MySQL." + Style.RESET_ALL)

    # Buscar en la base de datos MongoDB
    cliente_mongo = MongoClient("localhost", 27017)
    db_mongo = cliente_mongo["Responsables_Pruebas_M"]
    coleccion_mongo = db_mongo["Informacion_Responsables_M"]
    responsable_mongo = coleccion_mongo.find_one({"documento_I": documento_I})
    cliente_mongo.close()

    if responsable_mongo:
        print(Fore.CYAN + "\nInformación del responsable encontrado en MongoDB:" + Style.RESET_ALL)
        print("="*80)
        for clave, valor in responsable_mongo.items():
            print(f"{Fore.GREEN + clave.upper() + Style.RESET_ALL}: {valor}")
    else:
        print(Fore.RED + "\nNo se encontró al responsable en MongoDB." + Style.RESET_ALL)


def solicitar_informacion_nueva():
    """
    Solicita al usuario ingresar la nueva información de un responsable, incluyendo contraseña, apellido, nombre y cargo, y valida que cumplan con ciertos requisitos.

    Returns:
        dict: Un diccionario que contiene la nueva información del responsable, con las siguientes claves:
            - "contraseña": La nueva contraseña del responsable.
            - "apellido": El nuevo apellido del responsable.
            - "nombre": El nuevo nombre del responsable.
            - "cargo": El nuevo cargo del responsable.
    """
    def validar_alfabetico(cadena):
        """
        Valida que una cadena contenga solo caracteres alfabéticos y espacios.

        Args:
            cadena (str): La cadena a validar.

        Returns:
            bool: True si la cadena cumple con los requisitos, False de lo contrario.
        """
        return bool(re.match(r'^[a-zA-Z ]+$', cadena))

    def validar_alfanumerico(cadena):
        """
        Valida que una cadena contenga solo caracteres alfanuméricos.

        Args:
            cadena (str): La cadena a validar.

        Returns:
            bool: True si la cadena cumple con los requisitos, False de lo contrario.
        """
        return bool(re.match(r'^[a-zA-Z0-9]+$', cadena))

    while True:
        documento_I_nuevo = input(
            "Ingrese el nuevo documento de identidad. \n -> ").strip()
        contraseña = input("Ingrese la nueva contraseña. \n -> ").strip()
        apellido = input("Ingrese el nuevo apellido. \n -> ").strip()
        nombre = input("Ingrese el nuevo nombre. \n -> ").strip()
        cargo = input("Ingrese el nuevo cargo. \n -> ").strip()

        # Validar entradas

        if not validar_alfanumerico(contraseña):
            print(
                Fore.RED + "ERROR! La contraseña debe ser alfanumérica." + Style.RESET_ALL)
            continue

        # Validar que el apellido, nombre y cargo contengan solo caracteres alfabéticos y espacios
        if not validar_alfabetico(apellido):
            print(
                Fore.RED + "ERROR! El apellido debe contener solo letras y espacios." + Style.RESET_ALL)
            continue

        if not validar_alfabetico(nombre):
            print(
                Fore.RED + "ERROR! El nombre debe contener solo letras y espacios." + Style.RESET_ALL)
            continue

        if not validar_alfabetico(cargo):
            print(
                Fore.RED + "ERROR! El cargo debe contener solo letras y espacios." + Style.RESET_ALL)
            continue
        try:
            documento_I_nuevo = es_numero(documento_I_nuevo)
            documento_I_nuevo = str(documento_I_nuevo)
            documento_I_nuevo = nueve_cifras(documento_I_nuevo)
            documento_I_nuevo = int(documento_I_nuevo)
        except ValueError as e:
            print(e)
            continue
        # Si todas las validaciones pasan, retornar la información
        diccionario_info = {
            "documento_I_nuevo": int(documento_I_nuevo),
            "contraseña": contraseña,
            "apellido": apellido,
            "nombre": nombre,
            "cargo": cargo
        }

        return diccionario_info


def actualizar_informacion(diccionario_info):
    """
    Actualiza la información de un responsable en las bases de datos MySQL y MongoDB, si existe en alguna de ellas.

    Args:
        diccionario_info (dict): Un diccionario que contiene la nueva información del responsable, con las siguientes claves:
            - "contraseña": La nueva contraseña del responsable.
            - "apellido": El nuevo apellido del responsable.
            - "nombre": El nuevo nombre del responsable.
            - "cargo": El nuevo cargo del responsable.
    """
    while True:
        print("=" * 40)
        documento_I_buscar = input(
            "Ingrese el número de documento de identidad del responsable a actualizar \n -> ")
        print("="*40)
        if not documento_I_buscar.isdigit() or len(documento_I_buscar) != 9:
            print(Fore.RED + "ERROR! El número de documento debe ser numérico y tener exactamente 9 dígitos." + Style.RESET_ALL)
            continue
        else:
            break

    documento_I_buscar = int(documento_I_buscar)  # Convertir a entero

    # Conexión a MySQL
    conexion_mysql = pymysql.connect(
        host="localhost", user="root", password="info2024", database="Responsables_Pruebas")
    cursor_mysql = conexion_mysql.cursor()

    # Consulta MySQL para verificar si el documento existe
    consulta_mysql = "SELECT * FROM informacion_responsables WHERE documento_I = %s"
    cursor_mysql.execute(consulta_mysql, (documento_I_buscar,))
    responsable_mysql = cursor_mysql.fetchone()

    # Conexión a MongoDB
    cliente_mongo = MongoClient("localhost", 27017)
    db_mongo = cliente_mongo["Responsables_Pruebas_M"]
    coleccion_mongo = db_mongo["Informacion_Responsables_M"]

    # Actualizar en MongoDB si el responsable existe allí
    responsable_mongo = coleccion_mongo.find_one(
        {"documento_I": documento_I_buscar})

    if responsable_mysql or responsable_mongo:
        try:
            valor_eliminado = diccionario_info.pop("documento_I_nuevo")
            diccionario_info["documento_I"] = valor_eliminado

            # Actualizar en MongoDB
            if responsable_mongo:
                # Crear un nuevo diccionario sin la clave "documento_I_nuevo"
                diccionario_info_mongo = diccionario_info.copy()
                del diccionario_info_mongo["documento_I"]

                resultado_mongo = coleccion_mongo.update_one(
                    {"documento_I": documento_I_buscar}, {"$set": diccionario_info_mongo})
                if resultado_mongo.matched_count > 0:
                    print(
                        Fore.CYAN + "Información actualizada correctamente en MongoDB." + Style.RESET_ALL)
                else:
                    print(
                        Fore.RED + "No se encontró al responsable con ese documento en MongoDB." + Style.RESET_ALL)

            # Actualizar en MySQL
            if responsable_mysql:
                consulta_mysql_actualizar = """
                    UPDATE informacion_responsables
                    SET contraseña = %s, apellido = %s, nombre = %s, cargo = %s, documento_I = %s
                    WHERE documento_I = %s
                """
                cursor_mysql.execute(consulta_mysql_actualizar, (
                    diccionario_info["contraseña"], diccionario_info["apellido"],
                    diccionario_info["nombre"], diccionario_info["cargo"],
                    diccionario_info["documento_I"], documento_I_buscar))
                conexion_mysql.commit()
                print(
                    Fore.CYAN + "Información actualizada correctamente en MySQL." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Error al actualizar la información en ambas bases de datos:",
                  e, Style.RESET_ALL)

    # Si el responsable no está en ninguna base de datos, imprimir un mensaje de error
    if not (responsable_mysql or responsable_mongo):
        print(Fore.RED + "No se encontró al responsable con ese documento en ninguna base de datos." + Style.RESET_ALL)

    # Cerrar conexiones
    cursor_mysql.close()
    conexion_mysql.close()
    cliente_mongo.close()


def obtener_resultados_pruebas(documento_I):
    # Conexión a la base de datos MySQL
    conexion = pymysql.connect(
        host='localhost',
        user='root',
        password='info2024',
        db='Responsables_Pruebas'
    )

    with conexion.cursor() as cursor:
        # Consulta para obtener la información del responsable
        sql_responsable = """
            SELECT nombre, apellido, documento_I, cargo
            FROM Informacion_Responsables
            WHERE documento_I = %s
            """
        cursor.execute(sql_responsable, (documento_I,))
        responsable_info = cursor.fetchone()

        if responsable_info:
            print(Fore.CYAN + "Información del Responsable en MySQL:" + Style.RESET_ALL)
            print(f"Nombre: {responsable_info[0]} {responsable_info[1]}")
            print(f"Documento: {responsable_info[2]}")
            print(f"Cargo: {responsable_info[3]}")
            print("=" * 40)

            # Consulta para obtener los resultados de pruebas asociados al responsable
            sql_pruebas = """
                SELECT serial_probeta, nombre_material, Rp_traccion, Rp_dureza, Rp_hemocompatibilidad, Rp_inflamabilidad, Rp_densidad, RT_fusion, fecha_realizacion
                FROM Informacion_Pruebas
                WHERE codigo_responsable IN (SELECT codigo_responsable FROM Informacion_Responsables WHERE documento_I = %s)
                """
            cursor.execute(sql_pruebas, (documento_I,))
            resultados = cursor.fetchall()

            if resultados:
                print(Fore.CYAN + "Resultados de Pruebas en MySQL:" + Style.RESET_ALL)
                for resultado in resultados:
                    print("Serial Probeta:", resultado[0])
                    print("Nombre Material:", resultado[1])
                    print("Resultado Tracción:", resultado[2])
                    print("Resultado Dureza:", resultado[3])
                    print("Resultado Hemocompatibilidad:", resultado[4])
                    print("Resultado Inflamabilidad:", resultado[5])
                    print("Resultado Densidad:", resultado[6])
                    print("Resultado Fusión:", resultado[7])
                    print("Fecha Realización:", resultado[8])
                    print("=" * 40)
            else:
                print(
                    Fore.YELLOW + "No se encontraron resultados de pruebas asociados a este responsable en MySQL." + Style.RESET_ALL)
        else:
            print(Fore.RED + "NO se encontró ningún responsable con ese documento en la base MySQL." + Style.RESET_ALL)

    # Cerrar la conexión
    conexion.close()


def cargar_json_a_mongodb(uri="mongodb://localhost:27017/"):
    """
    Carga los datos desde un archivo JSON a una colección en MongoDB.

    Args:
        uri (str): URI de conexión a la instancia de MongoDB. Por defecto, se conecta a "localhost:27017".

    """
    # Conectar a MongoDB
    cliente = pymongo.MongoClient(uri)
    base_datos = cliente["Responsables_Pruebas_M"]
    coleccion = base_datos["informacion_pruebas"]

    # Leer el archivo JSON
    archivo_json = "informacion_pruebas.json"
    with open(archivo_json, 'r') as archivo:
        datos = json.load(archivo)

    # Insertar datos en la colección
    if isinstance(datos, list):
        coleccion.insert_many(datos)
    else:
        coleccion.insert_one(datos)

    print(Fore.CYAN + "Datos cargados en la base de datos Responsables_Pruebas_M, colección informacion_pruebas" + Style.RESET_ALL)

    # Cerrar la conexión
    cliente.close()


def buscar_responsable_y_resultados_por_documento(documento_I, uri="mongodb://localhost:27017/"):
    """
    Busca un responsable por su número de documento de identidad en MongoDB y muestra sus resultados de pruebas asociados.

    Args:
        documento_I (int): Número de documento de identidad del responsable.
        uri (str): URI de conexión a la instancia de MongoDB. Por defecto, se conecta a "localhost:27017".

    """
    # Conectar a MongoDB
    cliente = pymongo.MongoClient(uri)
    base_datos = cliente["Responsables_Pruebas_M"]

    # Colecciones
    coleccion_responsables = base_datos["Informacion_Responsables_M"]
    coleccion_pruebas = base_datos["informacion_pruebas"]

    # Buscar al responsable por documento_I
    responsable = coleccion_responsables.find_one({"documento_I": documento_I})

    if responsable:
        # Si se encuentra al responsable, buscar los resultados de las pruebas asociadas
        resultados_pruebas = list(coleccion_pruebas.find(
            {"codigo_responsable": responsable["_id"]}))

        # Mostrar información del responsable
        print("="*40)
        print(Fore.CYAN + "Información del Responsable en MONGODB:" + Style.RESET_ALL)
        print(f"Nombre: {responsable['nombre']} {responsable['apellido']}")
        print(f"Documento: {responsable['documento_I']}")
        print(f"Cargo: {responsable['cargo']}")

        if resultados_pruebas:
            # Mostrar resultados de las pruebas asociadas al responsable
            print(Fore.CYAN + "\nResultados de Pruebas en MONGODB:" + Style.RESET_ALL)
            for resultado in resultados_pruebas:
                print("Serial Probeta:", resultado.get("serial_probeta", "N/A"))
                print("Nombre Material:", resultado.get(
                    "nombre_material", "N/A"))
                print("Resultado Tracción:", resultado.get("Rp_traccion", "N/A"))
                print("Resultado Dureza:", resultado.get("Rp_dureza", "N/A"))
                print("Resultado Hemocompatibilidad:",
                      resultado.get("Rp_hemocompatibilidad", "N/A"))
                print("Resultado Inflamabilidad:",
                      resultado.get("Rp_inflamabilidad", "N/A"))
                print("Resultado Densidad:", resultado.get("Rp_densidad", "N/A"))
                print("Resultado Fusión:", resultado.get("RT_fusion", "N/A"))
                print("Fecha Realización:", resultado.get(
                    "fecha_realizacion", "N/A"))
                print("="*40)
        else:
            print(Fore.YELLOW + "No se encontraron resultados de pruebas asociados a este responsable." + Style.RESET_ALL)
    else:
        print(Fore.RED + "NO se encontró ningún responsable con ese documento en la base MongoDB." + Style.RESET_ALL)

    # Cerrar la conexión
    cliente.close()


def obtener_materiales_responsables(uri_mongo="mongodb://localhost:27017/"):
    """
    Obtiene los materiales estudiados junto con los nombres de los responsables y las fechas de realización, tanto de MySQL como de MongoDB.

    Args:
        uri_mongo (str): URI de conexión a la instancia de MongoDB. Por defecto, se conecta a "mongodb://localhost:27017/".

    Returns:
        list: Una lista de tuplas que contienen el nombre del material, la fecha de realización y el nombre del responsable.
    """
    # Lista para almacenar los materiales estudiados con los nombres de los responsables y las fechas de realización
    materiales_y_responsables = []

    # Conexión a MySQL y consulta de los materiales estudiados con los nombres de los responsables
    conexion_mysql = pymysql.connect(
        host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
    cursor_mysql = conexion_mysql.cursor()
    query_mysql = """
        SELECT IP.nombre_material, IR.nombre, IP.fecha_realizacion
        FROM Informacion_Pruebas IP
        INNER JOIN Informacion_Responsables IR ON IP.codigo_responsable = IR.codigo_responsable
    """
    cursor_mysql.execute(query_mysql)
    resultados_mysql = cursor_mysql.fetchall()

    # Agregar los materiales estudiados con los nombres de los responsables y las fechas de realización de MySQL a la lista
    for material, responsable, fecha_realizacion in resultados_mysql:
        if isinstance(fecha_realizacion, datetime.date):
            fecha_formateada = fecha_realizacion.strftime("%d/%m/%Y")
        else:
            fecha_formateada = fecha_realizacion
        materiales_y_responsables.append(
            (material, fecha_formateada, responsable))

    # Cerrar conexión MySQL
    cursor_mysql.close()
    conexion_mysql.close()

    # Conexión a MongoDB
    cliente_mongo = pymongo.MongoClient(uri_mongo)
    base_datos_mongo = cliente_mongo["Responsables_Pruebas_M"]
    coleccion_pruebas = base_datos_mongo["informacion_pruebas"]
    coleccion_responsables = base_datos_mongo["Informacion_Responsables_M"]

    # Consulta de materiales en MongoDB
    resultados_mongo = coleccion_pruebas.aggregate([
        {"$lookup": {
            "from": "Informacion_Responsables_M",
            "localField": "codigo_responsable",
            "foreignField": "_id",
            "as": "responsable"
        }},
        {"$unwind": "$responsable"},
        {"$project": {
            "_id": 0,
            "nombre_material": 1,
            "nombre_responsable": "$responsable.nombre",
            "fecha_realizacion": 1
        }}
    ])

    # Agregar los materiales estudiados con los nombres de los responsables y las fechas de realización de MongoDB a la lista
    for documento in resultados_mongo:
        fecha_realizacion = documento.get("fecha_realizacion", "")
        # Intentar convertir la fecha a un objeto datetime si es una cadena
        if isinstance(fecha_realizacion, str):
            try:
                fecha_realizacion = datetime.datetime.strptime(
                    fecha_realizacion, "%d/%m/%Y")
            except ValueError:
                pass  # Si la conversión falla, dejar la fecha como está
        if isinstance(fecha_realizacion, datetime.datetime):
            fecha_formateada = fecha_realizacion.strftime("%d/%m/%Y")
        else:
            fecha_formateada = fecha_realizacion
        materiales_y_responsables.append(
            (documento["nombre_material"], fecha_formateada, documento["nombre_responsable"]))

    # Cerrar conexión MongoDB
    cliente_mongo.close()

    return materiales_y_responsables


def eliminar_sustitucion_responsable(cedula, nuevo_codigo):
    """
    Elimina un responsable y sustituye su código por uno nuevo en la base de datos MySQL, actualizando también las referencias en la tabla Informacion_Pruebas.

    Args:
        cedula (str): Número de cédula del responsable a eliminar.
        nuevo_codigo (str): Nuevo código que sustituirá al código del responsable eliminado.
    """
    try:
        # Conexión a la base de datos MySQL
        conexion = pymysql.connect(
            host="localhost", user="root", password="info2024", db="Responsables_Pruebas")
        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()
        # Consulta para obtener el código del responsable
        consulta = f"SELECT codigo_responsable FROM Informacion_Responsables WHERE documento_I = '{
            cedula}'"
        # Ejecutar la consulta
        cursor.execute(consulta)
        # Obtener el resultado
        codigo_responsable = cursor.fetchone()[0]
        if codigo_responsable is None:
            print(
                Fore.RED + "ERROR! No se encontró un responsable con esa codigo en la base de datos MYSQL." + Style.RESET_ALL)
            return
        # Consulta para validar si el nuevo código existe en la tabla Informacion_Responsables
        consulta = f"SELECT * FROM Informacion_Responsables WHERE codigo_responsable = '{
            nuevo_codigo}'"
        # Ejecutar la consulta
        cursor.execute(consulta)
        # Obtener el resultado
        resultado = cursor.fetchone()
        if resultado is not None:
            consulta = f"DELETE FROM Informacion_Responsables WHERE documento_I = '{
                cedula}'"
            cursor.execute(consulta)
            # Actualizar el código del responsable en la tabla Informacion_pruebas
            consulta = f"UPDATE Informacion_pruebas SET codigo_responsable = '{
                nuevo_codigo}' WHERE codigo_responsable = '{codigo_responsable}'"
            cursor.execute(consulta)
            print(Fore.CYAN + "La información del responsable ha sido eliminada y actualizada correctamente en MYSQL." + Style.RESET_ALL)
        else:
            print(
                Fore.RED + "Error al editar y obtener el código del responsable en MYSQL" + Style.RESET_ALL)
    except Exception:
        print(
            Fore.RED + "Error al editar y obtener el código del responsable en MYSQL" + Style.RESET_ALL)
        # Confirmar los cambios
    conexion.commit()
    # Cerrar la conexión
    conexion.close()


def eliminar_sustitucion_responsable_mongo(cedula, nuevo_codigo, uri_mongo="mongodb://localhost:27017/"):
    """
    Elimina un responsable de la colección "Informacion_Responsables_M" en MongoDB y actualiza las referencias en la colección "informacion_pruebas".

    Args:
        cedula (str): Número de cédula del responsable a eliminar.
        nuevo_codigo (str): Nuevo código que sustituirá al código del responsable eliminado.
        uri_mongo (str): URI de conexión a la instancia de MongoDB. Por defecto, se conecta a "mongodb://localhost:27017/".
    """
    try:
        # Conexión a la base de datos MongoDB
        cliente = pymongo.MongoClient(uri_mongo)
        db = cliente["Responsables_Pruebas_M"]
        coleccion_responsables = db["Informacion_Responsables_M"]
        coleccion_pruebas = db["informacion_pruebas"]
        # Consulta para obtener el código del responsable
        responsable = coleccion_responsables.find_one({"documento_I": cedula})

        if not responsable:
            print(
                Fore.RED + "No se encontró un responsable con esa cédula en la base de datos de MONGODB." + Style.RESET_ALL)
            return

        codigo_responsable = responsable["_id"]

        # Validar si el nuevo código existe en la colección de responsables
        nuevo_codigo_existe = coleccion_responsables.find_one(
            {"_id": nuevo_codigo})
        if not nuevo_codigo_existe:
            print(
                Fore.RED + "ERROR! El nuevo código de responsable no existe." + Style.RESET_ALL)
            return
        else:
            # Eliminar al responsable de la colección
            coleccion_responsables.delete_one({"documento_I": cedula})

        # Actualizar el código del responsable en la colección de pruebas
        coleccion_pruebas.update_many({"codigo_responsable": codigo_responsable}, {
                                      "$set": {"codigo_responsable": nuevo_codigo}})

        print(Fore.CYAN + "La información del responsable ha sido eliminada y actualizada correctamente en MongoDB." + Style.RESET_ALL)

    except Exception as e:
        print(
            Fore.RED + f"Error al editar y obtener el código del responsable: {e}" + Style.RESET_ALL)
