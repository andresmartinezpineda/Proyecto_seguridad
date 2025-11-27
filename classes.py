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


    @staticmethod
    def normalize(text: str) -> str:
        """Convierte textos a minúsculas para comparar sin discriminar mayúsculas."""
        return text.strip().lower()

    @classmethod
    def copy_latest_order(cls, vendor_name: str, product: str, year: int, month: int):

        print("\n================ INICIO DEL PROCESO ================")
        print(f"> vendor_name = {vendor_name}")
        print(f"> product = {product}")
        print(f"> year = {year}")
        print(f"> month = {month}")
        print("====================================================\n")

        vendor_name_clean = cls.normalize(vendor_name)
        product_clean = cls.normalize(product)

        if product_clean not in ["oe", "oe jr"]:
            print("❌ Error: producto inválido")
            return

        origin_product_folder = "01. OE" if product_clean == "oe" else "02. OE JR"
        dest_product_folder = "OEA" if product_clean == "oe" else "OE JR"

        print(f"[INFO] Carpeta de producto origen esperada: {origin_product_folder}")
        print(f"[INFO] Carpeta de producto destino esperada: {dest_product_folder}\n")

        # 2. Recorrer carpetas en BASE_PATH
        print(f"[INFO] Leyendo carpetas en origen BASE_PATH:\n{cls.BASE_PATH}\n")

        for vendor_folder in os.listdir(cls.BASE_PATH):
            vendor_path = os.path.join(cls.BASE_PATH, vendor_folder)
            print(f"[CHECK] Revisando folder: {vendor_folder}")

            if not os.path.isdir(vendor_path):
                print("   - No es carpeta, se ignora.")
                continue

            # 3. Buscar año
            year_folder_name = f"Año {year}"
            year_folder_path = os.path.join(vendor_path, year_folder_name)
            print(f"   > Buscando carpeta de año: {year_folder_name}")

            if not os.path.isdir(year_folder_path):
                print("     ✖ No existe esta carpeta de año, continuar con siguiente vendor\n")
                continue

            print("     ✔ Carpeta de año encontrada.")

            # 4. Buscar mes
            target_month_prefix = f"{month:02d}-"
            print(f"   > Buscando carpeta de mes con prefijo: {target_month_prefix}")

            month_folder = None
            for folder in os.listdir(year_folder_path):
                if cls.normalize(folder).startswith(cls.normalize(target_month_prefix)):
                    month_folder = folder
                    break

            if not month_folder:
                print("     ✖ No se encontró carpeta del mes.\n")
                continue

            print(f"     ✔ Carpeta de mes encontrada: {month_folder}")

            month_folder_path = os.path.join(year_folder_path, month_folder)

            # 5. Producto
            print(f"   > Buscando carpeta del producto: {origin_product_folder}")

            product_folder_path = os.path.join(month_folder_path, origin_product_folder)
            if not os.path.isdir(product_folder_path):
                print("     ✖ No existe carpeta de producto.\n")
                continue

            print("     ✔ Carpeta de producto encontrada.")

            # 6. 02. Insertion orders
            print("   > Entrando a carpeta '02. Insertion orders'")

            insertion_orders_path = os.path.join(product_folder_path, "02. Insertion orders")
            if not os.path.isdir(insertion_orders_path):
                print("     ✖ No existe '02. Insertion orders'.\n")
                continue

            print("     ✔ Carpeta '02. Insertion orders' encontrada.")

            # 7. Buscar archivos
            print("   > Listando archivos en carpeta de inserción...")

            all_files = [
                f for f in os.listdir(insertion_orders_path)
                if os.path.isfile(os.path.join(insertion_orders_path, f))
            ]

            print(f"     ✔ {len(all_files)} archivos encontrados.")

            if not all_files:
                print("     ✖ No hay archivos, continuar.\n")
                continue

            # 8. versión = cantidad de archivos
            total_files = len(all_files)
            version_to_copy = f"{total_files}."

            print(f"   > Versión esperada a copiar: {version_to_copy}")

            # 9. Buscar archivo correcto
            print("   > Buscando archivo que coincida con la versión y vendor...")

            file_to_copy = None
            for file in all_files:
                if cls.normalize(file).startswith(cls.normalize(version_to_copy)):
                    print(f"     - Candidato encontrado: {file}")

                    parts = file.split()

                    try:
                        if product_clean == "oe":
                            # Unir todas las palabras del vendor
                            vendor_in_file = " ".join(parts[4:])
                        else:
                            vendor_in_file = " ".join(parts[5:])

                        # Quitar extensión (.xlsm, .xlsx, etc.)
                        vendor_in_file = os.path.splitext(vendor_in_file)[0]
                    except IndexError:
                        print("       ✖ Error analizando nombre del archivo.")
                        continue


                    print(f"       > Vendor extraído del archivo: {vendor_in_file}")

                    if cls.normalize(vendor_in_file) == vendor_name_clean:
                        print("       ✔ Coincidencia encontrada con el vendor solicitado.")
                        file_to_copy = file
                        break
                    else:
                        print("       ✖ Vendor no coincide.")

            if not file_to_copy:
                print("     ✖ No se encontró un archivo que coincida con vendor y versión.\n")
                continue

            print(f"     ✔ Archivo final a copiar: {file_to_copy}\n")

            # 10. Ruta origen
            origin_file_path = os.path.join(insertion_orders_path, file_to_copy)
            print(f"[INFO] Ruta completa del archivo origen:\n{origin_file_path}\n")

            # 11. Destino
            print("\n[INFO] Buscando ruta destino en Vendor.BASE_PATH...\n")

            dest_base = Vendor.BASE_PATH
            print(f"[INFO] Ruta base destino: {dest_base}")

            dest_vendor_folder = None
            for folder in os.listdir(dest_base):
                if cls.normalize(folder) == vendor_name_clean:
                    dest_vendor_folder = folder
                    break

            if not dest_vendor_folder:
                print("❌ No existe carpeta destino del vendor.\n")
                return

            print(f"✔ Carpeta destino del vendor: {dest_vendor_folder}")

            dest_vendor_path = os.path.join(dest_base, dest_vendor_folder)

            # Año destino
            dest_year_path = os.path.join(dest_vendor_path, str(year))
            print(f"> Buscando carpeta año destino: {dest_year_path}")

            if not os.path.isdir(dest_year_path):
                print("❌ No existe carpeta destino del año.\n")
                return

            print("✔ Carpeta año destino encontrada.")

            # Mes destino formato "11.November"
            print("> Buscando carpeta de mes destino...")

            month_prefix_point = f"{month:02d}."
            dest_month_folder = None
            for folder in os.listdir(dest_year_path):
                if cls.normalize(folder).startswith(cls.normalize(month_prefix_point)):
                    dest_month_folder = folder
                    break

            if not dest_month_folder:
                print("❌ No existe carpeta destino del mes.\n")
                return

            print(f"✔ Carpeta mes destino encontrada: {dest_month_folder}")

            dest_month_path = os.path.join(dest_year_path, dest_month_folder)

            # ordenes
            orders_path = os.path.join(dest_month_path, "ordenes")
            print("> Buscando carpeta 'ordenes'...")

            if not os.path.isdir(orders_path):
                print("❌ No existe carpeta 'ordenes'.\n")
                return

            print("✔ Carpeta 'ordenes' encontrada.")

            # Producto destino
            final_dest_path = os.path.join(orders_path, dest_product_folder)
            print(f"> Buscando carpeta destino final: {final_dest_path}")

            if not os.path.isdir(final_dest_path):
                print("❌ No existe carpeta final del producto.\n")
                return

            print("✔ Carpeta final destino encontrada.\n")

            # 12. COPIAR ARCHIVO
            print(">>> COPIANDO ARCHIVO...")

            shutil.copy2(origin_file_path, final_dest_path)

            print(f"✅ Archivo copiado exitosamente a:\n{final_dest_path}")
            print("================ FIN DEL PROCESO ====================\n")
            return

        print("❌ No se encontró ningún archivo coincidente con el vendor solicitado.\n")

    @classmethod
    def copy_latest_orders_batch(cls, vendors: list, product: str, year: int, month: int):
        """
        Ejecuta copy_latest_order para varios vendors.
        """
        print("\n=========== INICIO PROCESO POR LOTES ===========\n")
        
        for vendor in vendors:
            print(f"\n>>> Ejecutando para vendor: {vendor}")
            print("---------------------------------------------")
            
            try:
                cls.copy_latest_order(vendor, product, year, month)
            except Exception as e:
                print(f"❌ Error inesperado con vendor {vendor}: {e}")
        
        print("\n=========== FIN PROCESO POR LOTES ===========\n")
            
def main():
    vendor = Vendor("MGG")
    vendor.update_structure()

if __name__ == "__main__":
    main()





 