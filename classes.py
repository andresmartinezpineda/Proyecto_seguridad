import os
import calendar
from datetime import datetime

class Vendor:

    BASE_PATH = r"G:\Unidades compartidas\Vendor_files"

    def __init__(self, name):
        """
        Inicializa un nuevo vendor con su nombre y ruta base.
        """
        self.name = name
        self.base_path = Vendor.BASE_PATH
        self.vendor_path = os.path.join(Vendor.BASE_PATH, name)
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

    # ---------------------------------------------------------
    # 1️⃣  Crear carpeta principal del vendor
    # ---------------------------------------------------------
    def create_vendor(self):
        """
        Crea la carpeta principal del vendor si no existe.
        Ejemplo: C:/Vendors/Sony
        """
        if not os.path.exists(self.vendor_path):
            os.makedirs(self.vendor_path)
            print(f"📁 Carpeta creada para el vendor: {self.name}")
        else:
            print(f"⚠️ La carpeta del vendor {self.name} ya existe.")


    # ---------------------------------------------------------
    # 2️⃣  Crear carpeta del año actual
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
    # 3️⃣  Crear estructura del mes actual
    # ---------------------------------------------------------
    def create_month_structure(self):
        """
        Crea la estructura del mes actual dentro del año correspondiente.
        Ejemplo: C:/Vendors/Sony/2025/11/
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

        # Crear carpeta de cierres del mes actual (ej: cierres/11)
        os.makedirs(os.path.join(closures_path, month_folder), exist_ok=True)

        print("📂 Estructura mensual creada correctamente.")


    # ---------------------------------------------------------
    # 4️⃣  Función principal para actualizar todo automáticamente
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
    # Crear estructura de un mes y año personalizados
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
        os.makedirs(os.path.join(closures_path, month_folder), exist_ok=True) # Crea 'cierres/<mes_folder>' (ej: 'cierres/11.November'), no falla si ya existe

        print("📂 Estructura personalizada creada correctamente.")     # Mensaje final indicando que la estructura del mes personalizado quedó creada

        # Restaurar los valores originales de año y mes
        self.current_year = previous_year                             # Restaura el valor original de self.current_year guardado al inicio
        self.current_month = previous_month                           # Restaura el valor original de self.current_month guardado al inicio


def update_all_vendors_month(year, month):
    # ---------------------------------------------------------
    # 🆕 Crear estructura de un mes y año personalizados
    # ---------------------------------------------------------

    BASE_PATH = r"G:\Unidades compartidas\Vendor_files"          # Ruta base donde se almacenan todas las carpetas de los vendors
        
    # Verificar que la ruta base exista antes de continuar
    if not os.path.exists(BASE_PATH):                            # Comprueba si la ruta base existe en el sistema
        print(f"❌ La ruta base '{BASE_PATH}' no existe. No se puede continuar.")  # Muestra error si la ruta no existe
        return                                                   # Sale de la función para evitar errores posteriores

    # Recorrer todas las carpetas (vendors) dentro de la ruta base
    for vendor_name in os.listdir(BASE_PATH):                    # Itera sobre cada elemento dentro de la ruta base
        vendor_path = os.path.join(BASE_PATH, vendor_name)       # Construye la ruta completa del elemento actual

        # Solo continuar si el elemento es una carpeta
        if os.path.isdir(vendor_path):                           # Verifica que el elemento sea una carpeta y no un archivo
            vendor = Vendor(vendor_name)                         # Crea una instancia de la clase Vendor con el nombre de la carpeta
            
            try:
                # Llamar al método existente para crear la carpeta del mes/año
                vendor.create_custom_month_structure(year, month)   # Usa el método para crear la estructura del mes/año personalizado
            except Exception as e:
                print(f"❌ Error al actualizar {vendor_name}: {e}")

            print(f"✅ Actualizado vendor: {vendor_name}")       # Informa que el vendor fue actualizado correctamente

    # Confirmar que todo terminó correctamente
    print("🎯 Estructura de mes/año creada para todos los vendors.")  # Mensaje final confirmando que el proceso concluyó



def main():

    year = int(input("ingresa el año:"))
    month = int(input("ingresa el mes:"))
    update_all_vendors_month(year,month)

if __name__ == "__main__":
    main()
