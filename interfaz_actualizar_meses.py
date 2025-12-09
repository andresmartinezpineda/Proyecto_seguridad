import tkinter as tk
from classes import ManagerVendors


def open_update_months(root):
    win = tk.Toplevel(root)
    manager = ManagerVendors()
    win.title("Crear estructura de nuevo año y mes")
    win.geometry("500x400")
    win.configure(bg="white")

    # Función para validar que solo se escriban números
    def validar_numero(texto):
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
        bg="white",
        fg="black",
        borderwidth=0,
        font=("Arial", 12, "bold"),
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
        font=("Arial", 18, "bold"),
        bg="white"
    )
    title_label.pack(pady=20)

    # -------------------------
    # INPUT PARA AÑO
    # -------------------------
    year_label = tk.Label(
        win, text="Año por crear", bg="white",
        font=("Arial", 12)
    )
    year_label.pack()

    year_entry = tk.Entry(
        win,
        validate="key",
        validatecommand=(validar_cmd, "%P"),
        font=("Arial", 14),
        width=20
    )
    year_entry.pack(pady=5)

    # -------------------------
    # INPUT PARA MES
    # -------------------------
    month_label = tk.Label(
        win, text="Mes por crear", bg="white",
        font=("Arial", 12)
    )
    month_label.pack()

    month_entry = tk.Entry(
        win,
        validate="key",
        validatecommand=(validar_cmd, "%P"),
        font=("Arial", 14),
        width=20
    )
    month_entry.pack(pady=5)

    # -------------------------
    # BOTÓN CREAR (sin funcionalidad aún)
    # -------------------------
    create_btn = tk.Button(
        win,
        text="Crear",
        bg="#C0BFBF",
        fg="black",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        relief="solid",
        borderwidth=2,
        command=ejecutar_creacion
    )
    create_btn.pack(pady=30)