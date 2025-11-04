# src/chess_teacher/engine/stockfish_engine.py
import chess
import chess.engine
import os

class StockfishEngine:
    def __init__(self, path=None, skill=10, elo=None):
        if path is None:
            # Ruta por defecto (ajústala a tu sistema)
            path = "/usr/games/stockfish"

        self.engine = chess.engine.SimpleEngine.popen_uci(path)

        # Configuración básica
        config = {
            "Threads": 2,
            "Hash": 256,
            "Skill Level": skill,
        }

        # Si se especifica un ELO, activamos el modo limitado
        if elo:
            config["UCI_LimitStrength"] = True
            config["UCI_Elo"] = elo

        self.engine.configure(config)

    def get_best_move(self, board, time_limit=0.5):
        """Devuelve el mejor movimiento según el motor."""
        result = self.engine.play(board, chess.engine.Limit(time=time_limit))
        return result.move

    def analyse_position(self, board, time_limit=0.5):
        """Devuelve una evaluación numérica (en centipawns)."""
        info = self.engine.analyse(board, chess.engine.Limit(time=time_limit))
        return info.get("score")

    def quit(self):
        self.engine.quit()
