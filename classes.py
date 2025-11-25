import os
import re
import shutil
import calendar
from slack_bot import SlackNotifier
from datetime import datetime


class Vendor:
    BASE_PATH = r"G:\Unidades compartidas\Vendor_files"

    def __init__(self, name, notifier: SlackNotifier = None):
        """
        Inicializa un nuevo vendor con su nombre y ruta base.
        """
        self.name = name
        self.base_path = Vendor.BASE_PATH
        self.vendor_path = os.path.join(Vendor.BASE_PATH, name)
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.notifier = notifier   # notificador de Slack opcional

    # ---------------------------------------------------------
    # Crear carpeta principal del vendor
    # ---------------------------------------------------------
    def create_vendor(self):
        """
        Crea la carpeta principal del vendor si no existe.
        """
        if not os.path.exists(self.vendor_path):
            os.makedirs(self.vendor_path)
            msg = f"Vendor '{self.name}' creado con éxito."
            print(msg)

            if self.notifier:
                self.notifier.send(msg)

        else:
            msg = f"⚠️ La carpeta del vendor '{self.name}' ya existe."
            print(msg)

            if self.notifier:
                self.notifier.send(msg)


    # ---------------------------------------------------------
    # Crear carpeta del año actual
    # ---------------------------------------------------------
    def create_year_folder(self):
        """
        Crea la carpeta del año actual dentro del vendor si no existe.
        Ejemplo: C:/Vendors/Sony/2025
        """
        year_path = os.path.join(self.vendor_path, str(self.current_year))

        if not os.path.exists(year_path):
            os.makedirs(year_path)
            print(f"📁 Carpeta creada para el año: {self.current_year}")
        else:
            print(f"✅ Carpeta del año {self.current_year} ya existe.")

        return year_path


    # ---------------------------------------------------------
    # Crear estructura del mes actual
    # ---------------------------------------------------------
    def create_month_structure(self):
        """
        Crea la estructura del mes actual dentro del año correspondiente.
        Ejemplo: C:/Vendor_files/Sony/2025/11/...
        """
        year_path = self.create_year_folder()

        month_folder = f"{self.current_month:02d}.{calendar.month_name[self.current_month]}"  # Convierte 11 en "11", 2 en "02"
        month_path = os.path.join(year_path, month_folder)

        if not os.path.exists(month_path):
            os.makedirs(month_path)
            print(f"📁 Carpeta creada para el mes: {month_folder}")
        else:
            print(f"✅ Carpeta del mes {month_folder} ya existe.")

        # Carpetas dentro del mes
        orders_path = os.path.join(month_path, "ordenes")
        closures_path = os.path.join(month_path, "cierres")

        # Crear las subcarpetas de órdenes
        os.makedirs(os.path.join(orders_path, "OEA"), exist_ok=True)
        os.makedirs(os.path.join(orders_path, "OE JR"), exist_ok=True)

        # Crear la carpeta de cierres
        os.makedirs(closures_path, exist_ok=True)

        print("📂 Estructura mensual creada correctamente.")


    # ---------------------------------------------------------
    # Función principal para crear todo un vendor automaticamente
    # lo ideal es crear un objeto vendor y llamar a este metodo para crear toda la estructura
    # ---------------------------------------------------------
    def update_structure(self):
        """
        Verifica si existe toda la estructura del vendor y crea
        lo que falte (vendor, año y mes actual).
        """
        # 1. Crear carpeta del vendor
        self.create_vendor()

        # 3. Crear carpeta del mes actual y sus subcarpetas
        self.create_month_structure()

        print(f"✅ Estructura actualizada para {self.name}: {self.current_year}/{self.current_month:02d}")

    # ---------------------------------------------------------
    # Crear estructura de un mes y año personalizados en un solo vendor, esto se usara en el manager de vendors
    # para crear la estructura de un mes/año especifico en todos los vendors
    # ---------------------------------------------------------
    def create_custom_month_structure(self, year, month):
        """
        Crea la estructura de carpetas para un año y mes específicos
        """
        # Validar rango del mes
        if not 1 <= month <= 12:
            print("❌ El mes debe estar entre 1 y 12.")
            return

        # Establecer temporalmente los valores de año y mes
        previous_year = self.current_year                             # Guarda el valor actual de self.current_year en previous_year
        previous_month = self.current_month                           # Guarda el valor actual de self.current_month en previous_month
        self.current_year = year                                      # Sustituye temporalmente self.current_year por el año solicitado
        self.current_month = month                                    # Sustituye temporalmente self.current_month por el mes solicitado

        # Reutiliza funciones existentes
        self.create_vendor()                # Crea carpeta principal del vendor (o no hace nada si ya existe) usando tu método existente
        year_path = self.create_year_folder()  # Crea (si hace falta) la carpeta del año actual (ahora modificado) y obtiene su ruta

        # Crear la carpeta del mes y su estructura
        month_name = calendar.month_name[month]                       # Obtiene el nombre del mes (ej. 'January') usando el número de mes dado
        month_folder = f"{month:02d}.{month_name}"                    # Formatea el nombre de la carpeta como "01.January", "11.November", etc.
        month_path = os.path.join(year_path, month_folder)            # Construye la ruta completa del mes dentro de la carpeta del año

        if not os.path.exists(month_path):                            # Comprueba si la carpeta del mes ya existe en disco
            os.makedirs(month_path)                                   # Si no existe, la crea (incluye carpetas intermedias si hiciera falta)
            print(f"📁 Carpeta creada para el mes: {month_folder}")   # Imprime mensaje indicando que se creó la carpeta del mes
        else:
            print(f"✅ Carpeta del mes {month_folder} ya existe.")     # Si ya existía, imprime mensaje indicando que no se crea de nuevo

        # Subcarpetas internas (idéntico a tu estructura actual)
        orders_path = os.path.join(month_path, "ordenes")             # Define la ruta para la carpeta 'ordenes' dentro del mes
        closures_path = os.path.join(month_path, "cierres")           # Define la ruta para la carpeta 'cierres' dentro del mes

        os.makedirs(os.path.join(orders_path, "OEA"), exist_ok=True)  # Crea 'ordenes/OEA', no falla si ya existe gracias a exist_ok=True
        os.makedirs(os.path.join(orders_path, "OE JR"), exist_ok=True) # Crea 'ordenes/OE JR', no falla si ya existe
        os.makedirs(closures_path, exist_ok=True)

        print("📂 Estructura personalizada creada correctamente.")     # Mensaje final indicando que la estructura del mes personalizado quedó creada

        # Restaurar los valores originales de año y mes
        self.current_year = previous_year                             # Restaura el valor original de self.current_year guardado al inicio
        self.current_month = previous_month                           # Restaura el valor original de self.current_month guardado al inicio

    # ---------------------------------------------------------
    # Funcion para tomar el archivo de un drive y dejarlo en otro
    # utilizando como referencia del nombre de los archivos: (mes/año/producto/vendor)
    # esto se usara en el manager de vendors para procesar archivos de todos los vendors
    # ---------------------------------------------------------
    def process_latest_file(self, source_path):
        """
        Busca el archivo más reciente en 'source_path', analiza su nombre
        para determinar vendor, mes, año y tipo (OE / OE JR), y lo copia
        automáticamente a la carpeta correcta del vendor correspondiente.
        """
        # ---------------------------------------------------------
        # Obtener archivo más reciente
        # ---------------------------------------------------------
        if not os.path.exists(source_path):                            # Comprueba que la ruta de origen exista
            print(f"❌ La ruta de origen '{source_path}' no existe.")   # Informa si no existe la ruta
            return                                                     # Sale de la función para evitar errores

        files = [                                                       # Lista todos los elementos en source_path
            f for f in os.listdir(source_path)
            if os.path.isfile(os.path.join(source_path, f))            # Filtra dejando solo ficheros (no carpetas)
        ]

        if not files:                                                   # Si no hay archivos en la carpeta de origen
            print("⚠️ No hay archivos en la carpeta de origen.")        # Informa y sale
            return

        # Elegir archivo más reciente por fecha de modificación
        latest_file = max(                                               # Selecciona el nombre del archivo con mayor mtime
            files,
            key=lambda f: os.path.getmtime(os.path.join(source_path, f))
        )

        latest_path = os.path.join(source_path, latest_file)             # Construye la ruta completa del archivo más reciente
        print(f"📄 Archivo más reciente encontrado: {latest_file}")      # Muestra el nombre del archivo elegido

        # ---------------------------------------------------------
        # Parsear nombre del archivo
        # Ej: '3. OT Nov'25 OE AMC'
        # ---------------------------------------------------------
        # Quitar solo el número inicial.
        clean_name = latest_file                                         # Copia el nombre original para limpiarlo sin modificarlo

        # Si empieza con "número."
        if clean_name[0].isdigit() and "." in clean_name.split()[0]:     # Detecta el numero de version del documento
            clean_name = clean_name.split(".", 1)[1].strip()             # Elimina ese numero y el punto (queda el resto del nombre)

        parts = clean_name.split()                                       # Separa el nombre limpio dividido por espacios(cada cadena separada por espacio la llamaremos "Token")

        # Buscar mes abreviado (3 letras antes del ')
        month_part = next((p for p in parts if "'" in p), None)          # Busca el token que contiene el apóstrofo (ej: "Nov'25")
        if not month_part:                                               # Si no encuentra ese token
            print("❌ No se pudo detectar el mes en el archivo.")        # Informa el error
            return                                                       # Sale de la función

        month_abbrev = month_part[:3]                                    # Toma las 3 primeras letras del token para obtener la abreviatura (ej: "Nov")
        year_suffix = month_part.split("'")[1]                           # Toma la parte después del apóstrofo (ej: "25")

        # Convertir año a formato 4 dígitos
        year = 2000 + int(year_suffix)                                   # Convierte "25" en 2025 (asume siglo 2000)

        # Convertir mes a número
        try:
            month_num = list(calendar.month_abbr).index(month_abbrev)    # Busca el índice de la abreviatura en calendar.month_abbr (0..12)
        except ValueError:                                               # Si la abreviatura no existe
            print(f"❌ Mes '{month_abbrev}' no reconocido.")              # Informa el error
            return                                                       # Sale de la función

        # ---------------------------------------------------------
        # Detectar el nombre del producto (OE / OE JR)
        # ---------------------------------------------------------
        file_text = latest_file.upper()                                   # Convierte el nombre original a mayúsculas para comparar sin distinción

        if "OE JR" in file_text:                                          # Si contiene "OE JR" (caso específico)
            order_type_folder = "OE JR"                                   # Asigna la carpeta destino exacta "OE JR"
        elif "OE" in file_text:                                           # Si contiene "OE" (y no "OE JR")
            order_type_folder = "OEA"                                     # Asigna la carpeta destino "OEA"
        else:
            print("❌ No se encontró producto OE u OE JR en el nombre del archivo.")  # Si no encuentra el nombre del producto, informa
            return                                                       # Sale de la función

        # ---------------------------------------------------------
        # Detectar vendor (última palabra del nombre)
        # ---------------------------------------------------------
        # Obtener el último fragmento (ej: "AMC.xlsm")
        last_part = parts[-1]                                             # Toma el último token del nombre limpiado

        # Quitar extensión correctamente
        vendor_name = os.path.splitext(last_part)[0].upper()              # Quita la extensión con splitext y pasa a mayúsculas (ej: "AMC")

        # Verificar si existe la carpeta del vendor
        vendor_path = os.path.join(self.BASE_PATH, vendor_name)           # Construye la ruta esperada del vendor dentro de BASE_PATH
        if not os.path.exists(vendor_path):                               # Si esa carpeta no existe
            print(f"❌ No existe el vendor '{vendor_name}' en la ruta base.")  # Informa que el vendor no fue encontrado
            return                                                       # Sale de la función

        # ---------------------------------------------------------
        # Crear estructura si no existe (reutiliza tu lógica)
        # ---------------------------------------------------------
        temp_vendor = Vendor(vendor_name)                                  # Crea una instancia temporal de Vendor para reutilizar sus métodos
        temp_vendor.create_custom_month_structure(year, month_num)         # Llama a tu método para asegurar que año/mes existan

        # ---------------------------------------------------------
        # Construir ruta final
        # ---------------------------------------------------------
        month_full_name = calendar.month_name[month_num]                   # Obtiene el nombre completo del mes (ej: "November")
        month_folder = f"{month_num:02d}.{month_full_name}"                # Formatea la carpeta del mes como "11.November"

        final_path = os.path.join(                                        # Construye la ruta final donde irá el archivo
            vendor_path,
            str(year),
            month_folder,
            "ordenes",
            order_type_folder
        )

        os.makedirs(final_path, exist_ok=True)                            # Asegura que la ruta final exista (la crea si falta)

        # Ruta del archivo de destino
        destination_file = os.path.join(final_path, latest_file)          # Nombre final: conserva el nombre original del archivo

        # ---------------------------------------------------------
        # Copiar archivo (reemplaza si ya existe)
        # ---------------------------------------------------------
        try:
            shutil.copy2(latest_path, destination_file)                     # Copia el archivo preservando metadatos; sobrescribe si existe
            print(f"✅ Archivo copiado a: {destination_file}")                 # Mensaje final indicando la ruta destino
        except PermissionError:
            print("❌ El archivo está en uso por otro programa (Excel u otro). No se pudo copiar.")
            return
        except Exception as e:
            print(f"❌ Error inesperado al copiar el archivo: {e}")
            return 

