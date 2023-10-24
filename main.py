from PIL import Image
import pyglet
import random
from pyglet import shapes
import json
import tkinter as tk
from tkinter import filedialog

# Ventana de selección de archivo
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal

# Abre un cuadro de diálogo para seleccionar un archivo
file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])

if file_path:
    # Cargar el archivo JSON seleccionado
    with open(file_path, 'r') as archivo:
        data = json.load(archivo)
    
    # Acceder a los datos del archivo JSON
    print(data)
else:
    print("No se seleccionó ningún archivo")


music = pyglet.media.load('music.wav', streaming=False)
music.play()


# Cargar los datos desde el archivo JSON
with open("categorias_de_palabras.json", "r") as archivo:
    categorias_de_palabras = json.load(archivo)




# Función para reiniciar el juego
def reiniciar_juego():
    global palabra, palabra_label, intentos, letras_adivinadas, perdiste, letras_pulsadas, categoria_elegida, pista
    categoria_elegida = random.choice(list(data.keys()))

    # Elegir un elemento al azar de la categoría seleccionada
    elemento_elegido = random.choice(data[categoria_elegida])
    palabra = elemento_elegido["nombre"].lower()
    palabra_label = elemento_elegido["nombre"]
    pista = elemento_elegido["pista"]
    intentos = 6
    letras_adivinadas = []
    letras_pulsadas = []  # Inicializa letras_pulsadas
    perdiste = False

# Función para verificar si el juego ha terminado
def juego_terminado():
    return set(letras_adivinadas) == set(palabra) or intentos == 0


# Elegir una categoría al azar del archivo JSON
categoria_elegida = random.choice(list(data.keys()))

# Elegir un elemento al azar de la categoría seleccionada
elemento_elegido = random.choice(data[categoria_elegida])

# Obtener los atributos del elemento seleccionado (por ejemplo, nombre y pista)
palabra = elemento_elegido["nombre"].lower()
palabra_label = elemento_elegido["nombre"]
pista = elemento_elegido["pista"]

intentos = 6  # Número de intentos permitidos
letras_adivinadas = []  # Letras adivinadas
letras_pulsadas = []  # Letras pulsadas
perdiste = False  # Variable para controlar si se ha perdido

# Inicializar la ventana
ventana = pyglet.window.Window()

# Cargar la imagen original con Pillow
imagen_reinicio_original = Image.open('reiniciar.png')

# Definir el factor de escala (por ejemplo, 0.5 para reducir a la mitad)
escala = 0.3

# Redimensionar la imagen a las nuevas dimensiones sin recortar
nueva_anchura = int(imagen_reinicio_original.width * escala)
nueva_altura = int(imagen_reinicio_original.height * escala)
imagen_reinicio_redimensionada = imagen_reinicio_original.resize((nueva_anchura, nueva_altura))

# Convertir la imagen redimensionada de Pillow a una imagen Pyglet
imagen_reinicio_pyglet = pyglet.image.ImageData(nueva_anchura, nueva_altura, 'RGBA', imagen_reinicio_redimensionada.tobytes(), -nueva_anchura * 4)

# Crear un sprite con la imagen redimensionada
boton_reiniciar = pyglet.sprite.Sprite(imagen_reinicio_pyglet)

# Ajustar la posición vertical para que el botón esté un poco más abajo
desplazamiento_vertical = 150  # Cambia esto según tus necesidades
boton_reiniciar.x = (ventana.width - boton_reiniciar.width) // 2  # Alineación horizontal al centro
boton_reiniciar.y = (ventana.height - boton_reiniciar.height) // 2 - desplazamiento_vertical

# ...

