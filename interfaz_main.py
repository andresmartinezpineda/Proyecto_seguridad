import tkinter as tk
from interfaz_subir_ordenes import open_upload_orders


def open_create_vendor():
    win = tk.Toplevel(root)
    win.title("Crear Vendor")
    tk.Label(win, text="Aquí va la interfaz para crear vendor").pack(padx=20, pady=20)


def open_update_months():
    win = tk.Toplevel(root)
    win.title("Actualizar Meses")
    tk.Label(win, text="Aquí va la interfaz para actualizar meses").pack(padx=20, pady=20)


root = tk.Tk()
root.title("Panel Principal")
root.geometry("800x600")
root.configure(bg="white")

frame = tk.Frame(root, bg="white")
frame.pack(expand=True)

button_style = {
    "width": 30,
    "height": 3,
    "bg": "#C0BFBF",
    "fg": "black",
    "borderwidth": 2,
    "relief": "solid",
    "font": ("Arial", 14, "bold")
}

tk.Button(
    frame,
    text="SUBIR ORDENES",
    command=lambda: (open_upload_orders(root), root.withdraw()),
    **button_style
).pack(pady=25)

tk.Button(frame, text="CREAR VENDOR",
          command=open_create_vendor, **button_style).pack(pady=25)

tk.Button(frame, text="ACTUALIZAR MESES",
          command=open_update_months, **button_style).pack(pady=25)

root.mainloop()