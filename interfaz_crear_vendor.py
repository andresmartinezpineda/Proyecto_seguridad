import tkinter as tk
import sys
from tkinter import messagebox
from classes import Vendor
from classes import ConsoleRedirect


def create_vendor_window(root):
    # -------------------------------------------------------
    # VENTANA PRINCIPAL
    # -------------------------------------------------------
    win = tk.Toplevel(root)  # Nueva ventana hija
    win.title("Crear nuevo vendor")
    win.geometry("600x500")
    win.resizable(False, False)

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
    # TÍTULO GRANDE ARRIBA
    # -------------------------------------------------------
    title_label = tk.Label(win, text="Crear nuevo vendor", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # -------------------------------------------------------
    # INPUT PARA NOMBRE DEL VENDOR CON PLACEHOLDER
    # -------------------------------------------------------
    entry_name = tk.Entry(win, width=40, font=("Arial", 12), justify="center")
    entry_name.pack(pady=5,ipady=5)

    # Función para placeholder
    def on_entry_click(event):
        if entry_name.get() == "Ingresa el nombre del vendor":
            entry_name.delete(0, "end")
            entry_name.config(fg="black")

    def on_focusout(event):
        if entry_name.get() == "":
            entry_name.insert(0, "Ingresa el nombre del vendor")
            entry_name.config(fg="grey")

    entry_name.insert(0, "Ingresa el nombre del vendor")
    entry_name.config(fg="grey")
    entry_name.bind("<FocusIn>", on_entry_click)
    entry_name.bind("<FocusOut>", on_focusout)

    # -------------------------------------------------------
    # TEXTO DE RECUERDO EN ROJO
    # -------------------------------------------------------
    reminder_label = tk.Label(
        win,
        text="Recuerda: El nombre del vendor debe ser exactamente\n igual al nombre que tienen las ordenes",
        fg="red",
        font=("Arial", 10)
    )
    reminder_label.pack(pady=10)

    # -------------------------------------------------------
    # BOTÓN CREAR
    # -------------------------------------------------------
    def crear_vendor():
        name = entry_name.get()  # Guardamos lo que el usuario puso en una variable

        if not name or name == "Ingresa el nombre del vendor":
            messagebox.showerror("Error", "Por favor ingresa un nombre válido para el vendor.")
            return

        # -------------------------------
        # Crear instancia temporal de Vendor
        # -------------------------------
        temp_vendor = Vendor(name)
        temp_vendor.update_structure()  # Ejecutar el método

        # -------------------------------
        # Mensaje de éxito
        # -------------------------------
        entry_name.delete(0, "end")  # Borra el contenido del input
        entry_name.insert(0, "Ingresa el nombre del vendor")  # Vuelve a poner el placeholder
        entry_name.config(fg="grey")  # Color del placeholder



    crear_btn = tk.Button(
        win,
        text="CREAR",
        font=("Arial", 12, "bold"),
        width=20,
        height=2,
        command=crear_vendor
    )
    crear_btn.pack(pady=20)

    # Contenedor con padding para simular borde redondeado
    console_frame = tk.Frame(win, bg="#d1d1d1", bd=2, relief="solid")
    console_frame.pack(pady=5, padx=20)

    console_text = tk.Text(
        console_frame,
        height=15,       # Más líneas visibles
        width=60,        # Un poco menos ancho
        state="disabled",
        bg="#f0f0f0",
        fg="black",
        font=("Consolas", 11),
        relief="flat",   # Quitar borde interno
        padx=5,
        pady=5
    )
    console_text.pack()

    sys.stdout = ConsoleRedirect(console_text)
    sys.stderr = ConsoleRedirect(console_text)