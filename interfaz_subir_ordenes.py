import tkinter as tk
from tkinter import messagebox
import os

# IMPORTAMOS LA CLASE
from classes import ManagerVendors

def only_numbers(char):
    return char.isdigit()

VENDOR_PATH = r"G:\Unidades compartidas\Vendor_files"

# Lista para guardar vendors seleccionados
selected_vendors = []

# Diccionario para guardar referencia a los botones
vendor_buttons = {}

# CREAMOS LA INSTANCIA
manager = ManagerVendors()


def open_vendor(name):
    """
    Alterna la selección del vendor: seleccionar / deseleccionar.
    """
    btn = vendor_buttons.get(name)

    if name in selected_vendors:
        # Deseleccionar
        selected_vendors.remove(name)
        if btn:
            btn.config(bg="#d1d1d1")   # color original
    else:
        # Seleccionar
        selected_vendors.append(name)
        if btn:
            btn.config(bg="#87CEFA")   # azul claro


def load_vendor_buttons(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    vendor_buttons.clear()

    if not os.path.exists(VENDOR_PATH):
        os.makedirs(VENDOR_PATH)

    folders = [
        f for f in os.listdir(VENDOR_PATH)
        if os.path.isdir(os.path.join(VENDOR_PATH, f))
    ]

    col = 0
    row = 0

    for folder in folders:
        btn = tk.Button(
            frame,
            text=folder,
            width=25,
            height=2,
            bg="#d1d1d1",
            command=lambda f=folder: open_vendor(f)
        )
        btn.grid(row=row, column=col, padx=10, pady=10)

        vendor_buttons[folder] = btn

        col += 1
        if col > 1:
            col = 0
            row += 1



def open_upload_orders(root):
    win = tk.Toplevel(root)
    win.title("Subir Órdenes")
    win.geometry("600x650")

    def volver():
        win.destroy()
        root.deiconify()


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

    # -------------------------------------------------------
    # SECCIÓN SUPERIOR
    # -------------------------------------------------------
    top_frame = tk.Frame(win)
    top_frame.pack(pady=10)

    # Año
    tk.Label(top_frame, text="Año:").grid(row=0, column=0, padx=5)
    vcmd = (win.register(only_numbers), "%S")

    entry_year = tk.Entry(
        top_frame, width=10,
        validate="key", validatecommand=vcmd
    )
    entry_year.grid(row=0, column=1, padx=5)

    # Mes
    tk.Label(top_frame, text="Mes:").grid(row=0, column=2, padx=5)
    entry_month = tk.Entry(
        top_frame, width=10,
        validate="key", validatecommand=vcmd
    )
    entry_month.grid(row=0, column=3, padx=5)

    # Tipo OE / OE JR
    tk.Label(top_frame, text="Tipo:").grid(row=0, column=4, padx=5)

    selected_type = tk.StringVar()
    selected_type.set("")   # dejar vacío al inicio

    dropdown = tk.OptionMenu(top_frame, selected_type, "OE", "OE JR")
    dropdown.grid(row=0, column=5, padx=5)

    # -------------------------------------------------------
    # CARGAR VENDORS (SIN CAMBIOS)
    # -------------------------------------------------------
    button_frame = tk.Frame(win)
    button_frame.pack(pady=20)

    load_vendor_buttons(button_frame)

    # ------------------ Checkbox "Seleccionar todos" ------------------
    select_all_var = tk.BooleanVar()
    def select_all_vendors():
        if select_all_var.get():  # Si está marcado
            for name in vendor_buttons:
                if name not in selected_vendors:
                    selected_vendors.append(name)
                    vendor_buttons[name].config(bg="#87CEFA")
        else:  # Si se desmarca
            for name in vendor_buttons:
                if name in selected_vendors:
                    selected_vendors.remove(name)
                    vendor_buttons[name].config(bg="#d1d1d1")

    tk.Checkbutton(
        win,
        text="select all",
        variable=select_all_var,
        command=select_all_vendors,
        anchor="e",          # mantiene la alineación a la derecha
        padx=20,
        justify="left"      # texto a la derecha del contenido
    ).pack(anchor="e", padx=20)

    # -------------------------------------------------------
    # NUEVA FUNCIÓN PARA EJECUTAR EL MÉTODO
    # -------------------------------------------------------
    def upload_orders():
        # Validaciones
        if not entry_year.get():
            messagebox.showerror("Error", "Falta el dato: Año")
            return

        if not entry_month.get():
            messagebox.showerror("Error", "Falta el dato: Mes")
            return

        if not selected_type.get():
            messagebox.showerror("Error", "Falta el dato: Tipo (OE / OE JR)")
            return

        if not selected_vendors:
            messagebox.showerror("Error", "Debe seleccionar al menos un vendor.")
            return

        # Convertir a entero después de validar
        year = int(entry_year.get())
        month = int(entry_month.get())
        tipo = selected_type.get()
        vendors = selected_vendors

        # Ejecutar método
        manager.copy_latest_orders_batch(vendors, tipo, year, month)

        # Mensaje de éxito
        messagebox.showinfo("Éxito", "Las órdenes se subieron correctamente.")

    # -------------------------------------------------------
    # NUEVO BOTÓN: "SUBIR ÓRDENES"
    # -------------------------------------------------------
    tk.Button(
        win,
        text="Subir órdenes",
        command=upload_orders  # AHORA EJECUTA TU MÉTODO
    ).pack(pady=10)