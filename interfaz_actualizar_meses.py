import tkinter as tk
from classes import ManagerVendors
import sys
from classes import ConsoleRedirect

# --- PALETA TIPO OPEN ENGLISH ---
COLOR_BG = "#FFFFFF"
COLOR_PRIMARY = "#007BFF"
COLOR_ACCENT = "#00A3E0"
COLOR_TEXT = "#003B5C"

def open_update_months(root):
    win = tk.Toplevel(root)
    manager = ManagerVendors()
    win.title("Crear estructura de nuevo año y mes")
    win.geometry("600x500")
    win.configure(bg=COLOR_BG)

    

    # Función para validar que solo se escriban números
    def validar_numero(texto):
        return texto.isdigit() or texto == ""
    
    def validar_year(texto, accion):
        # accion == 1 → intento de insertar
        if accion == "1" and len(year_entry.get()) >= 4:
            return False
        return texto.isdigit() or texto == ""

    def validar_month(texto, accion):
        if accion == "1" and len(month_entry.get()) >= 2:
            return False
        return texto.isdigit() or texto == ""


    validar_cmd = win.register(validar_numero)

    def volver():
        win.destroy()
        root.deiconify()

    def ejecutar_creacion():
        year = int(year_entry.get())
        month = int(month_entry.get())
        manager.update_all_vendors_month(year, month)


    # -------------------------
    # BOTÓN VOLVER (sin acción aún)
    # -------------------------
    back_btn = tk.Button(
        win,
        text="⬅ Volver",
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        borderwidth=0,
        font=("Segoe UI", 12, "bold"),
        cursor="hand2",
        command=volver
    )

    back_btn.pack(anchor="nw", padx=10, pady=10)

    # -------------------------
    # TÍTULO
    # -------------------------
    title_label = tk.Label(
        win,
        text="Crear estructura de nuevo año y mes",
        font=("Segoe UI", 22, "bold"),
        bg=COLOR_BG,
        fg=COLOR_TEXT
    )
    title_label.pack(pady=20)

    # -------------------------
    # INPUT PARA AÑO
    # -------------------------
    year_label = tk.Label(
        win, text="Año por crear",
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        font=("Segoe UI", 12)
    )

    year_label.pack()

    year_entry = tk.Entry(
        win,
        validate="key",
        validatecommand=(win.register(validar_year), "%S", "%d"),
        font=("Segoe UI", 14),
        width=20,
        bg="#F7F9FC",
        fg=COLOR_TEXT,
        relief="solid",
        bd=1,
        justify="center"
    )
    year_entry.pack(pady=5)

    # -------------------------
    # INPUT PARA MES
    # -------------------------
    month_label = tk.Label(
        win, text="Mes por crear",
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        font=("Segoe UI", 12)
    )

    month_label.pack()

    month_entry = tk.Entry(
        win,
        validate="key",
        validatecommand=(win.register(validar_month), "%S", "%d"),
        font=("Segoe UI", 14),
        width=20,
        bg="#F7F9FC",
        fg=COLOR_TEXT,
        relief="solid",
        bd=1,
        justify="center"
    )
    month_entry.pack(pady=5)

    # -------------------------
    # BOTÓN CREAR (sin funcionalidad aún)
    # -------------------------
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
        command=ejecutar_creacion
    )
    create_btn.pack(pady=30)

    console_frame = tk.Frame(win, bg=COLOR_ACCENT, bd=2, relief="flat")
    console_frame.pack(pady=5, padx=20)

    console_text = tk.Text(
        console_frame,
        height=15,       # Más líneas visibles
        width=60,        # Un poco menos ancho
        state="disabled",
        bg="#F0F4F8",
        fg=COLOR_TEXT,
        relief="flat",
        font=("Consolas", 11),
        padx=5,
        pady=5
    )
    console_text.pack()

    sys.stdout = ConsoleRedirect(console_text)
    sys.stderr = ConsoleRedirect(console_text)