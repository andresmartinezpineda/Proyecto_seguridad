import tkinter as tk
from interfaz_subir_ordenes import open_upload_orders
from interfaz_crear_vendor import create_vendor_window
from interfaz_actualizar_meses import open_update_months

root = tk.Tk()
root.title("Panel Principal")
root.geometry("600x450")
root.configure(bg="#F5F5F5")   # gris claro moderno

frame = tk.Frame(root, bg="#F5F5F5")
def on_enter(e):
    e.widget['bg'] = "#005A9E"   # azul más oscuro

def on_leave(e):
    e.widget['bg'] = "#0072CE"
frame.pack(expand=True)

title_label = tk.Label(
    frame,
    text="PANEL PRINCIPAL",
    bg="#F5F5F5",
    fg="#0072CE",
    font=("Segoe UI", 25, "bold")
)
title_label.pack(pady=(30, 10))


button_style = {
    "width": 30,
    "height": 2,
    "bg": "#0072CE",        # Azul Open English
    "fg": "white",
    "activebackground": "#005A9E",  # tono más oscuro al pulsar
    "activeforeground": "white",
    "borderwidth": 0,       # Quita bordes para look moderno
    "relief": "flat",
    "font": ("Segoe UI", 14, "bold"),  # fuente más moderna
    "cursor": "hand2"       # mano al pasar
}

btn_upload = tk.Button(
    frame,
    text="SUBIR ORDENES",
    command=lambda: (open_upload_orders(root), root.withdraw()),
    **button_style
)
btn_upload.pack(pady=15)
btn_upload.bind("<Enter>", on_enter)
btn_upload.bind("<Leave>", on_leave)

btn_upload = tk.Button(
    frame,
    text="CREAR VENDOR",
    command=lambda: (create_vendor_window(root), root.withdraw()),
    **button_style
)
btn_upload.pack(pady=15)
btn_upload.bind("<Enter>", on_enter)
btn_upload.bind("<Leave>", on_leave)

btn_upload = tk.Button(
    frame,
    text="ACTUALIZAR MESES",
    command=lambda: (open_update_months(root), root.withdraw()),
    **button_style
)
btn_upload.pack(pady=15)
btn_upload.bind("<Enter>", on_enter)
btn_upload.bind("<Leave>", on_leave)


root.mainloop()