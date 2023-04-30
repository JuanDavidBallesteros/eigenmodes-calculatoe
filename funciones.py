import math 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Variables Globales
list_output = []
filterNumber = 100
length= 5.2
width=4
height=2.4



'''
Esta función calcula las frecuencias propias de vibración (o eigenfrecuencias) de una cavidad tridimensional rectangular, 
donde length, width y height son las dimensiones de la cavidad. El parámetro c representa la velocidad del sonido.
Se utiliza un bucle anidado para calcular las eigenfrecuencias para diferentes modos de vibración, y las frecuencias se 
agregan a una lista eigenfreqs. Después, se ordenan las eigenfrecuencias en orden ascendente.

Finalmente, se imprimen las eigenfrecuencias en la consola, con un encabezado de tabla que muestra las etiquetas de las 
columnas. El número de eigenfrecuencias que se imprimen se determina mediante el parámetro filterValue.

La función devuelve una lista de tuplas que contienen las eigenfrecuencias y los números cuánticos de los modos de 
vibración correspondientes.
'''
def eigenmodes(length, width, height, eigenfreqs, filterValue, c):

    # Calculo de las eigenfrencias
    for nx in range(0, 5):
        for ny in range(0, 5):
            for nz in range(0, 5):
                if nx != 0 or ny != 0 or nz != 0:
                    freq = (c/2)*(math.sqrt((nx/length)**2 + (ny/width)**2 + (nz/height)**2))
                    eigenfreqs.append((freq, nx, ny, nz))
    
    # Ordenar las frecuencias en orden asendetete
    eigenfreqs = sorted(eigenfreqs)


    # Impresión por consola
    print("Eigenmodes:")
    print("  {:>5s}  {:>5s}  {:>5s}  {:>5s}".format("Freq (Hz)","K", "M", "N")) # Table Head
    for i, (freq, nx, ny, nz) in enumerate(eigenfreqs[:filterValue]):
        print("  {:.2f}  {:.0f}  {:.0f}  {:.0f}".format(freq, nx, ny, nz))
        
    return eigenfreqs




'''
Esta función genera una gráfica de barras que representa los modos de resonancia de una habitación rectangular. 
Recibe como argumentos una lista de eigenfrecuencias previamente calculadas, así como un valor para filtrar las 
frecuencias que se desean graficar.

Dentro de la función se crea una lista de strings con las frecuencias formateadas en dos decimales, se genera una 
lista de valores para la altura de las barras (1.1 para los modos fundamentales, 1 para los demás) y se establecen 
los colores de las barras dependiendo de si los modos son fundamentales o no.

Luego se usa la biblioteca matplotlib para crear la gráfica de barras con los valores previamente calculados. Se 
configuran los ejes, el título y los ticks del eje x, se rotan las etiquetas para que sean legibles y se guarda la 
gráfica en un archivo llamado "eigenmodes.png".
 '''       
def drawEigenmodes(eigenfreqs, filterValue):
  # Grafica de los eigenmodos
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
    # guardar el archivo
    plt.savefig("eigenmodes.png", bbox_inches="tight")
    #plt.show()
    
    
    
  
'''
Esta función recibe como entrada las dimensiones (largo, ancho, alto) de una habitación y 
calcula algunas propiedades geométricas de la misma, como el volumen y el área de su techo, 
suelo y paredes.

El resultado se imprime por consola y se devuelve como un diccionario con las siguientes claves:
"volumen", "a_techo", "a_suelo", "a_paredes1" y "a_paredes2" donde la letra "a_" hace referencia 
al área de cada una de las superficies de la habitación.
'''     
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




'''
La función rtmid_critica recibe los siguientes argumentos:

rt_mid: el tiempo de reverberación midrange de la habitación.
freq_critica: la frecuencia crítica de la habitación.
Con_RTmid: un valor booleano que indica si se proporciona el tiempo de reverberación o la frecuencia crítica.
k_shoedler: constante de Shoedler, que se usa para calcular la frecuencia crítica.
volumen: el volumen de la habitación.
La función comprueba si se proporciona el tiempo de reverberación o la frecuencia crítica y, a continuación, 
}calcula y devuelve el valor que falta.

Si se proporciona el tiempo de reverberación midrange (rt_mid) y Con_RTmid es verdadero, se imprime el valor 
de rt_mid en segundos.

Si no se proporciona el tiempo de reverberación midrange y Con_RTmid es falso, se utiliza la frecuencia crítica 
(freq_critica) para calcular el tiempo de reverberación midrange y se imprime su valor en segundos.

Si se proporciona el tiempo de reverberación midrange (rt_mid) y Con_RTmid es verdadero, se utiliza el tiempo de 
reverberación midrange para calcular la frecuencia crítica (freq_critica) y se imprime su valor en Hz.

Si no se proporciona el tiempo de reverberación midrange y Con_RTmid es falso, se imprime el valor de la frecuencia crítica.

La función devuelve un diccionario con los valores de rt_mid y freq_critica.
'''
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



'''
La función get_modos calcula el número y densidad de los diferentes modos de vibración de una 
habitación en base a sus dimensiones y a una frecuencia crítica dada.
Los modos se dividen en tres tipos: Axiales, Oblicuos y Tangenciales, y se calculan en base al 
largo, ancho y alto de la habitación y a la frecuencia crítica dada.

El número de modos totales se obtiene sumando los modos axiales, oblicuos y tangenciales.
La densidad modal se calcula en base al volumen, área de las paredes y frecuencia crítica dada.
'''
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
