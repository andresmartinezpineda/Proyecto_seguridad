import tkinter as tk                    # crear interfaces gráficas
from tkinter import messagebox          # mostrar ventanas de diálogo (error, info, etc.)
import os                               # operaciones de sistema de archivos

# Importar la clase ManagerVendors para ejecutar procesos de copia
from classes import ManagerVendors

# ---------------------------------------------------------
# Función para validar entrada de solo números
# ---------------------------------------------------------
def only_numbers(char):
    """
    Valida que el carácter ingresado sea un número.
    """
    return char.isdigit()               # Devuelve True si char es dígito


# ---------------------------------------------------------
# Constantes y variables globales
# ---------------------------------------------------------
VENDOR_PATH = r"G:\Unidades compartidas\Vendor_files"  # Ruta base donde están los vendors

selected_vendors = []                   # Lista para guardar vendors seleccionados

vendor_buttons = {}                     # Diccionario para guardar referencia a los botones

manager = ManagerVendors()              # Instancia de ManagerVendors para ejecutar métodos


# ---------------------------------------------------------
# Función para alternar selección de vendor
# ---------------------------------------------------------
def open_vendor(name):
    """
    Alterna la selección del vendor: seleccionar / deseleccionar.
    """
    btn = vendor_buttons.get(name)      # Obtener referencia al botón del vendor

    if name in selected_vendors:        # Si el vendor ya está seleccionado
        selected_vendors.remove(name)   # Removarlo de la lista
        if btn:
            btn.config(bg="#d1d1d1")   # Restaurar color original (gris)
    else:                               # Si no está seleccionado
        selected_vendors.append(name)   # Agregarlo a la lista
        if btn:
            btn.config(bg="#87CEFA")   # Cambiar color a azul claro


# ---------------------------------------------------------
# Función para cargar botones de vendors
# ---------------------------------------------------------
def load_vendor_buttons(frame):
    """
    Carga dinámicamente los botones de vendors desde el sistema de archivos.
    """
    # Eliminar widgets existentes en el frame para refrescar la lista
    for widget in frame.winfo_children():   # Iterar sobre widgets existentes
        widget.destroy()                    # Eliminar cada widget (botones anteriores)

    # Limpiar el diccionario que almacena referencias a los botones
    vendor_buttons.clear()

    # Asegurar que exista la ruta base de vendors; si no existe, crearla
    if not os.path.exists(VENDOR_PATH):     # Verificar existencia de carpeta
        os.makedirs(VENDOR_PATH)            # Crear carpeta base de vendors

    # Obtener solo los nombres de carpetas dentro de VENDOR_PATH (cada carpeta = un vendor)
    folders = [
        f for f in os.listdir(VENDOR_PATH)
        if os.path.isdir(os.path.join(VENDOR_PATH, f))
    ]

    # Inicializar índices de posición para la grilla (2 columnas)
    col = 0
    row = 0

    # Configurar las dos columnas del grid para que puedan expandirse y centrar contenido
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Crear un botón por cada carpeta (vendor) encontrada
    for folder in folders:
        # Construir el widget Button con texto y estilo
        btn = tk.Button(
            frame,
            text=folder,                    # Texto visible en el botón (nombre del vendor)
            width=30,                       # Ancho del botón en caracteres
            height=2,                       # Altura del botón en líneas
            bg="#d1d1d1",                 # Color de fondo por defecto
            font=("Segoe UI", 10),        # Fuente del texto
            relief="raised",              # Estilo de borde
            bd=1,                           # Grosor del borde
            command=lambda f=folder: open_vendor(f)  # Acción al hacer click: alternar selección
        )

        # Posicionar el botón en la grilla con un pequeño padding
        btn.grid(row=row, column=col, padx=8, pady=6)

        # Guardar referencia al botón en el diccionario para poder cambiar color/estado luego
        vendor_buttons[folder] = btn

        # Avanzar a la siguiente columna; si se superan 2 columnas, volver a la primera y avanzar fila
        col += 1
        if col > 1:
            col = 0
            row += 1


