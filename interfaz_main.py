import tkinter as tk
from interfaz_subir_ordenes import open_upload_orders
from interfaz_crear_vendor import create_vendor_window
from interfaz_actualizar_meses import open_update_months

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
    "font": ("Arial", 14, "bold"),
}

tk.Button(
    frame,
    text="SUBIR ORDENES",
    command=lambda: (open_upload_orders(root), root.withdraw()),
    **button_style
).pack(pady=25)

tk.Button(
    frame,
    text="CREAR VENDOR",
    command=lambda: (create_vendor_window(root), root.withdraw()),
    **button_style
).pack(pady=25)

tk.Button(
    frame,
    text="ACTUALIZAR MESES",
    command=lambda: (open_update_months(root), root.withdraw()),
    **button_style
).pack(pady=25)


root.mainloop()