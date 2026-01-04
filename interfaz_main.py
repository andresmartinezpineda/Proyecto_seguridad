import os
import subprocess
import tkinter as tk                    # Crear interfaces gráficas con Tkinter
from interfaz_subir_ordenes import open_upload_orders  # Función para abrir ventana de subir órdenes
from interfaz_crear_vendor import create_vendor_window  # Función para abrir ventana de crear vendor
from interfaz_actualizar_meses import open_update_months  # Función para abrir ventana de actualizar meses


def open_main_panel():
    """
    Abre la ventana principal de la aplicación.
    """
    # -------------------------------------------------------
    # VENTANA PRINCIPAL
    # -------------------------------------------------------
    root = tk.Tk()                          # Crear ventana raíz
    root.title("Panel Principal")            # Título de la ventana
    root.geometry("600x450")                 # Dimensiones de la ventana
    root.configure(bg="#F5F5F5")             # Aplicar color de fondo (gris claro moderno)

    # -------------------------------------------------------
    # FRAME CONTENEDOR PRINCIPAL
    # -------------------------------------------------------
    frame = tk.Frame(root, bg="#F5F5F5")    # Crear frame con mismo color de fondo
    frame.pack(expand=True)                  # Empaquetar y expandir

    # -------------------------------------------------------
    # Función: cambiar color al pasar el mouse (efecto hover)
    # -------------------------------------------------------
    def on_enter(e):
        """
        Al pasar el mouse sobre un botón: cambiar a azul más oscuro.
        e = evento de mouse
        """
        e.widget['bg'] = "#005A9E"           # Cambiar a azul más oscuro

    # -------------------------------------------------------
    # Función: restaurar color original al salir del mouse
    # -------------------------------------------------------
    def on_leave(e):
        """
        Al salir el mouse del botón: restaurar color original.
        e = evento de mouse
        """
        e.widget['bg'] = "#0072CE"           # Restaurar a azul Open English

    # -------------------------------------------------------
    # Función: abrir archivo de configuración (settings.xlsx)
    # -------------------------------------------------------
    def open_settings_excel():
        """
        Abre el archivo config/settings.xlsx del aplicativo.
        """
        try:
            # Obtener la ruta base del aplicativo (directorio del archivo actual)
            base_path = os.path.dirname(os.path.abspath(__file__))

            # Construir la ruta a la carpeta config
            config_path = os.path.join(base_path, "config")

            # Construir la ruta completa al archivo settings.xlsx
            settings_file = os.path.join(config_path, "settings.xlsx")

            # Validar que el archivo existe
            if not os.path.exists(settings_file):
                tk.messagebox.showerror(
                    "Error",                 # Título del cuadro de diálogo
                    "No se encontró el archivo settings.xlsx en la carpeta config."  # Mensaje de error
                )
                return

            # Abrir el archivo con el programa por defecto del sistema (Excel)
            subprocess.Popen(["start", settings_file], shell=True)

        except Exception as e:
            tk.messagebox.showerror(
                "Error",                     # Título del cuadro de diálogo
                f"No se pudo abrir el archivo de configuración.\n\n{e}"  # Mensaje de error con detalles
            )


    # -------------------------------------------------------
    # TÍTULO PRINCIPAL
    # -------------------------------------------------------
    title_label = tk.Label(
        frame,
        text="PANEL PRINCIPAL",              # Texto del título
        bg="#F5F5F5",                        # Color de fondo
        fg="#0072CE",                        # Color de texto (azul)
        font=("Segoe UI", 25, "bold")        # Fuente grande y bold
    )
    title_label.pack(pady=(30, 10))          # Espaciado vertical (30 arriba, 10 abajo)


    # -------------------------------------------------------
    # ESTILOS COMPARTIDOS PARA BOTONES
    # -------------------------------------------------------
    button_style = {
        "width": 30,                         # Ancho del botón
        "height": 2,                         # Alto del botón
        "bg": "#0072CE",                     # Color de fondo (Azul Open English)
        "fg": "white",                       # Color del texto
        "activebackground": "#005A9E",       # Tono más oscuro al pulsar
        "activeforeground": "white",         # Texto blanco al pulsar
        "borderwidth": 0,                    # Sin bordes para look moderno
        "relief": "flat",                    # Estilo plano
        "font": ("Segoe UI", 14, "bold"),    # Fuente moderna y bold
        "cursor": "hand2"                    # Cursor de mano al pasar
    }

    # -------------------------------------------------------
    # BOTÓN 1: SUBIR ORDENES
    # -------------------------------------------------------
    btn_upload = tk.Button(
        frame,
        text="SUBIR ORDENES",                # Texto del botón
        command=lambda: (open_upload_orders(root), root.withdraw()),  # Abrir ventana y ocultar principal
        **button_style                       # Aplicar estilos compartidos
    )
    btn_upload.pack(pady=15)                 # Espaciado vertical
    btn_upload.bind("<Enter>", on_enter)    # Bind: efecto al pasar mouse
    btn_upload.bind("<Leave>", on_leave)    # Bind: efecto al salir mouse

    # -------------------------------------------------------
    # BOTÓN 2: CREAR VENDOR
    # -------------------------------------------------------
    btn_upload = tk.Button(
        frame,
        text="CREAR VENDOR",                 # Texto del botón
        command=lambda: (create_vendor_window(root), root.withdraw()),  # Abrir ventana y ocultar principal
        **button_style                       # Aplicar estilos compartidos
    )
    btn_upload.pack(pady=15)                 # Espaciado vertical
    btn_upload.bind("<Enter>", on_enter)    # Bind: efecto al pasar mouse
    btn_upload.bind("<Leave>", on_leave)    # Bind: efecto al salir mouse

    # -------------------------------------------------------
    # BOTÓN 3: ACTUALIZAR MESES
    # -------------------------------------------------------
    btn_upload = tk.Button(
        frame,
        text="ACTUALIZAR MESES",             # Texto del botón
        command=lambda: (open_update_months(root), root.withdraw()),  # Abrir ventana y ocultar principal
        **button_style                       # Aplicar estilos compartidos
    )
    btn_upload.pack(pady=15)                 # Espaciado vertical
    btn_upload.bind("<Enter>", on_enter)    # Bind: efecto al pasar mouse
    btn_upload.bind("<Leave>", on_leave)    # Bind: efecto al salir mouse

    # -------------------------------------------------------
    # BOTÓN CONFIGURACIÓN (INFERIOR DERECHA)
    # -------------------------------------------------------
    btn_settings = tk.Button(
        root,                                # Ventana raíz como contenedor
        text="🔀 Rutas",                     # Texto del botón
        command=open_settings_excel,         # Comando: abrir archivo settings.xlsx
        bg="#FF8533",                        # Color de fondo (naranja)
        fg="#333333",                        # Color del texto (gris oscuro)
        activebackground="#CCCCCC",          # Fondo al hacer clic (gris claro)
        activeforeground="#000000",          # Texto al hacer clic (negro)
        borderwidth=0,                       # Sin bordes
        relief="flat",                       # Estilo plano
        font=("Segoe UI", 12, "bold"),       # Fuente moderna
        padx=10,                             # Espaciado horizontal
        pady=6,                              # Espaciado vertical
        cursor="hand2"                       # Cursor de mano
    )

    # Posicionar el botón en la esquina inferior derecha
    btn_settings.place(
        relx=1.0,                            # Alineado a la derecha (100%)
        rely=1.0,                            # Alineado abajo (100%)
        anchor="se",                         # Ancla en esquina inferior derecha
        x=-15,                               # Offset horizontal (-15 píxeles)
        y=-15                                # Offset vertical (-15 píxeles)
    )

    # -------------------------------------------------------
    # INICIAR LOOP PRINCIPAL
    # -------------------------------------------------------
    root.mainloop()                          # Mostrar ventana y esperar interacciones del usuario