# ---------------------------------------------------------
# Función principal para abrir ventana de subir órdenes
# --------------------------------------------------------- 
def open_upload_orders(root):
    """
    Abre la ventana para subir órdenes de insertion orders.
    Permite seleccionar vendors, año, mes y tipo de orden.
    """
    # Resetear la lista de vendors seleccionados al abrir la ventana
    selected_vendors.clear()

    win = tk.Toplevel(root)                 # Crear ventana secundaria

    # Definir paleta de colores
    COLOR_PRIMARY = "#0072CE"               # Azul oficial
    COLOR_PRIMARY_LIGHT = "#4DA3FF"         # Azul claro
    COLOR_BG = "#FFFFFF"                    # Blanco
    COLOR_GRAY = "#F2F2F2"                  # Gris suave
    COLOR_TEXT = "#000000"                  # Negro

    win.configure(bg=COLOR_BG)              # Aplicar color de fondo
    win.title("Subir Órdenes")              # Título de ventana
    win.geometry("600x650")                 # Tamaño de ventana

    # ---------------------------------------------------------
    # Función: volver a ventana anterior
    # ---------------------------------------------------------
    def volver():
        """
        Cierra la ventana actual y muestra la ventana principal.
        """
        win.destroy()                       # Destruir ventana secundaria
        root.deiconify()                    # Mostrar ventana principal

    # ---------------------------------------------------------
    # Función: validar año (máximo 4 dígitos)
    # ---------------------------------------------------------
    def validar_year(texto, accion):
        """
        Valida que el año no exceda 4 dígitos.
        accion = "1" cuando se inserta texto, "0" cuando se borra
        """
        if accion == "1" and len(entry_year.get()) >= 4:  # Si se inserta y ya hay 4 dígitos
            return False                    # Rechazar entrada
        return texto.isdigit()              # Aceptar solo dígitos

    # ---------------------------------------------------------
    # Función: validar mes (máximo 2 dígitos)
    # ---------------------------------------------------------
    def validar_month(texto, accion):
        """
        Valida que el mes no exceda 2 dígitos.
        accion = "1" cuando se inserta texto, "0" cuando se borra
        """
        if accion == "1" and len(entry_month.get()) >= 2:  # Si se inserta y ya hay 2 dígitos
            return False                    # Rechazar entrada
        return texto.isdigit()              # Aceptar solo dígitos

    # ---------------------------------------------------------
    # Botón volver
    # ---------------------------------------------------------
    back_btn = tk.Button(
        win,
        text="⬅ Volver",
        bg=COLOR_BG,
        fg=COLOR_PRIMARY,
        activeforeground=COLOR_PRIMARY_LIGHT,
        activebackground=COLOR_BG,
        borderwidth=0,
        font=("Segoe UI", 12, "bold"),
        cursor="hand2",
        command=volver
    )
    back_btn.pack(anchor="nw", padx=10, pady=10)

    # ---------------------------------------------------------
    # Sección superior: Año, Mes, Tipo
    # ---------------------------------------------------------
    top_frame = tk.Frame(win, bg=COLOR_BG)  # Frame contenedor
    top_frame.pack(pady=10)

    # Campo Año
    tk.Label(top_frame, text="Año:", bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 11)).grid(row=0, column=0, padx=5)
    vcmd = (win.register(only_numbers), "%S")

    entry_year = tk.Entry(
        top_frame,
        width=10,
        bg=COLOR_GRAY,
        relief="flat",
        font=("Segoe UI", 11),
        justify="center",
        validate="key",
        validatecommand=(win.register(validar_year), "%S", "%d")
    )
    entry_year.grid(row=0, column=1, padx=5)

    # Campo Mes
    tk.Label(top_frame, text="Mes:", bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 11)).grid(row=0, column=2, padx=5)
    entry_month = tk.Entry(
        top_frame,
        width=10,
        bg=COLOR_GRAY,
        relief="flat",
        font=("Segoe UI", 11),
        justify="center",
        validate="key",
        validatecommand=(win.register(validar_month), "%S", "%d")
    )
    entry_month.grid(row=0, column=3, padx=5)

    # Dropdown Tipo (OE / OE JR)
    tk.Label(top_frame, bg=COLOR_BG, text="Tipo:").grid(row=0, column=4, padx=5)
    selected_type = tk.StringVar()          # Variable para guardar opción seleccionada
    selected_type.set("")                   # Iniciar vacío

    dropdown = tk.OptionMenu(top_frame, selected_type, "OE", "OE JR")  # Crear dropdown con opciones
    dropdown.config(
        bg=COLOR_GRAY,
        fg=COLOR_TEXT,
        font=("Segoe UI", 10),
        relief="flat",
        highlightthickness=0,
        activebackground=COLOR_PRIMARY_LIGHT
    )
    dropdown.grid(row=0, column=5, padx=5)

    # ---------------------------------------------------------
    # Sección de carga de botones de vendors (scrollable)
    # ---------------------------------------------------------
    container = tk.Frame(win, bg=COLOR_BG)  # Contenedor que agrupa canvas y scrollbar
    container.pack(pady=20, fill="both", expand=True)  # Empaquetar con padding y permitir expansión

    canvas = tk.Canvas(container, bg=COLOR_BG, highlightthickness=0)  # Canvas que contendrá el frame interior

    vsb = tk.Scrollbar(container, orient="vertical", command=canvas.yview)  # Barra vertical ligada al canvas
    canvas.configure(yscrollcommand=vsb.set)  # Conectar scrollbar al canvas

    vsb.pack(side="right", fill="y")  # Mostrar scrollbar a la derecha
    canvas.pack(side="left", fill="both", expand=True)  # Mostrar canvas a la izquierda y expandir

    button_frame = tk.Frame(canvas, bg=COLOR_BG)  # Frame interior para los botones

    window_id = canvas.create_window((0, 0), window=button_frame, anchor="nw")  # Insertar frame interior en el canvas

    def _on_frame_config(event):  # Función que actualiza scrollregion cuando cambia el contenido
        canvas.configure(scrollregion=canvas.bbox("all"))  # Ajustar scrollregion al bounding box

    button_frame.bind("<Configure>", _on_frame_config)  # Asociar al evento Configure del frame interior

    def _on_canvas_config(event):  # Mantener el ancho del frame interior igual al ancho del canvas
        try:
            canvas.itemconfig(window_id, width=event.width)  # Actualizar ancho del objeto ventana insertado
        except Exception:
            pass  # Ignorar errores de reconfiguración

    canvas.bind("<Configure>", _on_canvas_config)  # Asociar al evento Configure del canvas

    def _on_mousewheel(event):  # Desplazar con la rueda del ratón (Windows)
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")  # Scroll vertical proporcional al delta

    button_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))  # Activar wheel binding al entrar
    button_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))  # Desactivar wheel binding al salir

    load_vendor_buttons(button_frame)  # Cargar botones dinámicamente en el frame interior

    # ---------------------------------------------------------
    # Checkbox "Seleccionar todos"
    # ---------------------------------------------------------
    select_all_var = tk.BooleanVar()        # Variable para estado del checkbox

    def select_all_vendors():
        """
        Selecciona o deselecciona todos los vendors según el estado del checkbox.
        """
        if select_all_var.get():            # Si checkbox está marcado
            for name in vendor_buttons:     # Iterar sobre todos los vendors
                if name not in selected_vendors:  # Si no está ya seleccionado
                    selected_vendors.append(name)  # Agregarlo
                    vendor_buttons[name].config(bg="#87CEFA")  # Cambiar color a azul
        else:                               # Si checkbox está desmarcado
            for name in vendor_buttons:     # Iterar sobre todos los vendors
                if name in selected_vendors:  # Si está seleccionado
                    selected_vendors.remove(name)  # Removarlo
                    vendor_buttons[name].config(bg="#d1d1d1")  # Restaurar color gris

    tk.Checkbutton(
        win,
        bg=COLOR_BG,
        fg=COLOR_PRIMARY,
        selectcolor=COLOR_GRAY,
        font=("Segoe UI", 11),
        text="select all",
        variable=select_all_var,
        command=select_all_vendors,
        anchor="e",                         # Alineación a la derecha
        padx=20,
        justify="left"                      # Texto a la derecha del contenido
    ).pack(anchor="e", padx=20)

    # ---------------------------------------------------------
    # Función para ejecutar proceso de subir órdenes
    # ---------------------------------------------------------
    def upload_orders():
        """
        Valida los datos ingresados y ejecuta el proceso de copia de órdenes.
        """        # Resetear la lista de vendors seleccionados al ejecutar el botón
        
        if not entry_year.get():            # Validar que año no esté vacío
            messagebox.showerror("Error", "Falta el dato: Año")
            return

        if len(entry_year.get()) != 4:      # Validar que año tenga exactamente 4 dígitos
            messagebox.showerror("Error", "El año debe tener 4 dígitos, intente de nuevo")
            return

        if not entry_month.get():           # Validar que mes no esté vacío
            messagebox.showerror("Error", "Falta el dato: Mes")
            return

        month_int = int(entry_month.get())  # Convertir a entero para validar rango
        if month_int < 1 or month_int > 12:  # Validar que mes esté entre 1 y 12
            messagebox.showerror("Error", "El mes solo puede ser del 1 al 12, intentalo de nuevo")
            return

        if not selected_type.get():         # Validar que tipo esté seleccionado
            messagebox.showerror("Error", "Falta el dato: Tipo (OE / OE JR)")
            return

        if not selected_vendors:            # Validar que al menos un vendor esté seleccionado
            messagebox.showerror("Error", "Debe seleccionar al menos un vendor.")
            return

        # Convertir datos a los tipos correctos
        year = int(entry_year.get())        # Convertir año a entero
        month = int(entry_month.get())      # Convertir mes a entero
        tipo = selected_type.get()          # Obtener tipo seleccionado
        vendors = selected_vendors          # Obtener lista de vendors seleccionados

        # Ejecutar el método del manager
        messages = manager.copy_latest_orders_batch(vendors, tipo, year, month)

        # Mostrar todos los mensajes en un solo messagebox
        full_message = "\n".join(messages)
        messagebox.showinfo("Resultado del Proceso", full_message)

        # Resetear la lista de vendors seleccionados y deseleccionar visualmente después de ejecutar el proceso
        selected_vendors.clear()
        for btn in vendor_buttons.values():
            btn.config(bg="#d1d1d1")
        select_all_var.set(False)

    # ---------------------------------------------------------
    # Botón principal: Subir órdenes
    # ---------------------------------------------------------
    tk.Button(
        win,
        text="Subir órdenes",
        command=upload_orders,
        bg=COLOR_PRIMARY,
        fg="white",
        font=("Segoe UI", 13, "bold"),
        activebackground=COLOR_PRIMARY_LIGHT,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        height=2,
        width=20
    ).pack(pady=15)