batch = pyglet.graphics.Batch()
batch1 = pyglet.graphics.Batch()
batch2 = pyglet.graphics.Batch()
batch3 = pyglet.graphics.Batch()
batch4 = pyglet.graphics.Batch()
batch5 = pyglet.graphics.Batch()
batch6 = pyglet.graphics.Batch()
palo = shapes.Line(42, 100, 300, 100, width=15, batch=batch, color=(139, 69, 19))  # Cambia el color a café (RGB: 139, 69, 19)
palo2 = shapes.Line(50, 100, 50, 450, width=15, batch=batch, color=(139, 69, 19))  # Cambia el color a café (RGB: 139, 69, 19)
palo3 = shapes.Line(42, 442, 180, 442, width=15, batch=batch, color=(139, 69, 19))  # Cambia el color a café (RGB: 139, 69, 19)
lazo = shapes.Line(175, 375, 175, 435, width=10, batch=batch, color=(255, 255, 255))  # Cambia el color a café (RGB: 139, 69, 19)
humano1 = shapes.Circle(175, 350, 35, segments=30, batch=batch1, color=(139, 69, 19))
humano2 = shapes.Line(175, 230, 175, 315, width=10, batch=batch2, color=(139, 69, 19))  # Cambia el color a café (RGB: 139, 69, 19)
humano3 = shapes.Line(175, 295, 220, 250, width=10, batch=batch3, color=(139, 69, 19))  # Cambia el color a café (RGB: 139, 69, 19)
humano4 = shapes.Line(130, 250, 175, 295, width=10, batch=batch4, color=(139, 69, 19))  # Cambia el color a café (RGB: 139, 69, 19)
humano5 = shapes.Line(175, 235, 220, 190, width=10, batch=batch5, color=(139, 69, 19))  # Cambia el color a café (RGB: 139, 69, 19)
humano6 = shapes.Line(130, 190, 175, 235, width=10, batch=batch6, color=(139, 69, 19))  # Cambia el color a café (RGB: 139, 69, 19)
# Función para dibujar el estado actual del juego
@ventana.event
def on_draw():    
    ventana.clear()
    estado_actual = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            estado_actual += letra
        else:
            estado_actual += " _ "

    if set(letras_adivinadas) == set(palabra):
        mensaje = "¡Felicidades!\nHas adivinado la palabra:\n" + palabra_label
    elif intentos == 0:
        mensaje = "¡Perdiste!\nLa palabra era:\n" + palabra_label
    else:
        mensaje = estado_actual

    # Divide el mensaje en varias líneas
    mensaje_lines = mensaje.split('\n')
    y_position = ventana.height // 2 + 50

    # Dibuja cada línea del mensaje
    for line in mensaje_lines:
        label = pyglet.text.Label(line,
                                 font_name='Arial',
                                 font_size=36,
                                 x=ventana.width // 2,
                                 y=y_position,
                                 anchor_x='center', anchor_y='center')
        label.draw()
        y_position -= 50  # Ajusta la posición vertical para la próxima línea

    # Dibuja el botón de reinicio si el juego ha terminado
    if juego_terminado():
        boton_reiniciar.draw()
    elif not juego_terminado():
        categoria = "Categoría: " + categoria_elegida + ", Pista: " + pista
        categoria_label = pyglet.text.Label(categoria,
                                                   font_name='Arial',
                                                   font_size=24,
                                                   x=ventana.width // 2,
                                                   y=y_position + 200,
                                                   anchor_x='center', anchor_y='center')
        categoria_label.draw()
        letras_pulsadas_str = "Letras pulsadas: " + ", ".join(letras_pulsadas)
        letras_pulsadas_label = pyglet.text.Label(letras_pulsadas_str,
                                                   font_name='Arial',
                                                   font_size=24,
                                                   x=ventana.width // 2,
                                                   y=y_position - 50,
                                                   anchor_x='center', anchor_y='center')
        letras_pulsadas_label.draw()
        
        # Dibuja una línea vertical al lado del mensaje

        batch.draw()
        if intentos == 5:
            # Muestra humano1
            batch1.draw()
        elif intentos == 4:
            # Muestra humano2
            batch1.draw()
            batch2.draw()
        elif intentos == 3:
            # Muestra humano3
            batch1.draw()
            batch2.draw()
            batch3.draw()
        elif intentos == 2:
            # Muestra humano4
            batch1.draw()
            batch2.draw()
            batch3.draw()
            batch4.draw()
        elif intentos == 1:
            # Muestra humano5
            batch1.draw()
            batch2.draw()
            batch3.draw()
            batch4.draw()
            batch5.draw()
        elif intentos == 0:
            # Muestra humano6
            batch1.draw()
            batch2.draw()
            batch3.draw()
            batch4.draw()
            batch5.draw()
            batch6.draw()

                

# Función para manejar eventos del mouse
@ventana.event
def on_mouse_press(x, y, button, modifiers):
    if juego_terminado() and boton_reiniciar.x < x < boton_reiniciar.x + boton_reiniciar.width and boton_reiniciar.y < y < boton_reiniciar.y + boton_reiniciar.height:
        reiniciar_juego()

# Función para manejar eventos de teclado
@ventana.event
def on_key_press(symbol, modifiers):
    if juego_terminado():
        return

    letra = chr(symbol)

    if letra not in letras_pulsadas:
        letras_pulsadas.append(letra)

        # Comprobar si la letra ya ha sido adivinada
        if letra in letras_adivinadas:
            return

        # Comprobar si la letra está en la palabra
        if letra in palabra:
            letras_adivinadas.append(letra)
        else:
            global intentos
            intentos -= 1

            

    # Resto del código para dibujar el mensaje y otros elementos




# Inicializar la aplicación Pyglet
if __name__ == "__main__":
    pyglet.app.run()
