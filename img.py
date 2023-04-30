from PIL import Image
import tkinter as tk
import os, sys

def run(root):
    app_path = os.path.dirname(sys.executable)
    # Creamos la ventana de tkinter

    # Abrimos la imagen y la cargamos en un objeto Image
    image1 = Image.open("eigenmodes.png")

    # Verificamos que la imagen se cargó correctamente
    if image1.format == "png":
        print("La imagen se cargó correctamente.")
    else:
        print("Error al cargar la imagen.")

    # Creamos un objeto PhotoImage de tkinter a partir de la imagen abierta
    photo = tk.PhotoImage(file="eigenmodes.png")

    # Verificamos que el objeto PhotoImage se creó correctamente
    if photo:
        print("El objeto PhotoImage se creó correctamente.")
    else:
        print("Error al crear el objeto PhotoImage.")

    # Mostramos la imagen en un widget Label
    label = tk.Label(root, image=photo)
    label.pack()

    root.mainloop()
