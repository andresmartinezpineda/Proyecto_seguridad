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


def main():
    name_vendor = input("Ingresa el nombre del vendor: ")
    vendor = Vendor(name_vendor)
    vendor.update_structure()

if __name__ == "__main__":
    main()
