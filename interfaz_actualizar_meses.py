import tkinter as tk                    # Crear interfaces gráficas con Tkinter
from classes import ManagerVendors      # Clase para gestionar múltiples vendors
import sys                              # Redirigir stdout/stderr hacia widget de consola
from classes import ConsoleRedirect     # Redirector para mostrar salida en widget Text

# ---------------------------------------------------------
# Paleta de colores usada en la interfaz
# ---------------------------------------------------------
COLOR_BG = "#FFFFFF"                    # Color de fondo de la ventana
COLOR_PRIMARY = "#007BFF"               # Color principal (botón Crear)
COLOR_ACCENT = "#00A3E0"                # Color activo para botones
COLOR_TEXT = "#003B5C"                  # Color del texto principal


def open_update_months(root):
    """
    Abre ventana secundaria para crear estructura de nuevo año y mes en todos los vendors.
    - root: ventana principal para retornar cuando se cierre esta ventana.
    """
    win = tk.Toplevel(root)               # Crear ventana hija sobre root
    manager = ManagerVendors()            # Instancia de ManagerVendors para ejecutar métodos
    win.title("Crear estructura de nuevo año y mes")  # Título de la ventana
    win.geometry("600x600")               # Dimensiones fijas
    win.configure(bg=COLOR_BG)            # Aplicar color de fondo

    # -------------------------------------------------------
    # Función: volver a ventana principal
    # -------------------------------------------------------
    def volver():
        """
        Cierra la ventana actual y reaparece la ventana principal.
        """
        win.destroy()                      # Cerrar ventana hija
        root.deiconify()                   # Mostrar ventana principal nuevamente

    # -------------------------------------------------------
    # Función: validar año (máximo 4 dígitos)
    # -------------------------------------------------------
    def validar_year(texto, accion):
        """
        Valida que el año no exceda 4 dígitos.
        accion = "1" cuando se inserta texto, "0" cuando se borra
        """
        if accion == "1" and len(year_entry.get()) >= 4:  # Si se inserta y ya hay 4 dígitos
            return False                    # Rechazar entrada
        return texto.isdigit() or texto == ""  # Aceptar solo dígitos o vacío

    # -------------------------------------------------------
    # Función: validar mes (máximo 2 dígitos)
    # -------------------------------------------------------
    def validar_month(texto, accion):
        """
        Valida que el mes no exceda 2 dígitos.
        accion = "1" cuando se inserta texto, "0" cuando se borra
        """
        if accion == "1" and len(month_entry.get()) >= 2:  # Si se inserta y ya hay 2 dígitos
            return False                    # Rechazar entrada
        return texto.isdigit() or texto == ""  # Aceptar solo dígitos o vacío

    # -------------------------------------------------------
    # Función: ejecutar creación de estructura en todos los vendors
    # -------------------------------------------------------
    def ejecutar_creacion():
        """
        Obtiene año y mes ingresados y crea la estructura para todos los vendors.
        """
        year_text = year_entry.get().strip()  # Obtener texto del año y quitar espacios
        month_text = month_entry.get().strip()  # Obtener texto del mes y quitar espacios
        
        if not year_text or not month_text:  # Verificar si alguno está vacío
            tk.messagebox.showerror("Error", "Por favor, ingrese tanto el año como el mes.")
            return
        
        if len(year_text) != 4:  # Verificar que el año tenga exactamente 4 dígitos
            tk.messagebox.showerror("Error", "El año debe tener exactamente 4 dígitos.")
            return
        
        try:
            year = int(year_text)  # Convertir año a entero
            month = int(month_text)  # Convertir mes a entero
        except ValueError:
            tk.messagebox.showerror("Error", "El año y el mes deben ser números válidos.")
            return
        
        messages = manager.update_all_vendors_month(year, month)  # Ejecutar creación en todos los vendors y obtener mensajes
        output = "\n".join(messages)  # Unir mensajes en una cadena
        tk.messagebox.showinfo("Resultado de la creación", output)  # Mostrar mensaje emergente

    # -------------------------------------------------------
    # BOTÓN VOLVER (fila superior izquierda)
    # -------------------------------------------------------
    back_btn = tk.Button(
        win,
        text="⬅ Volver",
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        borderwidth=0,
        font=("Segoe UI", 12, "bold"),
        cursor="hand2",
        command=volver                      # Asociar la acción de volver
    )
    back_btn.pack(anchor="nw", padx=10, pady=10)  # Posicionar en la esquina superior izquierda

    # -------------------------------------------------------
    # TÍTULO PRINCIPAL (encabezado)
    # -------------------------------------------------------
    title_label = tk.Label(
        win,
        text="Crear estructura de nuevo año y mes",
        font=("Segoe UI", 22, "bold"),
        bg=COLOR_BG,
        fg=COLOR_TEXT
    )
    title_label.pack(pady=20)              # Separación vertical bajo el título

    # -------------------------------------------------------
    # LABEL Y INPUT PARA AÑO
    # -------------------------------------------------------
    year_label = tk.Label(
        win,
        text="Año por crear",
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        font=("Segoe UI", 12)
    )
    year_label.pack()                      # Mostrar etiqueta

    year_entry = tk.Entry(
        win,
        validate="key",
        validatecommand=(win.register(validar_year), "%S", "%d"),  # Asociar validación de año
        font=("Segoe UI", 14),
        width=20,
        bg="#F7F9FC",
        fg=COLOR_TEXT,
        relief="solid",
        bd=1,
        justify="center"
    )
    year_entry.pack(pady=5)                # Espaciado alrededor del entry

    # -------------------------------------------------------
    # LABEL Y INPUT PARA MES
    # -------------------------------------------------------
    month_label = tk.Label(
        win,
        text="Mes por crear",
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        font=("Segoe UI", 12)
    )
    month_label.pack()                     # Mostrar etiqueta

    month_entry = tk.Entry(
        win,
        validate="key",
        validatecommand=(win.register(validar_month), "%S", "%d"),  # Asociar validación de mes
        font=("Segoe UI", 14),
        width=20,
        bg="#F7F9FC",
        fg=COLOR_TEXT,
        relief="solid",
        bd=1,
        justify="center"
    )
    month_entry.pack(pady=5)               # Espaciado alrededor del entry

    # -------------------------------------------------------
    # BOTÓN CREAR: valida inputs y crea estructura en todos los vendors
    # -------------------------------------------------------
    create_btn = tk.Button(
        win,
        text="Crear",
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground=COLOR_ACCENT,
        activeforeground="white",
        font=("Segoe UI", 14, "bold"),
        bd=0,
        cursor="hand2",
        width=20,
        height=2,
        relief="solid",
        borderwidth=2,
        command=ejecutar_creacion          # Asociar la acción de creación
    )
    create_btn.pack(pady=30)               # Separación vertical antes del botón

    # -------------------------------------------------------
    # CONTENEDOR Y WIDGET DE CONSOLA (salida stdout/stderr)
    # -------------------------------------------------------
    console_frame = tk.Frame(
        win,
        bg=COLOR_ACCENT,
        bd=2,
        relief="flat"
    )
    console_frame.pack(pady=5, padx=20)    # Margen alrededor del contenedor de consola

    console_text = tk.Text(
        console_frame,
        height=9,                         # Más líneas visibles
        width=60,                          # Ancho del widget de consola
        state="disabled",                  # Inicio en solo lectura
        bg="#F0F4F8",
        fg=COLOR_TEXT,
        relief="flat",
        font=("Consolas", 11),
        padx=5,                            # Padding interno horizontal
        pady=5                             # Padding interno vertical
    )
    console_text.pack()                    # Empaquetar el Text dentro del frame

    # -------------------------------------------------------
    # Redirigir stdout y stderr al widget de consola
    # -------------------------------------------------------
    sys.stdout = ConsoleRedirect(console_text)   # Mostrar prints en la interfaz
    sys.stderr = ConsoleRedirect(console_text)   # Mostrar errores también en la interfaz