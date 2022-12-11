import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib 
from math import pi, sin
from matplotlib import pyplot as plt

matplotlib.use('TkAgg')

class TransformeeFourrier:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Transformée de Fourrier")
        self.fenetre.rowconfigure(0, minsize=700, weight=1)
        self.fenetre.columnconfigure(1, minsize=1150, weight=1)

        self.frame = tk.Frame(self.fenetre, relief=tk.RAISED, bd=2)
        self.frame.grid(row=0, column=0, sticky="ns")

        self.frame_principal = tk.Frame(self.fenetre, relief=tk.RAISED, bd=2)
        self.frame_principal.grid(row=0, column=1, sticky="ns")

        self.frame_diagrame_sinusoidal = tk.Frame(self.frame_principal, relief=tk.RAISED, bd=2)
        self.frame_diagrame_sinusoidal.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.frame_diagrame_continu = tk.Frame(self.frame_principal, relief=tk.RAISED, bd=2)
        self.frame_diagrame_continu.grid(row=1, column=1, sticky=tk.W+tk.E)

        label_frequence = tk.Label(self.frame, text="Fréquence")
        label_frequence.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.input_frequence = tk.Entry(self.frame, width=10)
        self.input_frequence.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        label_amplitude = tk.Label(self.frame, text="Amplitude")
        label_amplitude.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.input_amplitude = tk.Entry(self.frame, width=10)
        self.input_amplitude.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.value_signal_sinusoidal = tk.BooleanVar()
        self.value_signal_continu = tk.BooleanVar()

        self.radio_signal_sinusoidal = tk.Checkbutton(
            self.frame,
            text="Signal sinusoïdal",
            variable=self.value_signal_sinusoidal,
            onvalue=True,
            offvalue=False,
            command=self.on_signal_sinusoidal
        )
        self.radio_signal_sinusoidal.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.radio_signal_continu = tk.Checkbutton(
            self.frame,
            text="Signal continu    ",
            variable=self.value_signal_continu,
            onvalue=True,
            offvalue=False,
            command=self.on_signal_continu
        )
        self.radio_signal_continu.grid(row=4, column=0, sticky="ew", padx=5)

        self.figure_sinusoidal = plt.Figure(figsize=(12, 4))
        self.subplot_sinusoidal = self.figure_sinusoidal.add_subplot(1, 1, 1)
        self.subplot_sinusoidal.set_title ("Signal sinusoïdal", loc='right')
        self.subplot_sinusoidal.set_ylabel("Amplitude")
        self.subplot_sinusoidal.set_xlabel("Fréquence (Hz)")
        self.subplot_sinusoidal.set_ylim

        self.canvas_sinusoidal = FigureCanvasTkAgg(self.figure_sinusoidal, master=self.frame_diagrame_sinusoidal)
        self.canvas_sinusoidal.get_tk_widget().pack()

        self.figure_continu = plt.Figure(figsize=(12, 4))
        self.subplot_continu = self.figure_continu.add_subplot(1, 1, 1)
        self.subplot_continu.set_title ("Signal Continu", loc='right')
        self.subplot_continu.set_ylabel("Amplitude")
        self.subplot_continu.set_xlabel("Fréquence (Hz)")
        
        self.canvas_continu = FigureCanvasTkAgg(self.figure_continu, master=self.frame_diagrame_continu)
        self.canvas_continu.get_tk_widget().pack()

    
    def on_signal_sinusoidal(self):
        if self.value_signal_sinusoidal.get():
            self.calcul_echantillonage_signal_sinusoidal()
        else:
            self.effacer_graphe_sinusoidal()
    
    def calcul_echantillonage_signal_sinusoidal(self):
        try:
            frequence, amplitude = self.obtenir_frequence_amplitude()
            
            # Échantillonnage du signal
            Te = 0.1  # Période d'échantillonnage en seconde
            Duree = 1  # Durée du signal en secondes

            N = int(Duree/Te) + 1  # Nombre de points du signal échantillonné
            t = np.linspace(0, Duree, N)  # Temps des échantillons

            s = self.calcul_signal(t, frequence, amplitude)
            self.construire_graphe_sinusoidal(t, s)
        except Exception as e:
            print("Une erreur c'est produite")
    

    def construire_graphe_sinusoidal(self, t, a):
        self.frame_diagrame_sinusoidal.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.subplot_sinusoidal.scatter(t, a, color='orange')
        self.subplot_sinusoidal.invert_yaxis()
        self.subplot_sinusoidal.grid()
        self.canvas_sinusoidal.draw()


    def effacer_graphe_sinusoidal(self):
        self.frame_diagrame_sinusoidal.grid_forget()
    
    
    def on_signal_continu(self):
        if self.value_signal_continu.get():
            self.calcul_echantillonage_signal_continu()
        else:
            self.effacer_graphe_continu()

    
    def calcul_echantillonage_signal_continu(self):
        try:
            frequence, amplitude = self.obtenir_frequence_amplitude()
            
            # Période du signal
            T = 1 / frequence
            # Durée du signal
            D = 5 * T
            # Nombre d'échantillons
            N = 1000

            # Génération du signal
            t = np.linspace(0, D, N)
            s = self.calcul_signal(t, frequence, amplitude)
            
            # Calcul des coefficients de la série de Fourier
            S = np.fft.fft(s) / N

            # Fréquences associées aux coefficients de la série de Fourier
            f = np.fft.fftfreq(N, d = t[1] - t[0])
        
            self.construire_signal_continu(f, np.abs(S))
            
        except Exception as e:
            print("Une erreur c'est produite")

    
    def obtenir_frequence_amplitude(self):
        frequence = 1
        amplitude = 1
        try:
            if (self.input_frequence.get().strip() != ""):
                frequence = int(self.input_frequence.get())
            if (self.input_amplitude.get().strip() != ""):
                amplitude = int(self.input_amplitude.get())
        except:
            pass

        return frequence, amplitude
    
    
    def calcul_signal(self, t, f = 1, A = 1):
        # Calcul du signal x(t) = A*sin(2*pi*f*t)
        return A*np.sin(2*np.pi*f*t)


    def construire_signal_continu(self, f, a):
        self.frame_diagrame_continu.grid(row=1, column=1, sticky=tk.W+tk.E)
        self.subplot_continu.plot(f, np.abs(a), color="blue")
        self.subplot_continu.grid()
        self.canvas_continu.draw()

    
    def effacer_graphe_continu(self):
        self.frame_diagrame_continu.grid_forget()

    def montrer_fenetre(self):
        self.fenetre.mainloop()


if __name__=="__main__":
    fourrier = TransformeeFourrier()
    fourrier.montrer_fenetre()