# Importar módulos estándar y clases auxiliares
import os                      # operaciones de sistema de archivos (path, exists, listdir, makedirs, etc.)
import shutil                  # funciones para copiar archivos (copy2)
import calendar                # obtener nombres de meses y utilidades relacionadas
from slack_bot import NOTIFIER  # importar el notificador de Slack preconfigurado
from datetime import datetime # obtener fecha y hora actuales


# ---------------------------------------------------------
# Clase Vendor: representa un vendor y su estructura en disco
# ---------------------------------------------------------
class Vendor:
    BASE_PATH = r"G:\Unidades compartidas\Vendor_files"  # Ruta base donde se guardan los vendors destino

    def __init__(self, name):
        """
        Inicializa un nuevo vendor con su nombre y ruta base.
        """
        self.name = name                                     # Nombre del vendor (string)
        self.base_path = Vendor.BASE_PATH                    # Referencia a la ruta base (constante de clase)
        self.vendor_path = os.path.join(Vendor.BASE_PATH, name)  # Ruta completa del vendor (base + nombre)
        self.current_year = datetime.now().year              # Año actual (int)
        self.current_month = datetime.now().month            # Mes actual (int)
        self.notifier = NOTIFIER   # notificador de Slack opcional (puede ser None)


    # ---------------------------------------------------------
    # Crear carpeta principal del vendor
    # ---------------------------------------------------------
    def create_vendor(self):
        """
        Crea la carpeta principal del vendor si no existe.
        """
        if not os.path.exists(self.vendor_path):             # Si la carpeta del vendor no existe
            os.makedirs(self.vendor_path)                    # Crear la carpeta (incluyendo padres si aplica)
            msg = f"Vendor '{self.name}' creado con éxito."  # Mensaje de éxito
            print(msg)                                       # Mostrar mensaje por consola
            return True

        else:                                               # Si la carpeta ya existía
            msg = f"⚠️ La carpeta del vendor '{self.name}' ya existe."  # Mensaje de aviso
            print(msg)                                       # Mostrar aviso por consola
            return False


    # ---------------------------------------------------------
    # Crear carpeta del año actual
    # ---------------------------------------------------------
    def create_year_folder(self):
        """
        Crea la carpeta del año actual dentro del vendor si no existe.
        Ejemplo: C:/Vendors/Sony/2025
        """
        year_path = os.path.join(self.vendor_path, str(self.current_year))  # Ruta al folder del año dentro del vendor

        if not os.path.exists(year_path):                 # Si la carpeta del año no existe
            os.makedirs(year_path)                        # Crear carpeta del año
            print(f"📁 Carpeta creada para el año: {self.current_year}")  # Mensaje de creación
        else:
            print(f"✅ Carpeta del año {self.current_year} ya existe.")    # Mensaje si ya existía

        return year_path                                   # Devolver la ruta del año (creada o existente)


    # ---------------------------------------------------------
    # Crear estructura del mes actual
    # ---------------------------------------------------------
    def create_month_structure(self):
        """
        Crea la estructura del mes actual dentro del año correspondiente.
        Ejemplo: C:/Vendor_files/Sony/2025/11/...
        """
        year_path = self.create_year_folder()              # Asegurar que la carpeta del año exista y obtener su ruta

        month_folder = f"{self.current_month:02d}.{calendar.month_name[self.current_month]}"  # Nombre carpeta mes "MM.MonthName"
        month_path = os.path.join(year_path, month_folder)  # Ruta completa al folder del mes

        if not os.path.exists(month_path):                 # Si la carpeta del mes no existe
            os.makedirs(month_path)                        # Crear la carpeta del mes
            print(f"📁 Carpeta creada para el mes: {month_folder}")  # Mensaje de creación
        else:
            print(f"✅ Carpeta del mes {month_folder} ya existe.")    # Mensaje si ya existía

        # Carpetas dentro del mes
        orders_path = os.path.join(month_path, "ordenes")  # Ruta a la carpeta 'ordenes' dentro del mes
        closures_path = os.path.join(month_path, "cierres")# Ruta a la carpeta 'cierres' dentro del mes

        # Crear las subcarpetas de órdenes (si no existen, no lanzar error)
        os.makedirs(os.path.join(orders_path, "OEA"), exist_ok=True)
        os.makedirs(os.path.join(orders_path, "OE JR"), exist_ok=True)

        # Crear la carpeta de cierres (exist_ok evita excepción si ya existe)
        os.makedirs(closures_path, exist_ok=True)

        print("📂 Estructura mensual creada correctamente.")  # Confirmación final


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
        vendor_created = self.create_vendor()                                # Crear carpeta principal si hace falta

        # 3. Crear carpeta del mes actual y sus subcarpetas
        self.create_month_structure()                       # Crear año/mes/ordenes/cierres

        # Crear nombre del mes en formato "MM.MonthName"
        month_folder = f"{self.current_month:02d}.{calendar.month_name[self.current_month]}"

        # Mensaje final resumen
        if vendor_created:
            msg = f"""🗂️ Vendor '{self.name}' creado con éxito:
        -    Estructura inicial creada para el año: {self.current_year}
        -    mes: {month_folder}"""
            # enviar a Slack este mensaje
            print(msg)
        else:
            msg = f"""⚠️ Vendor '{self.name}' ya existía."""

            # Si existe Slack, enviar el mensaje
            if self.notifier:
                self.notifier.send(msg)


    # ---------------------------------------------------------
    # Crear estructura de un mes y año personalizados en un solo vendor, esto se usara en el manager de vendors
    # para crear la estructura de un mes/año especifico en todos los vendors
    # ---------------------------------------------------------
    def create_custom_month_structure(self,vendor_name, year, month):
        """
        Crea la estructura de carpetas para un año y mes específicos
        """
        # Validar rango del mes
        if not 1 <= month <= 12:
            print("❌ El mes debe estar entre 1 y 12.")     # Mensaje de error si el mes no está en 1..12
            return                                       # Salir sin hacer cambios

        # Establecer temporalmente los valores de año y mes
        previous_year = self.current_year                    # Guarda el valor actual de self.current_year en previous_year
        previous_month = self.current_month                  # Guarda el valor actual de self.current_month en previous_month
        self.current_year = year                             # Sustituye temporalmente self.current_year por el año solicitado
        self.current_month = month                           # Sustituye temporalmente self.current_month por el mes solicitado

        # Reutiliza funciones existentes
        self.create_vendor()                                 # Crea carpeta principal del vendor (o no hace nada si ya existe)
        year_path = self.create_year_folder()                # Crea/retorna la carpeta del año (ahora modificado)

        # Crear la carpeta del mes y su estructura
        month_name = calendar.month_name[month]              # Obtiene el nombre del mes (ej. 'January')
        month_folder = f"{month:02d}.{month_name}"           # Formatea la carpeta como "MM.MonthName"
        month_path = os.path.join(year_path, month_folder)   # Construye la ruta completa del mes dentro del año

        if not os.path.exists(month_path):                   # Si la carpeta del mes no existe
            os.makedirs(month_path)                          # Crear la carpeta del mes
            msg = f"📁 La carpeta para  el vendor {vendor_name} del mes: {month_folder}"
            print(msg)  # Mensaje de creación exitosa
            if self.notifier:
                self.notifier.send(msg)
        else:
            msg = f"⚠️ Carpeta del vendor {vendor_name} para el mes {month_folder} ya existe."
            print(msg)    # Mensaje si ya existía
            if self.notifier:
                self.notifier.send(msg)

        # Subcarpetas internas (idéntico a tu estructura actual)
        orders_path = os.path.join(month_path, "ordenes")    # Ruta a 'ordenes' dentro del mes
        closures_path = os.path.join(month_path, "cierres")  # Ruta a 'cierres' dentro del mes

        os.makedirs(os.path.join(orders_path, "OEA"), exist_ok=True)  # Crear 'ordenes/OEA' si no existe
        os.makedirs(os.path.join(orders_path, "OE JR"), exist_ok=True)# Crear 'ordenes/OE JR' si no existe
        os.makedirs(closures_path, exist_ok=True)            # Crear 'cierres' si no existe

        print("📂 Estructura personalizada creada correctamente.")  # Confirmación final

        # Restaurar los valores originales de año y mes
        self.current_year = previous_year                     # Restaura el valor original de self.current_year
        self.current_month = previous_month                   # Restaura el valor original de self.current_month


