import os
import tkinter as tk
from PIL import Image, ImageTk
import chess
from chess_teacher.core.game_controller import GameController

TILE_SIZE = 80


class ChessGUI:
    def __init__(self, master, controller: GameController):
        self.master = master
        self.controller = controller
        self.board = controller.get_board()

        self.master.title("Chess Teacher ♟️")
        self.master.configure(bg="#2E2E2E")

        self.board_size = 8 * TILE_SIZE
        window_size = self.board_size + 60
        self.master.geometry(f"{window_size}x{window_size}")

        self.canvas = tk.Canvas(
            master,
            width=self.board_size,
            height=self.board_size,
            highlightthickness=0,
            bg="#2E2E2E",
        )
        self.canvas.pack(padx=30, pady=30)

        self.images = {}
        self.load_images()
        self.selected_square = None
        self.draw_board()

        self.canvas.bind("<Button-1>", self.on_click)

    def load_images(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "pieces")
        base_path = os.path.abspath(base_path)

        pieces = ["r", "n", "b", "q", "k", "p", "R", "N", "B", "Q", "K", "P"]
        for piece in pieces:
            img_path = os.path.join(base_path, f"{piece}.png")
            if not os.path.exists(img_path):
                print(f"⚠️ No se encontró la imagen: {img_path}")
                continue
            img = Image.open(img_path).resize((TILE_SIZE, TILE_SIZE))
            self.images[piece] = ImageTk.PhotoImage(img)

    def draw_board(self):
        self.canvas.delete("all")

        light_color = "#EDEBD7"
        dark_color = "#595959"
        highlight_color = "#D7B43E"

        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)

                # Color base
                color = light_color if (row + col) % 2 == 0 else dark_color

                # Casilla seleccionada → dorado
                if self.selected_square == square:
                    color = highlight_color

                x1, y1 = col * TILE_SIZE, row * TILE_SIZE
                self.canvas.create_rectangle(
                    x1, y1, x1 + TILE_SIZE, y1 + TILE_SIZE, fill=color, outline=color
                )

        # Dibujar piezas
        for square, piece in self.board.piece_map().items():
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            symbol = piece.symbol()
            if symbol in self.images:
                self.canvas.create_image(
                    col * TILE_SIZE,
                    row * TILE_SIZE,
                    image=self.images[symbol],
                    anchor="nw",
                )

    def on_click(self, event):
        col = event.x // TILE_SIZE
        row = 7 - (event.y // TILE_SIZE)
        square = chess.square(col, row)

        # Si no hay selección, selecciona
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.draw_board()  # 👈 Redibuja para ver el color inmediatamente
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                # Movimiento jugador
                self.controller.player_move(move.uci())
                self.selected_square = None  # limpia la selección antes del redraw
                self.draw_board()

                # Movimiento IA
                self.master.after(100, self.make_ai_move)
            else:
                # Si no era válido, deselecciona
                self.selected_square = None
                self.draw_board()

    def make_ai_move(self):
        ai_move = self.controller.ai_move()
        if ai_move:
            print("Stockfish juega:", ai_move)
        self.draw_board()
