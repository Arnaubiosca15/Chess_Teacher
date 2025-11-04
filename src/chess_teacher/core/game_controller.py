# src/chess_teacher/core/game_controller.py
import chess
from chess_teacher.engine.stockfish_engine import StockfishEngine


class GameController:
    def __init__(self, skill_level=10, elo=None):
        self.board = chess.Board()
        self.engine = StockfishEngine(skill=skill_level, elo=elo)

    def get_board(self):
        return self.board

    def player_move(self, move_uci: str):
        """Aplica el movimiento del jugador humano (en UCI, ej. 'e2e4')."""
        move = chess.Move.from_uci(move_uci)
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def ai_move(self):
        """Hace que el motor juegue su movimiento."""
        move = self.engine.get_best_move(self.board)
        if move:
            self.board.push(move)
        return move

    def quit(self):
        self.engine.quit()
