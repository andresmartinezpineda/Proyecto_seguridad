import tkinter as tk                    # Crear interfaces gráficas con Tkinter
import sys                              # Redirigir stdout/stderr hacia widget de consola
from tkinter import messagebox          # Mostrar diálogos de error / info
from classes import Vendor              # Clase Vendor para crear estructura en disco
from classes import ConsoleRedirect     # Redirector para mostrar salida en widget Text


# ---------------------------------------------------------
# Paleta de colores usada en la interfaz
# ---------------------------------------------------------
COLOR_BG = "#FFFFFF"                    # Color de fondo de la ventana
COLOR_PRIMARY = "#007BFF"               # Color principal (botón Crear)
COLOR_ACCENT = "#00A3E0"                # Color activo para botones
COLOR_TEXT = "#003B5C"                  # Color del texto principal


def create_vendor_window(root):
    """
    Abre ventana secundaria para crear un nuevo vendor.
    - root: ventana principal para retornar cuando se cierre esta ventana.
    """
    # -------------------------------------------------------
    # VENTANA PRINCIPAL (hija)
    # -------------------------------------------------------
    win = tk.Toplevel(root)               # Crear ventana hija sobre root
    win.title("Crear nuevo vendor")        # Título de la ventana
    win.geometry("600x500")               # Dimensiones fijas
    win.resizable(False, False)           # No permitir redimensionar
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
        text="Crear nuevo vendor",
        font=("Segoe UI", 22, "bold"),
        bg=COLOR_BG,
        fg=COLOR_TEXT
    )
    title_label.pack(pady=20)              # Separación vertical bajo el título

    # -------------------------------------------------------
    # INPUT PARA NOMBRE DEL VENDOR (con placeholder)
    # -------------------------------------------------------
    entry_name = tk.Entry(
        win,
        width=40,
        font=("Segoe UI", 12),
        justify="center",
        bg="#F7F9FC",
        fg="grey",
        relief="solid",
        bd=1
    )
    entry_name.pack(pady=5, ipady=5)       # Espaciado alrededor del entry

    # -------------------------------------------------------
    # Comportamiento del placeholder dentro del Entry
    # -------------------------------------------------------
    def on_entry_click(event):
        """
        Al enfocar el input: si contiene el placeholder, limpiarlo y poner texto en negro.
        """
        if entry_name.get() == "Ingresa el nombre del vendor":
            entry_name.delete(0, "end")
            entry_name.config(fg="black")

    def on_focusout(event):
        """
        Al perder foco: si está vacío, restaurar placeholder y color gris.
        """
        if entry_name.get() == "":
            entry_name.insert(0, "Ingresa el nombre del vendor")
            entry_name.config(fg="grey")

    # Inicializar placeholder y bind de eventos
    entry_name.insert(0, "Ingresa el nombre del vendor")  # Texto inicial tipo placeholder
    entry_name.config(fg="grey")                          # Color del placeholder
    entry_name.bind("<FocusIn>", on_entry_click)          # Evento foco in
    entry_name.bind("<FocusOut>", on_focusout)            # Evento foco out

    # -------------------------------------------------------
    # TEXTO INFORMATIVO (recordatorio sobre nombre)
    # -------------------------------------------------------
    reminder_label = tk.Label(
        win,
        text="Recuerda: El nombre del vendor debe ser exactamente\n igual al nombre que tienen las ordenes",
        fg="red",
        bg=COLOR_BG,
        font=("Arial", 10)
    )
    reminder_label.pack(pady=10)            # Mostrar advertencia en rojo


    # -------------------------------------------------------
    # BOTÓN CREAR: valida input y crea vendor en disco
    # -------------------------------------------------------
    def crear_vendor():
        """
        Toma el nombre ingresado, valida y crea la estructura del vendor usando Vendor.update_structure().
        Actualiza el placeholder tras la creación.
        """
        name = entry_name.get()             # Obtener texto del Entry

        # Validación básica: no aceptar vacío ni placeholder
        if not name or name == "Ingresa el nombre del vendor":
            messagebox.showerror("Error", "Por favor ingresa un nombre válido para el vendor.")
            return

        # -------------------------------
        # Crear instancia temporal de Vendor y ejecutar creación
        # -------------------------------
        temp_vendor = Vendor(name)          # Instanciar Vendor con el nombre ingresado
        temp_vendor.update_structure()      # Crear carpetas: vendor, año y mes según implementación de Vendor

        # -------------------------------
        # Restaurar placeholder y estado del Entry
        # -------------------------------
        entry_name.delete(0, "end")         # Limpiar contenido del input
        entry_name.insert(0, "Ingresa el nombre del vendor")  # Restaurar placeholder
        entry_name.config(fg="grey")        # Poner color gris en placeholder


    # Botón físico que ejecuta crear_vendor()
    crear_btn = tk.Button(
        win,
        text="CREAR",
        font=("Segoe UI", 12, "bold"),
        width=20,
        height=2,
        bg=COLOR_PRIMARY,
        fg="white",
        activebackground=COLOR_ACCENT,
        activeforeground="white",
        cursor="hand2",
        bd=0,
        command=crear_vendor
    )
    crear_btn.pack(pady=20)                # Separación vertical antes del botón


    # -------------------------------------------------------
    # CONTENEDOR Y WIDGET DE CONSOLA (salida stdout/stderr)
    # -------------------------------------------------------
    console_frame = tk.Frame(
        win,
        bg=COLOR_BG,
        highlightbackground=COLOR_PRIMARY,
        highlightthickness=2,
        bd=0
    )
    console_frame.pack(pady=5, padx=20)    # Margen alrededor del contenedor de consola

    console_text = tk.Text(
        console_frame,
        height=15,
        width=60,
        state="disabled",                   # Inicio en solo lectura
        bg="#F0F4F8",
        fg=COLOR_TEXT,
        font=("Consolas", 11),
        relief="solid",
        bd=1,
        padx=5,
        pady=5
    )
    console_text.pack()                    # Empaquetar el Text dentro del frame

    # -------------------------------------------------------
    # Redirigir stdout y stderr al widget de consola
    # -------------------------------------------------------
    sys.stdout = ConsoleRedirect(console_text)   # Mostrar prints en la interfaz
    sys.stderr = ConsoleRedirect(console_text)   # Mostrar errores también en la interfaz