# Nueva clase para gestionar varios vendors
class ManagerVendors:
    # Referenciar la misma ruta base definida en Vendor evita duplicar la constante
    BASE_PATH = r"G:\Unidades compartidas\Marketing Team\Offline Marketing\03. Insertion orders\01. TV"

    @classmethod
    def update_all_vendors_month(cls, year, month):
        """
        Crea la estructura de un mes/año específicos para todos los vendors dentro de BASE_PATH.
        """
        if not os.path.exists(Vendor.BASE_PATH):
            print(f"❌ La ruta base '{cls.BASE_PATH}' no existe. No se puede continuar.")
            return

        for vendor_name in os.listdir(Vendor.BASE_PATH):
            vendor_path = os.path.join(Vendor.BASE_PATH, vendor_name)
            if os.path.isdir(vendor_path):
                vendor = Vendor(vendor_name)
                try:
                    vendor.create_custom_month_structure(year, month)
                except Exception as e:
                    print(f"❌ Error al actualizar {vendor_name}: {e}")
                else:
                    print(f"✅ Actualizado vendor: {vendor_name}")

        print("🎯 Estructura de mes/año creada para todos los vendors.")


    @classmethod
    def process_all_latest_files(cls, selected_year, selected_month):
        """
        Procesa archivos de todos los vendors usando el año y mes seleccionados.
        Busca carpetas de año como: 'Año 2025', '2025', '2025 OLD', etc.
        Busca carpetas de mes como: '11-November', '11_December', '11.November', etc.
        """
        # -----------------------------------------------------------
        # Formatos aceptados para el mes
        # -----------------------------------------------------------
        possible_month_prefixes = [
            f"{selected_month:02d}-",  # ejemplo real: "11-November" (prefijo con guion)
            f"{selected_month:02d}_",  # variante: "11_November" (prefijo con guion bajo)
            f"{selected_month:02d}.",  # variante: "11.November" (prefijo con punto)
        ]  # <-- lista con los prefijos posibles que se usarán para detectar la carpeta del mes

        # -----------------------------------------------------------
        # Recorrer cada vendor dentro de la ruta base
        # -----------------------------------------------------------
        for vendor_name in os.listdir(cls.BASE_PATH):                # Lee todos los elementos en BASE_PATH (posibles vendors)
            vendor_path = os.path.join(cls.BASE_PATH, vendor_name)   # Construye la ruta completa del vendor

            if not os.path.isdir(vendor_path):                       # Si no es una carpeta (ej: archivo), saltarla
                continue

            print(f"\n🔍 Procesando vendor: {vendor_name}")          # Mensaje informativo: vendor que se está procesando

            # -------------------------------------------------------
            # 1. BUSCAR LA CARPETA DEL AÑO (ej: "Año 2025", "2025", etc.)
            # -------------------------------------------------------
            year_folder = None                                       # Inicializar variable que contendrá el nombre de la carpeta de año
            year_pattern = re.compile(rf".*{selected_year}.*")       # Expresión regular: coincide con cualquier carpeta que contenga el número del año

            for folder in os.listdir(vendor_path):                   # Iterar sobre las carpetas/archivos dentro del vendor
                full_path = os.path.join(vendor_path, folder)        # Construir la ruta completa del item actual
                if os.path.isdir(full_path) and year_pattern.match(folder):  # Si es carpeta y su nombre coincide con el patrón del año
                    year_folder = folder                             # Guardar el nombre de la carpeta de año encontrada
                    break                                            # Salir del bucle al encontrar la primera coincidencia

            if not year_folder:                                      # Si no se encontró ninguna carpeta que contenga el año
                print(f"⚠️ El vendor '{vendor_name}' no tiene pautas en el año {selected_year}.")  # Mensaje informativo de ausencia
                continue                                             # Seguir con el siguiente vendor

            year_path = os.path.join(vendor_path, year_folder)       # Construir la ruta completa a la carpeta de año encontrada
            print(f"📁 Carpeta encontrada del año: {year_folder}")   # Mensaje informativo con el nombre exacto de la carpeta de año

            # -------------------------------------------------------
            # 2. BUSCAR LA CARPETA DEL MES (formato flexible: 11-November | 11_November | 11.November)
            # -------------------------------------------------------
            month_folder = None                                      # Inicializar variable que contendrá el nombre de la carpeta del mes

            for folder in os.listdir(year_path):                     # Iterar sobre los elementos dentro de la carpeta del año
                # Si el nombre de la carpeta empieza con cualquiera de los prefijos aceptados => es el mes buscado
                if any(folder.startswith(prefix) for prefix in possible_month_prefixes):
                    month_folder = folder                            # Guardar el nombre de la carpeta del mes encontrada
                    break                                            # Salir del bucle al encontrar la primera coincidencia

            if not month_folder:                                     # Si no se encontró la carpeta del mes
                print(f"⚠️ El vendor '{vendor_name}' no tiene pautas en el mes {selected_month:02d}.")  # Mensaje informativo de ausencia
                continue                                             # Seguir con el siguiente vendor

            month_path = os.path.join(year_path, month_folder)       # Construir la ruta completa a la carpeta del mes encontrada
            print(f"📁 Carpeta encontrada del mes: {month_folder}")  # Mensaje informativo con el nombre exacto de la carpeta del mes

            # -------------------------------------------------------
            # 3. PROCESAR CARPETAS "01. OE" Y "02. OE JR"
            # -------------------------------------------------------
            oe_folders = {
                "01. OE": "02. Insertion orders",                    # Mapeo: carpeta principal -> subcarpeta donde están las insertion orders
                "02. OE JR": "02. Insertion orders",
            }

            vendor_instance = Vendor(vendor_name)                    # Crear instancia temporal de Vendor para reutilizar process_latest_file

            for main_folder, subfolder in oe_folders.items():        # Iterar sobre ambas carpetas (OE y OE JR)
                main_path = os.path.join(month_path, main_folder)    # Ruta a "01. OE" o "02. OE JR"
                final_orders_path = os.path.join(main_path, subfolder)  # Ruta a "02. Insertion orders" dentro de la anterior

                if os.path.isdir(final_orders_path):                 # Si la ruta existe (carpeta de insertion orders)
                    print(f"📄 Procesando archivos en: {final_orders_path}")  # Mensaje informativo antes de procesar
                    vendor_instance.process_latest_file(final_orders_path)   # Llamada al método que copia el archivo más reciente
                else:
                    print(f"⚠️ No se encontró {final_orders_path}")  # Mensaje informando que la subcarpeta esperada no existe

    @classmethod
    def send_vendor_summary(cls, year: int, month: int):
        """
        Busca en cada vendor origen el archivo 'Summary' y lo copia al vendor destino.
        Se respetan los formatos:
        - Origen:  "MM-MonthName"  (ej: "12-December")
        - Destino: "MM.MonthName"  (ej: "12.November") y dentro de esa carpeta entramos en 'cierres/'
        No crea carpetas nuevas; si falta algo imprime mensaje y continúa.
        """
        # Nombre de carpeta mes destino: "11.November"
        month_name = datetime(year, month, 1).strftime("%B")  # p. ej. "November"  -> obtiene nombre del mes completo

        month_folder_dest = f"{month:02d}.{month_name}"       # p. ej. "11.November"  -> construye carpeta destino con formato MM.MonthName

        # Nombre de carpeta mes origen: "11-November"
        month_folder_src = f"{month:02d}-{month_name}"        # p. ej. "11-November"  -> construye carpeta origen con guion (formato esperado en remitente)

        # Validar que la ruta remitente exista
        if not os.path.isdir(cls.BASE_PATH):                  # comprueba que la ruta base de remitente exista y sea directorio
            print(f"❌ La ruta remitente '{cls.BASE_PATH}' no existe.")  # informa si no existe
            return                                           # sale si la ruta remitente no existe

        # Recorrer todos los vendors en la ruta remitente
        for vendor in os.listdir(cls.BASE_PATH):              # itera sobre cada entrada en la ruta remitente
            vendor_path = os.path.join(cls.BASE_PATH, vendor) # construye la ruta completa al item actual
            if not os.path.isdir(vendor_path):                # si el item no es carpeta, lo ignora
                continue  # ignorar archivos sueltos

            # Buscar carpeta del año origen
            year_folder_src = None                            # inicializa variable para guardar el nombre de la carpeta del año encontrado
            year_re = re.compile(rf".*{year}.*")              # regex para encontrar cualquier carpeta que contenga el año (flexible: "2025", "Año 2025", etc.)
            for entry in os.listdir(vendor_path):             # recorre entradas dentro del vendor
                full_entry = os.path.join(vendor_path, entry) # ruta completa de la entrada
                if os.path.isdir(full_entry) and year_re.match(entry):  # si es carpeta y su nombre coincide con la regex
                    year_folder_src = entry                   # guarda el nombre de la carpeta del año
                    break                                     # sale del bucle al encontrar la primera coincidencia
            if not year_folder_src:                           # si no se encontró carpeta de año, sigue al siguiente vendor
                continue

            # Carpeta mes origen (formato con guion)
            path_month = os.path.join(vendor_path, year_folder_src, month_folder_src)  # arma la ruta a la carpeta del mes en el origen
            if not os.path.isdir(path_month):                 # si no existe la carpeta mes en el origen, pasa al siguiente vendor
                continue

            # Entrar a "01. OE"
            oe_path = os.path.join(path_month, "01. OE")      # ruta esperada donde está el summary dentro del mes origen
            if not os.path.isdir(oe_path):                    # si no existe, saltar vendor
                continue

            # Entrar a "05. Certificates (CT) and Closures"
            summary_folder = os.path.join(oe_path, "05. Certificates (CT) and Closures")  # carpeta donde se busca el archivo Summary
            if not os.path.isdir(summary_folder):             # si no existe la carpeta de summary, saltar vendor
                continue

            # Buscar archivo Summary
            summary_file = None                               # variable para almacenar nombre de archivo encontrado
            for f in os.listdir(summary_folder):              # recorrer archivos en la carpeta de summary
                if os.path.isfile(os.path.join(summary_folder, f)) \
                and "SUMMARY" in f.upper() \
                and f.lower().endswith((".xls", ".xlsx", ".xlsm")):  # filtro: que sea archivo y contenga "SUMMARY" y tenga extensión Excel
                    summary_file = f                          # asigna el primer archivo que cumple la condición
                    break                                     # rompe tras encontrar el primer match

            if summary_file is None:                          # si no encontró summary en esa carpeta
                print(f'El documento de cierre de "{vendor}" no está disponible aun.')  # informa y continúa con siguiente vendor
                continue

            summary_path = os.path.join(summary_folder, summary_file)  # ruta completa al archivo summary encontrado

            # --------------------------------------------------------
            # EXTRAER summary SEGÚN TU REGLA
            # --------------------------------------------------------
            name_no_ext = os.path.splitext(summary_file)[0]   # quita la extensión para analizar el nombre
            try:
                part_after_second_dash = name_no_ext.split("-", 2)[2]  # intenta obtener la parte después del segundo guion
            except IndexError:
                print(f"No se pudo leer el vendor destino en el archivo: {summary_file}")  # si el formato no coincide, informa y continua
                continue

            if "_" in part_after_second_dash:                  # si contiene underscore, elimina el sufijo tras el último underscore
                summary = part_after_second_dash.rsplit("_", 1)[0]
            else:
                summary = part_after_second_dash               # si no, usa la parte tal cual

            summary = summary.rstrip("-_. ").strip()           # limpia caracteres sobrantes al final y espacios

            # --------------------------------------------------------
            # 🔥 AQUI VA TU NUEVA LÓGICA (respeta todo lo anterior)
            #
            # 1. Ir a Vendor.BASE_PATH
            # 2. Revisar cada vendor
            # 3. Buscar carpeta cuyo nombre coincida EXACTAMENTE con summary
            # 4. Dentro de esa misma carpeta, entrar al año
            # 5. Luego al mes con formato "MM.MonthName"
            # 6. Luego a "cierres"
            # --------------------------------------------------------

            # -----------------------------------------------
            # 🔍 Buscar dentro de cada vendor una carpeta cuyo
            #     nombre coincida EXACTAMENTE con summary
            # -----------------------------------------------
            final_vendor_path = None

            for vendor_folder in os.listdir(Vendor.BASE_PATH):
                vendor_folder_path = os.path.join(Vendor.BASE_PATH, vendor_folder)

                if not os.path.isdir(vendor_folder_path):
                    continue

                # Revisar las subcarpetas dentro del vendor
                for subfolder in os.listdir(vendor_folder_path):
                    subfolder_path = os.path.join(vendor_folder_path, subfolder)

                    if os.path.isdir(subfolder_path) and subfolder == summary:
                        final_vendor_path = vendor_folder_path
                        break

                if final_vendor_path:
                    break

            if not final_vendor_path:                         # si no encontró vendor destino exacto
                print(f'El vendor destino "{summary}" no existe en la ruta destino.')  # informa y continúa
                continue

            # Buscar carpeta del año en esta misma ruta
            target_year_path = os.path.join(final_vendor_path, str(year))  # arma ruta al año dentro del vendor destino
            if not os.path.isdir(target_year_path):          # si no existe la carpeta del año en destino
                print(f'El vendor destino "{summary}" no tiene carpeta para el año {year}.')  # informa y continúa
                continue

            # Buscar carpeta del mes
            target_month_path = os.path.join(target_year_path, month_folder_dest, "cierres")  # arma ruta final esperada: MM.MonthName/cierres
            if not os.path.isdir(target_month_path):        # si no existe la carpeta de cierres en destino
                print(f"la carpeta para el cierre de '{summary}' no fue encontrada")  # informa y continúa
                continue

            # Copiar archivo al destino final
            destination = os.path.join(target_month_path, summary_file)  # ruta destino final del archivo
            try:
                shutil.copy2(summary_path, destination)      # copia preservando metadatos; sobreescribe si ya existe
                print(f"cierre de '{summary}' guardado con exito")  # confirma éxito
            except PermissionError:
                print(f"❌ Permiso denegado al copiar a: {destination}")  # manejo específico de permiso denegado
            except Exception as e:
                print(f"❌ Error copiando archivo: {e}")         # manejo genérico de errores al copiar

def main():

    vendor = Vendor("sony")
    vendor.update_structure()
    manager_vendors = ManagerVendors()
    manager_vendors.update_all_vendors_month(2025,9)
    manager_vendors.send_vendor_summary(2025,9)


if __name__ == "__main__":
    main()
