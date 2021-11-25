import gamelib
import random
import palabras
import string

PALABRAS = palabras.copiar_palabras()
INTENTOS_MAXIMOS = 7
SALIR = "Escape"
LETRAS_ACENTOS = {"á": "a", "ä": "a", "é": "e", "ë": "e", "í": "i", "ï": "i", "ó": "o", "ö": "o", "ú": "u", "ü": "u"}
imagenes = {0: "hangman0.gif", 1: "hangman1.gif", 2: "hangman2.gif", 3: "hangman3.gif", 4: "hangman4.gif", 5: "hangman5.gif", 6: "hangman6.gif"}

def actualizar_palabra_mostrada(letra, palabra, letras_adivinadas):
	cantidad_letras_adivinadas_iniciales = len(letras_adivinadas)
	palabra_mostrada = ""
	for c in palabra:
		if c in letras_adivinadas:
			palabra_mostrada += c
		elif c in LETRAS_ACENTOS:
			if LETRAS_ACENTOS[c] == letra.lower():
				palabra_mostrada += c
				letras_adivinadas.append(c)
			else:
				palabra_mostrada += "*"
		elif letra.lower() == c:
			palabra_mostrada += c
			letras_adivinadas.append(c)
		else:
			palabra_mostrada += "*"
	if cantidad_letras_adivinadas_iniciales == len(letras_adivinadas):
		return palabra_mostrada, False
	return palabra_mostrada, True

def pedir_letra(letras_adivinadas, letras_incorrectas):
	while True:
		ev = gamelib.wait(gamelib.EventType.KeyPress)
		if not ev:
			break
		tecla = ev.key
		if tecla == SALIR:
			return None
		if tecla == "ntilde":
			letra = "ñ"
			return letra
		letra = tecla
		if letra.lower() not in string.ascii_lowercase:
			continue
		if letra in letras_adivinadas or letra in letras_incorrectas:
			continue
		return letra

def main():
	inicializar = True
	gamelib.resize(300, 300)
	while gamelib.is_alive():
		if inicializar:
			numero = random.randrange(0, len(PALABRAS))
			palabra = PALABRAS[numero]
			letras_adivinadas = []
			letras_incorrectas = ""
			palabra_mostrada = "*" * len(palabra)
			intentos = 0
		inicializar = False

		gamelib.title("Ahorcado")
		gamelib.draw_begin()
		gamelib.draw_image('white.gif', 0, 0)

		for i in range(0, intentos+1):
			gamelib.draw_image(imagenes[i], -20, 20)
		gamelib.draw_text(letras_incorrectas, 160-(len(letras_incorrectas)*12//2), 250, size=20, fill='black', anchor='nw')
		gamelib.draw_text(palabra_mostrada, 145-(len(palabra)*12//2), 13, size=20, fill='black', anchor='nw')

		if palabra == palabra_mostrada:
			gamelib.play_sound('win_sound.wav')
			gamelib.say(f"GANASTE")
		if intentos == INTENTOS_MAXIMOS-1:
			gamelib.say(f"PERDISTE\nLa palabra era {palabra}")
		if palabra == palabra_mostrada or intentos == INTENTOS_MAXIMOS-1:
			inicializar = True
			continue

		letra = pedir_letra(letras_adivinadas, letras_incorrectas)
		if letra == None:
			break

		palabra_mostrada, adivino = actualizar_palabra_mostrada(letra, palabra, letras_adivinadas)
		if not adivino:
			letras_incorrectas += letra + " "
			intentos += 1
		
		gamelib.draw_end()


gamelib.init(main)
main()