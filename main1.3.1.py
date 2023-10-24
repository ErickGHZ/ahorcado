from PIL import Image
import pyglet
import random

# Lista de palabras para adivinar
palabras = ["python", "programacion", "computadora", "tecnologia", "inteligencia"]

# Función para reiniciar el juego
def reiniciar_juego():
    global palabra, intentos, letras_adivinadas, perdiste, letras_pulsadas
    palabra = random.choice(palabras)
    intentos = 6
    letras_adivinadas = []
    letras_pulsadas = []  # Inicializa letras_pulsadas
    perdiste = False

# Función para verificar si el juego ha terminado
def juego_terminado():
    return set(letras_adivinadas) == set(palabra) or intentos == 0

# Elegir una palabra al azar
palabra = random.choice(palabras)

# Inicializar las variables
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

# Función para dibujar el estado actual del juego
@ventana.event
def on_draw():
    ventana.clear()
    estado_actual = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            estado_actual += letra
        else:
            estado_actual += "_"

    if set(letras_adivinadas) == set(palabra):
        mensaje = "¡Felicidades!\nHas adivinado la palabra:\n" + palabra
    elif intentos == 0:
        mensaje = "¡Perdiste!\nLa palabra era:\n" + palabra
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
        # Dibuja las letras pulsadas
        letras_pulsadas_str = "Letras pulsadas: " + ", ".join(letras_pulsadas)
        letras_pulsadas_label = pyglet.text.Label(letras_pulsadas_str,
                                                   font_name='Arial',
                                                   font_size=24,
                                                   x=ventana.width // 2,
                                                   y=y_position - 50,
                                                   anchor_x='center', anchor_y='center')
        letras_pulsadas_label.draw()


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

    letra = chr(symbol).lower()

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

# Inicializar la aplicación Pyglet
if __name__ == "__main__":
    pyglet.app.run()
