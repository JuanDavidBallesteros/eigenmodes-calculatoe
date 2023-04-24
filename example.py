import tkinter as tk

root = tk.Tk()
root.title("Mi aplicación de formulario")

# Crear un frame contenedor para los widgets del formulario
form_frame = tk.Frame(root)
form_frame.pack(side="top", padx=20, pady=20)

# Crear un widget de etiqueta para el título
title_label = tk.Label(form_frame, text="Formulario de contacto", font=("Arial", 20))

# Crear los widgets del formulario
name_label = tk.Label(form_frame, text="Nombre:")
name_entry = tk.Entry(form_frame)
email_label = tk.Label(form_frame, text="Email:")
email_entry = tk.Entry(form_frame)
message_label = tk.Label(form_frame, text="Mensaje:")
message_entry = tk.Entry(form_frame)

# Crear un botón para enviar el formulario
send_button = tk.Button(form_frame, text="Enviar", bg="#ff5555", fg="white", padx=20, pady=10, borderwidth=0, relief=tk.FLAT)

# Posicionar los widgets del formulario en el frame contenedor
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

title_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

email_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")
message_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
message_entry.grid(row=3, column=1, padx=5, pady=5, sticky="e")
send_button.grid(row=4, column=1, padx=5, pady=10, sticky="e")



root.mainloop()
