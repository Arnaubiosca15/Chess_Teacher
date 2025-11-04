# src/chess_teacher/__main__.py
import tkinter as tk
from chess_teacher.core.game_controller import GameController
from chess_teacher.ui.gui import ChessGUI

def main():
    print("=== Chess Teacher ===")
    try:
        skill = int(input("Elige nivel de Stockfish (0–20): "))
        skill = max(0, min(20, skill))
    except ValueError:
        skill = 10

    controller = GameController(skill_level=skill)

    root = tk.Tk()
    gui = ChessGUI(root, controller)
    root.mainloop()

    controller.quit()

if __name__ == "__main__":
    main()
