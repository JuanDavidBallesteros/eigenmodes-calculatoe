import math 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Global variables
list_output = []
filterNumber = 100
length= 5.2
width=4
height=2.4

def eigenmodes(length, width, height, eigenfreqs, filterValue, c):

    # Calculate the eigenfrequencies
    for nx in range(0, 5):
        for ny in range(0, 5):
            for nz in range(0, 5):
                if nx != 0 or ny != 0 or nz != 0:
                    freq = (c/2)*(math.sqrt((nx/length)**2 + (ny/width)**2 + (nz/height)**2))
                    eigenfreqs.append((freq, nx, ny, nz))
    
    # Sort the eigenfrequencies in ascending order
    eigenfreqs = sorted(eigenfreqs)

    # df = pd.DataFrame(eigenfreqs[:filterValue],columns = ["Freq (Hz)","K", "M", "N"])
    # display(df)

    # Print the eigenmodes
    print("Eigenmodes:")
    print("  {:>5s}  {:>5s}  {:>5s}  {:>5s}".format("Freq (Hz)","K", "M", "N")) # Table Head
    for i, (freq, nx, ny, nz) in enumerate(eigenfreqs[:filterValue]):
        print("  {:.2f}  {:.0f}  {:.0f}  {:.0f}".format(freq, nx, ny, nz))
        
    return eigenfreqs
        
def drawEigenmodes(eigenfreqs, filterValue):
  # Plot the eigenfrequencies as a bar graph
    modes = ["{:.2f}".format(freq) for (freq, nx, ny, nz ) in eigenfreqs[:filterValue]]
    freqs = [1.1 if (nx, ny, nz) in [(1,0,0), (0,1,0), (0,0,1), (1,1,1), (1,0,1), (1,1,0), (0,1,1)] else 1 for (_, nx, ny, nz) in eigenfreqs[:filterValue]]
    colors = ["red" if (nx, ny, nz) in [(1,0,0), (0,1,0), (0,0,1), (1,1,1), (1,0,1), (1,1,0), (0,1,1)] else "grey" for (_, nx, ny, nz) in eigenfreqs[:filterValue]]

    plt.bar(modes, freqs, color=colors)
    plt.ylabel("Eigenmode")
    plt.xlabel("Frequency (Hz)")
    plt.title("Eigenmodes of a rectangular room")

    ax = plt.gca()
    ax.axes.get_yaxis().set_ticks([])
    ax.set_xticks(ax.get_xticks()[::5])
    font_props = fm.FontProperties(size=10)
    plt.xticks(rotation=70, fontproperties=font_props)
    # Save the graph as a JPEG file
    plt.savefig("eigenmodes.png", bbox_inches="tight")
    #plt.show()
    
    
def dimensionesGenerales(Largo, Ancho, Alto):
    volumen = Largo * Ancho * Alto
    a_techo= Largo * Ancho
    a_suelo= Largo * Ancho
    a_paredes_1= Ancho * Alto*2
    a_paredes_2=Largo * Alto*2
    
    print("Volumen de la habitación: {:.2f} m^3".format(volumen))
    print("")
    print("Área del Techo: {:.2f} m^2".format(a_techo))
    print("Área del Suelo: {:.2f} m^2".format(a_suelo))
    print("Área del Paredes 1: {:.2f} m^2".format(a_paredes_1))
    print("Área del Paredes 2: {:.2f} m^2  \n\n".format(a_paredes_2))
    
    return { 
            "volumen": volumen,
            "a_techo": a_techo, 
            "a_suelo": a_suelo, 
            "a_paredes1": a_paredes_1, 
            "a_paredes2": a_paredes_2
            }

def rtmid_critica(rt_mid,  freq_critica, Con_RTmid, k_shoedler, volumen):
    if rt_mid == 0 and Con_RTmid:
        raise Exception("Debes definir un valor para RTmid diferente a 0")

    if freq_critica == 0 and not Con_RTmid:
        raise Exception("Debes definir un valor para la frecuencia crítica diferente a 0")
    
    if Con_RTmid:
        print("Tiempo de reverberación: (RTmid): {:.2f} s".format(rt_mid))

    if freq_critica != 0 and not Con_RTmid:
        rt_mid = ((freq_critica/k_shoedler)**2)*volumen 
        print("Tiempo de reverberación en base a la frecuencia crítica dada es: (RTmid): {:.2f} s".format(rt_mid))
    
    if Con_RTmid:
        freq_critica = k_shoedler*math.sqrt(rt_mid/(volumen))
        print("Frecuencia Crítica en base a RTmid dado: {:.2f} Hz".format(freq_critica))

    if not Con_RTmid:
        print("Frecuencia Crítica: {:.2f} Hz".format(freq_critica))
        
    print("\n\n")
    return { 
            "rt_mid":rt_mid , 
            "freq_critica":freq_critica
            }   
    
def get_modos(c,Alto, Ancho, Largo, freq_critica ):

    # Modos
    c = 340.0  # m/s
    L = 4*(Alto+Ancho+Largo)
    S = 2*(Ancho*Alto+Ancho*Largo+Alto*Largo)
    V = (Largo*Ancho*Alto)

    NL = (L*freq_critica)//(8*c) # Axiales

    NV = (V*4*math.pi*(freq_critica**3))//(3*(c**3)) # Oblicuos

    NE = (math.pi*S*(freq_critica**2))//(4*(c**2))  # Tangenciales

    Nf = NL+NE+NV # Numero de modos totales


    print("Modos: \n Axiales: {:.1f} \n Oblicuos: {:.1f} \n angenciales: {:.1f} \n\n Total de modos:  {:.1f}".format(NL,NV, NE, Nf))

    # Densidad Modal

    DN = ((4*math.pi*V*(freq_critica**2)) / (c**3))  + ((math.pi*S*freq_critica) / (2*(c**2))) + (L/(8*c))

    print("Dencidad Modal: {:.2f} ".format(DN))
    
    return {
        "Axiales": NL,
        "Oblicuos": NV,
        "angenciales": NE,
        "modos_totales": Nf,
        "Dencidad": DN
    }
