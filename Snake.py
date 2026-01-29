import tkinter as tk
import random
import pygame.mixer as mixer

class JuegoSerpiente:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tu Real Culebra Manito")
        self.root.geometry("600x600")
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="black")
        self.canvas.pack()

        mixer.pre_init(44100, -16, 2, 1024)
        mixer.init()

        self.imagen_fondo = tk.PhotoImage(file="Hierba.png")
        self.canvas.create_image(0, 0, anchor="nw", image=self.imagen_fondo)

        self.imagen_estrella = tk.PhotoImage(file="Star.png").subsample(3, 3)
        self.estrella_id = None

        self.serpiente = [(200, 200)]
        self.direccion = (0, -1)
        self.comida = self.generar_comida()

        self.frutas_comidas = 0
        self.marcador_frutas = self.canvas.create_text(
            10, 10,
            text=f"Frutas comidas: {self.frutas_comidas}",
            fill="white",
            anchor="nw",
            font=("Helvetica", 12)
        )

        self.music_playing = False
        self.juego_terminado = False

        self.root.bind("<space>", self.iniciar_juego)
        self.root.bind("<KeyPress>", self.cambiar_direccion)
        self.root.bind("<KeyPress-p>", self.pausar_juego)
        self.root.bind("<Return>", self.reiniciar_juego)

        self.velocidad = 150
        self.pausa = False
        self.pausa_label = None

    def generar_comida(self):
        return (random.randint(0, 29) * 20, random.randint(0, 29) * 20)

    def actualizar_marcador_frutas(self):
        self.canvas.itemconfig(
            self.marcador_frutas,
            text=f"Frutas comidas: {self.frutas_comidas}"
        )

    def actualizar(self):
        if not self.music_playing or self.pausa or self.juego_terminado:
            return

        cabeza_x, cabeza_y = self.serpiente[0]
        nueva_cabeza = (
            cabeza_x + self.direccion[0] * 20,
            cabeza_y + self.direccion[1] * 20
        )

        # Colisión con bordes
        if not (0 <= nueva_cabeza[0] < 600 and 0 <= nueva_cabeza[1] < 600):
            self.fin_juego()
            return

        # Colisión consigo misma
        if nueva_cabeza in self.serpiente:
            self.fin_juego()
            return

        self.serpiente.insert(0, nueva_cabeza)

        if nueva_cabeza == self.comida:
            self.comida = self.generar_comida()
            self.frutas_comidas += 1
            self.actualizar_marcador_frutas()
        else:
            self.serpiente.pop()

        self.dibujar_serpiente()
        self.dibujar_comida()

        self.root.after(self.velocidad, self.actualizar)

    def cambiar_direccion(self, evento):
        if not self.music_playing or self.pausa or self.juego_terminado:
            return

        if evento.keysym == "Up" and self.direccion != (0, 1):
            self.direccion = (0, -1)
        elif evento.keysym == "Down" and self.direccion != (0, -1):
            self.direccion = (0, 1)
        elif evento.keysym == "Left" and self.direccion != (1, 0):
            self.direccion = (-1, 0)
        elif evento.keysym == "Right" and self.direccion != (-1, 0):
            self.direccion = (1, 0)

    def iniciar_juego(self, evento=None):
        if self.music_playing:
            return

        self.juego_terminado = False
        self.reproducir_musica_fondo()
        self.music_playing = True

        self.ocultar_estrella()
        self.canvas.delete("mensaje_inicio")
        self.actualizar()

    def dibujar_serpiente(self):
        self.canvas.delete("serpiente")
        for x, y in self.serpiente:
            self.canvas.create_rectangle(
                x, y, x + 20, y + 20,
                fill="green",
                tag="serpiente"
            )

    def dibujar_comida(self):
        self.canvas.delete("comida")
        x, y = self.comida
        self.canvas.create_oval(
            x, y, x + 20, y + 20,
            fill="red",
            tag="comida"
        )

    def fin_juego(self):
        self.juego_terminado = True
        self.music_playing = False
        mixer.music.stop()

        self.canvas.create_text(
            300, 300,
            text="GAME OVER\nPresiona ENTER",
            fill="red",
            font=("Helvetica", 28),
            tag="game_over"
        )

        mixer.music.load("GameO.mp3")
        mixer.music.play()

    def reiniciar_juego(self, evento=None):
        if not self.juego_terminado:
            return

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.imagen_fondo)

        self.serpiente = [(200, 200)]
        self.direccion = (0, -1)
        self.comida = self.generar_comida()
        self.frutas_comidas = 0
        self.actualizar_marcador_frutas()

        self.music_playing = False
        self.juego_terminado = False
        self.pausa = False

        self.mostrar_estrella()

    def pausar_juego(self, evento):
        if self.juego_terminado:
            return

        self.pausa = not self.pausa

        if self.pausa:
            mixer.music.pause()
            self.pausa_label = self.canvas.create_text(
                300, 300,
                text="Juego Pausado",
                fill="white",
                font=("Helvetica", 30)
            )
        else:
            mixer.music.unpause()
            self.canvas.delete(self.pausa_label)
            self.actualizar()

    def mostrar_estrella(self):
        self.estrella_id = self.canvas.create_image(
            300, 300,
            image=self.imagen_estrella
        )
        self.canvas.create_text(
            300, 350,
            text="Presiona ESPACIO para iniciar",
            fill="white",
            font=("Helvetica", 14),
            tag="mensaje_inicio"
        )

    def ocultar_estrella(self):
        if self.estrella_id:
            self.canvas.delete(self.estrella_id)

    def reproducir_musica_fondo(self):
        mixer.music.load("Ambiente.mp3")
        mixer.music.play(-1)

if __name__ == "__main__":
    juego = JuegoSerpiente()
    juego.mostrar_estrella()
    juego.root.mainloop()
