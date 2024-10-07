import tkinter as tk
from tkinter import messagebox
from src.run_detection import run_timer
from src.press_detection import count_reps
from src.visualization import close_window
import cv2

class TicTacToe():
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("350x450")  # Aumentamos el tamaño para incluir las vidas
        self.root.resizable(False, False)
        self.current_player = "X"
        self.lives_X = 3  # Vidas del jugador X
        self.lives_O = 3  # Vidas del jugador O
        self.board = [" " for _ in range(9)]
        self.buttons = [None] * 9
        self.create_buttons()
        self.set_style()

    def create_buttons(self):
        for i in range(9):
            self.buttons[i] = tk.Button(self.root, text=" ", font=("Arial", 24), width=5, height=2,
                                         command=lambda i=i: self.make_move(i), bg="#ffffff", activebackground="#f0f0f0")
            self.buttons[i].grid(row=i // 3 + 2, column=i % 3, padx=5, pady=5)

    def set_style(self):
        self.root.configure(bg="#fffbf4")
        title = tk.Label(self.root, text="Tic Tac Toe", font=("Arial", 20), bg="#fffbf4", fg="#00101d")
        title.grid(row=0, columnspan=3, pady=10)

        # Mostrar las vidas
        self.lives_label_X = tk.Label(self.root, text=f"Vidas X: {self.lives_X}", font=("Arial", 14), bg="#fffbf4", fg="#00101d")
        self.lives_label_X.grid(row=1, column=0)

        self.lives_label_O = tk.Label(self.root, text=f"Vidas O: {self.lives_O}", font=("Arial", 14), bg="#fffbf4", fg="#00101d")
        self.lives_label_O.grid(row=1, column=2)

    def update_lives(self):
        """ Actualizar las vidas en pantalla """
        self.lives_label_X.config(text=f"Vidas X: {self.lives_X}")
        self.lives_label_O.config(text=f"Vidas O: {self.lives_O}")

    def make_move(self, index):
        if self.board[index] == " ":
            self.board[index] = self.current_player
            color = "#087cff" if self.current_player == "X" else "#b60f00"
            self.buttons[index].config(text=self.current_player, bg=color, fg="#fffbf4")
            if self.check_winner():
                self.handle_winner(self.current_player)  # Manejar la pérdida de vida del jugador
            elif " " not in self.board:
                messagebox.showinfo("Empate", "¡Es un empate!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return True
        return False

    def handle_winner(self, winner):
        """ Manejar la lógica de pérdida de vidas cuando alguien gana """
        loser = "X" if winner == "O" else "O"

        # El jugador perdedor pierde una vida
        if loser == "X":
            self.lives_X -= 1
        else:
            self.lives_O -= 1
        
        self.update_lives()

        # Verificar si el jugador ha perdido todas las vidas
        if self.lives_X == 0:
            messagebox.showinfo("Juego terminado", "El jugador O ha ganado el juego.")
            self.root.quit()  # Termina el juego
        elif self.lives_O == 0:
            messagebox.showinfo("Juego terminado", "El jugador X ha ganado el juego.")
            self.root.quit()  # Termina el juego
        else:
            self.show_exercise_options(loser)

    def show_exercise_options(self, loser):
        """ Crear una nueva ventana emergente para elegir entre 'Corre' y 'Military Press' """
        exercise_window = tk.Toplevel(self.root)
        exercise_window.title("Elige tu ejercicio")
        exercise_window.geometry("300x150")
        exercise_window.resizable(False, False)

        message = tk.Label(exercise_window, text=f"El jugador {loser} ha perdido.\nElige tu castigo:", font=("Arial", 14))
        message.pack(pady=10)

        corre_button = tk.Button(exercise_window, text="Corre", font=("Arial", 14), width=10,
                                 command=lambda: self.select_exercise("Corre", exercise_window))
        corre_button.pack(side=tk.LEFT, padx=20)

        military_button = tk.Button(exercise_window, text="Military Press", font=("Arial", 14), width=12,
                                    command=lambda: self.select_exercise("Military Press", exercise_window))
        military_button.pack(side=tk.RIGHT, padx=20)

    def select_exercise(self, exercise, window):
        """ Manejar la selección del ejercicio y cerrar la ventana """
        messagebox.showinfo("Ejercicio Seleccionado", f"¡Prepárate para {exercise}!")
        window.destroy()

        # Iniciar el ejercicio seleccionado
        self.start_exercise(exercise)

    def start_exercise(self, exercise):
        """Iniciar el ejercicio seleccionado y reiniciar el Tic Tac Toe después"""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            return  # Evitar continuar si no hay cámara

        if exercise == "Corre":
            print("Iniciando detección de correr en caminadora...")
            run_timer(cap)
        elif exercise == "Military Press":
            print("Iniciando detección de military press...")
            count_reps(cap)

        cap.release()
        close_window()

        self.reset_game()

    def reset_game(self):
        """Reiniciar el tablero pero mantener las vidas y el jugador actual"""
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ", bg="#ffffff", fg="black")  # Restablecer el color


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
