import tkinter as tk
from tkinter import Canvas, PhotoImage, ttk
from funciones import *
from PIL import ImageTk, Image
from test_img import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Calculadora de Modos")
        
        
        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("TButton",background='#cba',borderwidth=0, font=("Arial", 12), relief='flat')
        style.configure("TEntry",borderwidth=0, font=("Arial", 12))

        # Crear un frame contenedor para los widgets del formulario
        form_frame = tk.Frame(self.master)
        form_frame.pack(side="top", padx=20, pady=20)

        # Sección constantes
        k_title_label = tk.Label(form_frame, text="Definición de constantes", font=("Arial", 20))
        self.sound_label = tk.Label(form_frame, text="Constante del sonido:")
        self.sound_entry = tk.Entry(form_frame)
        self.schoedler_label = tk.Label(form_frame, text="Constante de schoedler:")
        self.schoedler_entry = tk.Entry(form_frame)
        
        # Sección cuarto
        room_title_label = tk.Label(form_frame, text="Dimensiones del cuarto", font=("Arial", 20))
        self.largo_label = tk.Label(form_frame, text="Largo:")
        self.largo_entry = tk.Entry(form_frame)
        self.ancho_label = tk.Label(form_frame, text="Ancho:")
        self.ancho_entry = tk.Entry(form_frame)
        self.alto_label = tk.Label(form_frame, text="Alto:")
        self.alto_entry = tk.Entry(form_frame)
        
        # Sección RTmid y Freq Critica
        opciones_label = tk.Label(form_frame, text="Calculo RTmid o frecuencia crítica", font=("Arial", 20))
        self.Con_RTmid = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(form_frame, text="Usar RTmid?", variable=self.Con_RTmid)
        self.rt_mid_label = tk.Label(form_frame, text="RTmid:")
        self.rt_mid_entry = tk.Entry(form_frame)
        self.freq_critica_label = tk.Label(form_frame, text="Frecuencia Crítica:")
        self.freq_critica_entry = tk.Entry(form_frame)

        # Crear un botón para enviar el formulario
        send_button = tk.Button(form_frame, text="Calcular", bg="#ff5555", 
                                fg="white", padx=20, pady=10, borderwidth=0, 
                                relief=tk.FLAT, command=self.submit)

        # Posicionar los widgets del formulario en el frame contenedor
        k_title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.sound_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.sound_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        self.schoedler_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.schoedler_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        room_title_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.largo_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.largo_entry.grid(row=4, column=1, padx=5, pady=5, sticky="e")
        self.ancho_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.ancho_entry.grid(row=5, column=1, padx=5, pady=5, sticky="e")
        self.alto_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.alto_entry.grid(row=6, column=1, padx=5, pady=5, sticky="e")
        
        opciones_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.checkbox.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.rt_mid_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.rt_mid_entry.grid(row=9, column=1, padx=5, pady=5, sticky="e")
        self.freq_critica_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.freq_critica_entry.grid(row=10, column=1, padx=5, pady=5, sticky="e")
        
        send_button.grid(row=11, column=1, padx=5, pady=10, sticky="e")

    def submit(self):

        # Obtener el valor del campo de formulario
        dimensiones = dimensionesGenerales(int(self.largo_entry.get()), 
                             int(self.ancho_entry.get()),  
                             int(self.alto_entry.get()))
        
        print( self.Con_RTmid.get())
        
        rtmid_and_critica = rtmid_critica(int(self.rt_mid_entry.get()), 
                                          int(self.freq_critica_entry.get()), 
                                          self.Con_RTmid.get(), 
                                          int(self.schoedler_entry.get()), 
                                          dimensiones["volumen"] )
        
        modes = get_modos(self.sound_entry.get(),
                     int(self.largo_entry.get()), 
                     int(self.ancho_entry.get()), 
                     int(self.alto_entry.get()), 
                     rtmid_and_critica["freq_critica"])
        
        lista = []
        eigenmodes(int(self.largo_entry.get()),
                            int(self.ancho_entry.get()),
                            int(self.alto_entry.get()),
                            lista, int(100), int(self.sound_entry.get()))
        
        grafica = drawEigenmodes(lista, int(100))
        
    ## -------------------------------------- Caracterisitcas fisicas y modos ------------------------------
        # Crear una nueva ventana
        new_window = tk.Toplevel(root)
        new_window.title("RTmid, Freq Critica y Modos")
        
        # Configurar los widgets de la nueva ventana con los datos ingresados
        Resultados = tk.Label(new_window, text="\n\nResultados \n", font=("Arial", 20))
        freq_critica = tk.Label(new_window, text="Frecuencia Crítica: {:.2f} Hz".format(rtmid_and_critica["freq_critica"]))
        rtmid = tk.Label(new_window, text="Tiempo de reverberación: (RTmid): {:.2f} s".format(rtmid_and_critica["rt_mid"]))
        
        dimensiones2 = tk.Label(new_window, text="\n\nDimensiones\n", font=("Arial", 20))
        volumen = tk.Label(new_window, text=f'''Volumen de la habitación: {dimensiones["volumen"]} m^3''')
        a_techo = tk.Label(new_window, text="Área del Techo: {:.2f} m^2".format(dimensiones["a_techo"]))
        a_suelo = tk.Label(new_window, text="Área del Suelo: {:.2f} m^2".format(dimensiones["a_suelo"]))
        a_paredes1 = tk.Label(new_window, text="Área del Paredes 1: {:.2f} m^2".format(dimensiones["a_paredes1"]))
        a_paredes2 = tk.Label(new_window, text="Área del Paredes 2: {:.2f} m^2".format(dimensiones["a_paredes2"]))
        
        modos = tk.Label(new_window, text="\n\nModos\n", font=("Arial", 20))
        axiales = tk.Label(new_window, text="Modos Axiales: {:.1f} ".format(modes["Axiales"]))
        Oblicuos = tk.Label(new_window, text="Modos Oblicuos: {:.1f} ".format(modes["Oblicuos"]))
        tangenciales = tk.Label(new_window, text="Modos tangenciales: {:.1f} ".format(modes["angenciales"]))
        total_modos = tk.Label(new_window, text="Modos totales:  {:.1f}".format(modes["modos_totales"]))
        densidad_modal = tk.Label(new_window, text="Dencidad Modal: {:.2f} ".format(modes["Dencidad"]))
        
        Resultados.pack()        
        freq_critica.pack()
        rtmid.pack()
        dimensiones2.pack()
        volumen.pack()
        a_techo.pack()
        a_suelo.pack()
        a_paredes1.pack()
        a_paredes2.pack()
        modos.pack()
        axiales.pack()
        Oblicuos.pack()
        tangenciales.pack()
        total_modos.pack()
        densidad_modal.pack()
    
    
    ## -------------------------------------- Tabla ------------------------------
        # Crear una nueva ventana
        new_window2 = tk.Toplevel(root)
        new_window2.title("Lista de eigenmodes")
        
        tree = ttk.Treeview(new_window2)
        tree["columns"] = ("Freq","K", "M", "N")
        tree.column("Freq", width=100, anchor='center')
        tree.column("K", width=100, anchor='center') 
        tree.column("M", width=100, anchor='center')
        tree.column("N", width=100, anchor='center')

        tree.heading("#0", text="Fila")
        tree.heading("Freq", text="Freq (Hz)")
        tree.heading("K", text="K") 
        tree.heading("M", text="M")
        tree.heading("N", text="N")      

        # Añadir elementos a la lista
        i = 0
        for item in lista:
            i = i+1
            tree.insert("", 0, text=i, values=item)
        
        tree.pack()

        # Crear una nueva ventana
        new_window3 = tk.Toplevel(root)
        new_window3.title("Gráfica")
        
        image = Image.open("eigenmodes.png")

        # Verificamos que la imagen se cargó correctamente
        if image.format == "png":
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
        label = tk.Label(new_window3, image=photo)
        label.pack()
        
        run(root)
                    

root = tk.Tk()
app = Application(master=root)
app.mainloop()