# ---------------------------------------------------------
# Nueva clase para gestionar varios vendors (origen = Marketing Team)
# ---------------------------------------------------------
class ManagerVendors:
    # Referenciar la misma ruta base definida en el origen (Marketing Team)
    BASE_PATH = r"G:\Unidades compartidas\Marketing Team\Offline Marketing\03. Insertion orders\01. TV" 

    @classmethod
    def update_all_vendors_month(cls, year, month):
        """
        Crea la estructura de un mes/año específicos para todos los vendors dentro de Vendor.BASE_PATH.
        """
        if not os.path.exists(Vendor.BASE_PATH):             # Verificar que la ruta destino exista
            print(f"❌ La ruta base '{cls.BASE_PATH}' no existe. No se puede continuar.")  # Mensaje de error
            return                                           # Salir si no existe

        for vendor_name in os.listdir(Vendor.BASE_PATH):     # Iterar sobre cada vendor dentro de la ruta destino
            vendor_path = os.path.join(Vendor.BASE_PATH, vendor_name)  # Ruta al vendor
            if os.path.isdir(vendor_path):                    # Si es carpeta (vendor)
                vendor = Vendor(vendor_name)                  # Crear instancia temporal de Vendor
                try:
                    vendor.create_custom_month_structure(vendor_name,year, month)  # Crear estructura personalizada
                except Exception as e:
                    print(f"❌ Error al actualizar {vendor_name}: {e}") # Informar error si falla
                else:
                    print(f"✅ Actualizado vendor: {vendor_name}")     # Informar éxito

        print("🎯 Estructura de mes/año creada para todos los vendors.")  # Mensaje final


    @staticmethod
    def normalize(text: str) -> str:
        """Convierte textos a minúsculas para comparar sin discriminar mayúsculas."""
        return text.strip().lower()                         # Quitar espacios y convertir a minúsculas


    @classmethod
    def copy_latest_order(cls, vendor_name: str, product: str, year: int, month: int):
        """
        Copia el último archivo de insertion orders desde la ruta ORIGEN (Marketing Team)
        al Vendor correspondiente en Vendor.BASE_PATH, según product (OE / OE JR), año y mes.
        """
        print("\n================ INICIO DEL PROCESO ================")  # Encabezado informativo
        print(f"> vendor_name = {vendor_name}")                       # Mostrar vendor solicitado
        print(f"> product = {product}")                               # Mostrar producto solicitado
        print(f"> year = {year}")                                     # Mostrar año solicitado
        print(f"> month = {month}")                                   # Mostrar mes solicitado
        print("====================================================\n")

        vendor_name_clean = cls.normalize(vendor_name)                # Normalizar vendor para comparación
        product_clean = cls.normalize(product)                        # Normalizar producto para comparación

        if product_clean not in ["oe", "oe jr"]:                      # Validar producto permitido
            print("❌ Error: producto inválido")                      # Mensaje en caso de producto inválido
            return                                                   # Salir sin más acciones

        origin_product_folder = "01. OE" if product_clean == "oe" else "02. OE JR"  # Carpeta origen según producto
        dest_product_folder = "OEA" if product_clean == "oe" else "OE JR"          # Carpeta destino según producto

        print(f"[INFO] Carpeta de producto origen esperada: {origin_product_folder}")  # Info de carpeta origen
        print(f"[INFO] Carpeta de producto destino esperada: {dest_product_folder}\n")# Info de carpeta destino

        # 2. Recorrer carpetas en BASE_PATH
        print(f"[INFO] Leyendo carpetas en origen BASE_PATH:\n{cls.BASE_PATH}\n")    # Mostrar ruta origen que se recorrerá

        for vendor_folder in os.listdir(cls.BASE_PATH):                  # Iterar sobre cada carpeta en ruta origen
            vendor_path = os.path.join(cls.BASE_PATH, vendor_folder)     # Construir ruta completa al folder actual
            print(f"[CHECK] Revisando folder: {vendor_folder}")          # Imprimir carpeta que se está revisando

            if not os.path.isdir(vendor_path):                          # Si no es carpeta, ignorar
                print("   - No es carpeta, se ignora.")                 # Indicar que se omite
                continue

            # 3. Buscar año
            year_folder_name = f"Año {year}"                            # Nombre esperado: "Año 2025"
            year_folder_path = os.path.join(vendor_path, year_folder_name)  # Ruta esperada al folder del año
            print(f"   > Buscando carpeta de año: {year_folder_name}")  # Mostrar búsqueda de año

            if not os.path.isdir(year_folder_path):                     # Si no existe carpeta de año, continuar
                print("     ✖ No existe esta carpeta de año, continuar con siguiente vendor\n")
                continue

            print("     ✔ Carpeta de año encontrada.")                  # Confirmar que año fue encontrado

            # 4. Buscar mes (formato origen con guion "MM-Name")
            target_month_prefix = f"{month:02d}-"                       # Prefijo que identifica la carpeta del mes en origen
            print(f"   > Buscando carpeta de mes con prefijo: {target_month_prefix}")  # Mostrar prefijo buscado

            month_folder = None                                         # Inicializar variable para carpeta mes
            for folder in os.listdir(year_folder_path):                 # Iterar carpetas dentro del año
                if cls.normalize(folder).startswith(cls.normalize(target_month_prefix)):  # Comparar prefijos normalizados
                    month_folder = folder                               # Guardar carpeta mes encontrada
                    break

            if not month_folder:                                        # Si no se encontró el mes, continuar
                print("     ✖ No se encontró carpeta del mes.\n")
                continue

            print(f"     ✔ Carpeta de mes encontrada: {month_folder}")    # Informar mes encontrado

            month_folder_path = os.path.join(year_folder_path, month_folder)  # Ruta completa al folder de mes

            # 5. Producto (dentro del mes origen)
            print(f"   > Buscando carpeta del producto: {origin_product_folder}")  # Info producto origen

            product_folder_path = os.path.join(month_folder_path, origin_product_folder)  # Ruta a carpeta de producto origen
            if not os.path.isdir(product_folder_path):                        # Si no existe esa carpeta
                print("     ✖ No existe carpeta de producto.\n")
                continue

            print("     ✔ Carpeta de producto encontrada.")                    # Confirmar carpeta producto

            # 6. 02. Insertion orders (ruta dentro de product_folder_path)
            print("   > Entrando a carpeta '02. Insertion orders'")             # Mensaje informativo

            insertion_orders_path = os.path.join(product_folder_path, "02. Insertion orders")  # Ruta a insertion orders
            if not os.path.isdir(insertion_orders_path):                         # Si no existe esta subcarpeta
                print("     ✖ No existe '02. Insertion orders'.\n")
                continue

            print("     ✔ Carpeta '02. Insertion orders' encontrada.")            # Confirmación existencia

            # 7. Buscar archivos dentro de la carpeta de insertion orders
            print("   > Listando archivos en carpeta de inserción...")            # Mensaje informativo

            all_files = [                                                         # Listado de archivos (no directorios)
                f for f in os.listdir(insertion_orders_path)
                if os.path.isfile(os.path.join(insertion_orders_path, f))
            ]

            print(f"     ✔ {len(all_files)} archivos encontrados.")                # Mostrar cantidad de archivos hallados

            if not all_files:                                                     # Si no hay archivos, continuar con siguiente vendor
                print("     ✖ No hay archivos, continuar.\n")
                continue

            # 8. versión = cantidad de archivos (regla de negocio usada para elegir archivo)
            total_files = len(all_files)                                          # Contar archivos
            version_to_copy = f"{total_files}."                                   # Construir prefijo de versión: "N."

            print(f"   > Versión esperada a copiar: {version_to_copy}")            # Informar versión esperada

            # 9. Buscar archivo correcto según versión y vendor
            print("   > Buscando archivo que coincida con la versión y vendor...") # Mensaje informativo

            file_to_copy = None                                                    # Inicializar variable para el archivo final
            for file in all_files:                                                 # Iterar candidatos
                if cls.normalize(file).startswith(cls.normalize(version_to_copy)): # Filtrar por prefijo de versión
                    print(f"     - Candidato encontrado: {file}")                  # Mostrar candidato

                    parts = file.split()                                           # Separar nombre en partes por espacios

                    try:
                        if product_clean == "oe":                                 # Si producto es OE
                            # Unir todas las palabras del vendor (según posición esperada en el nombre)
                            vendor_in_file = " ".join(parts[4:])                   # Extraer vendor desde posición 4 en adelante
                        else:
                            vendor_in_file = " ".join(parts[5:])                   # Para "OE JR" el vendor empieza en posición 5

                        # Quitar extensión (.xlsm, .xlsx, etc.)
                        vendor_in_file = os.path.splitext(vendor_in_file)[0]      # Eliminar la extensión para comparar nombre del vendor
                    except IndexError:
                        print("       ✖ Error analizando nombre del archivo.")     # Manejo si la estructura del nombre no coincide
                        continue                                                   # Saltar este archivo candidato

                    print(f"       > Vendor extraído del archivo: {vendor_in_file}")  # Mostrar vendor extraído del nombre de archivo

                    if cls.normalize(vendor_in_file) == vendor_name_clean:          # Comparar vendor extraído con vendor solicitado
                        print("       ✔ Coincidencia encontrada con el vendor solicitado.")  # Coincidencia encontrada
                        file_to_copy = file                                           # Asignar archivo final a copiar
                        break                                                       # Salir del bucle de archivos
                    else:
                        print("       ✖ Vendor no coincide.")                        # No coincide, seguir buscando

            if not file_to_copy:                                                      # Si tras revisar todos no hay coincidencia
                print("     ✖ No se encontró un archivo que coincida con vendor y versión.\n")
                continue

            print(f"     ✔ Archivo final a copiar: {file_to_copy}\n")                   # Informar archivo seleccionado

            # 10. Ruta origen del archivo seleccionado
            origin_file_path = os.path.join(insertion_orders_path, file_to_copy)      # Ruta completa al archivo origen
            print(f"[INFO] Ruta completa del archivo origen:\n{origin_file_path}\n")    # Mostrar ruta origen

            # 11. Destino (buscar vendor equivalente en Vendor.BASE_PATH)
            print("\n[INFO] Buscando ruta destino en Vendor.BASE_PATH...\n")           # Mensaje informativo

            dest_base = Vendor.BASE_PATH                                              # Ruta destino base (vendors)
            print(f"[INFO] Ruta base destino: {dest_base}")                            # Mostrar ruta destino base

            dest_vendor_folder = None                                                  # Inicializar variable para carpeta destino
            for folder in os.listdir(dest_base):                                       # Iterar carpetas en destino
                if cls.normalize(folder) == vendor_name_clean:                        # Comparar nombres normalizados
                    dest_vendor_folder = folder                                       # Si coincide, guardar nombre real de carpeta destino
                    break

            if not dest_vendor_folder:                                                 # Si no se encontró carpeta destino
                print("❌ No existe carpeta destino del vendor.\n")                     # Mensaje de error
                return                                                                 # Salir del método (no continuar)

            print(f"✔ Carpeta destino del vendor: {dest_vendor_folder}")                 # Informar carpeta destino encontrada

            dest_vendor_path = os.path.join(dest_base, dest_vendor_folder)              # Ruta completa al vendor destino

            # Año destino dentro del vendor destino
            dest_year_path = os.path.join(dest_vendor_path, str(year))                  # Ruta al folder del año destino
            print(f"> Buscando carpeta año destino: {dest_year_path}")                  # Mostrar ruta buscada

            if not os.path.isdir(dest_year_path):                                       # Si no existe carpeta del año en destino
                print("❌ No existe carpeta destino del año.\n")                         # Mensaje de error
                return                                                                   # Salir

            print("✔ Carpeta año destino encontrada.")                                   # Confirmación año encontrado

            # Mes destino formato "MM.MonthName" en Vendor_files
            print("> Buscando carpeta de mes destino...")                                # Mensaje informativo

            month_prefix_point = f"{month:02d}."                                        # Prefijo que identifica carpeta mes detino ("MM.")
            dest_month_folder = None                                                    # Inicializar variable para carpeta mes destino
            for folder in os.listdir(dest_year_path):                                   # Iterar carpetas dentro del año destino
                if cls.normalize(folder).startswith(cls.normalize(month_prefix_point)): # Buscar carpeta que empiece con "MM."
                    dest_month_folder = folder                                         # Guardar carpeta encontrada
                    break

            if not dest_month_folder:                                                    # Si no se encontró carpeta mes destino
                print("❌ No existe carpeta destino del mes.\n")                         # Mensaje de error
                return                                                                   # Salir

            print(f"✔ Carpeta mes destino encontrada: {dest_month_folder}")               # Informar carpeta mes destino encontrada

            dest_month_path = os.path.join(dest_year_path, dest_month_folder)            # Ruta completa al folder del mes destino

            # Carpeta 'ordenes' dentro del mes destino
            orders_path = os.path.join(dest_month_path, "ordenes")                       # Ruta a 'ordenes' dentro del mes destino
            print("> Buscando carpeta 'ordenes'...")                                     # Mensaje informativo

            if not os.path.isdir(orders_path):                                           # Si no existe carpeta 'ordenes'
                print("❌ No existe carpeta 'ordenes'.\n")                                # Mensaje de error
                return                                                                   # Salir

            print("✔ Carpeta 'ordenes' encontrada.")                                     # Confirmar existencia

            # Producto destino dentro de 'ordenes'
            final_dest_path = os.path.join(orders_path, dest_product_folder)             # Ruta final donde se copiará el archivo
            print(f"> Buscando carpeta destino final: {final_dest_path}")                # Mostrar ruta final buscada

            if not os.path.isdir(final_dest_path):                                       # Si no existe carpeta de producto destino
                print("❌ No existe carpeta final del producto.\n")                       # Mensaje de error
                return                                                                   # Salir

            print("✔ Carpeta final destino encontrada.\n")                               # Confirmación final

            # 12. COPIAR ARCHIVO
            print(">>> COPIANDO ARCHIVO...")                                             # Mensaje antes de copiar

            shutil.copy2(origin_file_path, final_dest_path)                              # Copiar archivo preservando metadatos

            print(f"✅ Archivo copiado exitosamente a:\n{final_dest_path}")               # Confirmación de copia
            print("================ FIN DEL PROCESO ====================\n")              # Mensaje final de proceso
            return                                                                       # Salir del método al terminar exitosamente

        # Si se recorrió todo origen y no se encontró archivo coincidente para el vendor solicitado
        print("❌ No se encontró ningún archivo coincidente con el vendor solicitado.\n")


    @classmethod
    def copy_latest_orders_batch(cls, vendors: list, product: str, year: int, month: int):
        """
        Ejecuta copy_latest_order para varios vendors.
        """
        print("\n=========== INICIO PROCESO POR LOTES ===========\n")  # Encabezado batch

        for vendor in vendors:                                      # Iterar lista de vendors proporcionada
            print(f"\n>>> Ejecutando para vendor: {vendor}")        # Mensaje por vendor
            print("---------------------------------------------")
            try:
                cls.copy_latest_order(vendor, product, year, month)  # Llamada al proceso para cada vendor
            except Exception as e:
                print(f"❌ Error inesperado con vendor {vendor}: {e}") # Capturar e informar errores por vendor

        print("\n=========== FIN PROCESO POR LOTES ===========\n")     # Mensaje final batch



# def main():
#     vendor = Vendor("NBC Viacom")            
#     vendor.update_structure()

#     manager = ManagerVendors()
#     manager.copy_latest_orders_batch(["NBC Viacom", "Sony", "AMC"],"oe", 2025, 11)

#     manager.update_all_vendors_month(2026, 2)


# if __name__ == "__main__":
#     main()                             





