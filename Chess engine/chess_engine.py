import chess
import time

class NV_Chess_engine: # name of the chess engine
    def __init__(self,board):
        self.board = board

    def get_game_phase(self, board):
        phase_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.piece_type in [chess.ROOK, chess.QUEEN]:
                    phase_score += 2
                elif piece.piece_type in [chess.BISHOP, chess.KNIGHT]:
                    phase_score += 1
        return 'opening' if phase_score > 12 else 'midgame' if phase_score > 6 else 'endgame'

    def evaluate_position(self, board):
        # Material values in centipawns, keyed by chess piece constants
        piece_vals = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0
        }

        # Simplified piece-square tables for white; black uses mirror
        pst = {
            chess.PAWN: [
                 0,  5,  5, -10,-10,  5,  5,  0,
                 5, 10, 10,   0,  0, 10, 10,  5,
                 5, 10, 20,  20, 20, 20, 10,  5,
                 0,  0, 20,  25, 25, 20,  0,  0,
                 5,  5, 10,  20, 20, 10,  5,  5,
                 5, 10, 10, -20,-20, 10, 10,  5,
                 5, 10, 10, -30,-30, 10, 10,  5,
                 0,  0,  0,   0,  0,  0,  0,  0
            ],
            chess.KNIGHT: [
                -50,-40,-30,-30,-30,-30,-40,-50,
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50
            ],
            chess.BISHOP: [
                -20,-10,-10,-10,-10,-10,-10,-20,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -20,-10,-10,-10,-10,-10,-10,-20
            ],
            chess.ROOK: [
                 0,  0,  5, 10, 10,  5,  0,  0,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                 5, 10, 10, 10, 10, 10, 10,  5,
                 0,  0,  0,  0,  0,  0,  0,  0
            ],
            chess.QUEEN: [
                -20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                 -5,  0,  5,  5,  5,  5,  0, -5,
                  0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20
            ],
            chess.KING: [
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                 20, 20,  0,  0,  0,  0, 20, 20,
                 20, 30, 10,  0,  0, 10, 30, 20
            ]
        }

        phase = self.get_game_phase(board)

        # Endgame king PST adjustment
        if phase == 'endgame':
            pst[chess.KING] = [
                 -50,-40,-30,-20,-20,-30,-40,-50,
                 -30,-20,-10,  0,  0,-10,-20,-30,
                 -30,-10, 20, 30, 30, 20,-10,-30,
                 -30,-10, 30, 40, 40, 30,-10,-30,
                 -30,-10, 30, 40, 40, 30,-10,-30,
                 -30,-10, 20, 30, 30, 20,-10,-30,
                 -30,-30,  0,  0,  0,  0,-30,-30,
                 -50,-30,-30,-30,-30,-30,-30,-50
            ]

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_vals[piece.piece_type]
                psq = pst[piece.piece_type][square if piece.color == chess.WHITE else chess.square_mirror(square)]
                total = value + psq
                score += total if piece.color == chess.WHITE else -total

        # Mobility (simple)
        white_mobility = len([m for m in board.legal_moves if board.color_at(m.from_square) == chess.WHITE])
        board.push(chess.Move.null())  # switch turn
        black_mobility = len([m for m in board.legal_moves if board.color_at(m.from_square) == chess.BLACK])
        board.pop()
        score += 10 * (white_mobility - black_mobility)

        # Attacks/defenses bonus
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue

            # enemy pieces attacking this square
            enemy_attackers = board.attackers(not piece.color, square)
            # friendly pieces defending this square
            friendly_defenders = board.attackers(piece.color, square)

            for attacker_sq in enemy_attackers:
                attacker_piece = board.piece_at(attacker_sq)
                if attacker_piece:
                    target_value = piece_vals[piece.piece_type]
                    bonus = int(target_value * 0.1)  # 10% of target piece value
                    score += bonus if attacker_piece.color == chess.WHITE else -bonus

            for defender_sq in friendly_defenders:
                defender_piece = board.piece_at(defender_sq)
                if defender_piece:
                    support_bonus = 5
                    score += support_bonus if defender_piece.color == chess.WHITE else -support_bonus

        return score

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board)

        legal_moves = list(board.legal_moves)
        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval_val = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                if eval_val > max_eval:
                    max_eval = eval_val
                if eval_val > alpha:
                    alpha = eval_val
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval_val = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                if eval_val < min_eval:
                    min_eval = eval_val
                if eval_val < beta:
                    beta = eval_val
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def black_move(self, board):
        # Update internal board to match the current game state
        self.board = board
        start_time = time.time()

        print('Computer Calculating Move...')
        best_score = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score = self.minimax(board, 3, float('-inf'), float('inf'), True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
        
        if best_move:
            board.push(best_move)
            print(f'Move played : {best_move}')
            end_time = time.time()
            time_taken = end_time - start_time
            print(f'Time taken: {time_taken} seconds')
            print('------')
            return time_taken
        else:
            # No legal moves available (shouldn't happen in normal chess)
            end_time = time.time()
            time_taken = end_time - start_time
            print('No legal moves available')
            print(f'Time taken: {time_taken} seconds')
            print('------')
            return time_taken