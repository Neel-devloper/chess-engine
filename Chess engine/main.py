import pygame
import chess
import chess_engine

# Initialize Pygame to set up its internal components for graphics, sound, and input handling
pygame.init()

THEMES = [
    ((240, 217, 181), (181, 136, 99)),  # Classic
    ((255, 255, 255), (0, 0, 0)),  # Black & White
    ((200, 200, 255), (100, 100, 200)),  # Cool Blue
    ((255, 228, 196), (139, 69, 19)),  # Brown
    ((152, 251, 152), (34, 139, 34)),  # Green
    ((255, 192, 203), (255, 105, 180)),  # Pink
    ((255, 255, 224), (128, 128, 0)),  # Yellow Olive
    ((173, 216, 230), (0, 191, 255)),  # Sky Blue
    ((211, 211, 211), (105, 105, 105)),  # Grey
    ((255, 250, 240), (160, 82, 45))  # Antique White and Saddle Brown
]

theme_index = 0
SQUARE_SIZE = 100
SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()
LIGHT_COLOR, DARK_COLOR = THEMES[theme_index]

PIECE_TYPES = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
IMAGES = {}



for color in ['white', 'black']:
    for piece in PIECE_TYPES:
        if color == 'white':
          # replace this with your own path to the images (white images here)
            path_map = {
                'pawn': 'Chess engine/white pawn.png',
                'rook': 'Chess engine/white rook.png',
                'knight': 'Chess engine/white knight.png',
                'bishop': 'Chess engine/white bishop.png',
                'queen': 'Chess engine/white queen.png',
                'king': 'Chess engine/white king.png'
            }
        else:
          # replace this with your own path to the iamges (black images here)
            path_map = {
                'pawn': 'Chess engine/black pawn.png',
                'rook': 'Chess engine/black rook.png',
                'knight': 'Chess engine/black knight.png',
                'bishop': 'Chess engine/black bishop.png',
                'queen': 'Chess engine/black queen.png',
                'king': 'Chess engine/black king.png'
            }
        IMAGES[(color, piece)] = pygame.transform.scale(pygame.image.load(path_map[piece]), (SQUARE_SIZE, SQUARE_SIZE))

BOARD = chess.Board()
SELECTED_SQUARE = None
running = True
chess_ai = chess_engine.NV_Chess_engine(BOARD)
winner = None


# New function to highlight legal moves
def draw_legal_moves(screen, board, selected_square, square_size):
    if selected_square is None:
        return

    for move in board.legal_moves:
        if move.from_square == selected_square:
            # Calculate screen position
            to_square = move.to_square
            board_row = 7 - (to_square // 8)
            board_col = to_square % 8
            x = board_col * square_size + square_size // 2
            y = board_row * square_size + square_size // 2

            # Draw circle indicator
            pygame.draw.circle(screen, (0, 255, 0, 128), (x, y), 10)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle both white and black turns with mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            screen_col = pos[0] // SQUARE_SIZE
            screen_row = pos[1] // SQUARE_SIZE
            board_row = 7 - screen_row
            board_col = screen_col
            square = board_row * 8 + board_col
            piece = BOARD.piece_at(square)

            # Only allow moves for current player
            if (BOARD.turn == chess.WHITE and piece and piece.color == chess.WHITE) or \
                    (BOARD.turn == chess.BLACK and piece and piece.color == chess.BLACK):
                # If clicking on own piece
                if SELECTED_SQUARE == square:
                    # Deselect if clicking selected piece again
                    SELECTED_SQUARE = None
                else:
                    # Select new piece
                    SELECTED_SQUARE = square
            else:
                # Attempt to move to empty square or capture
                if SELECTED_SQUARE is not None:
                    from_square = SELECTED_SQUARE
                    to_square = square
                    piece = BOARD.piece_at(from_square)

                    # Handle pawn promotion
                    if piece and piece.piece_type == chess.PAWN:
                        # White pawn reaching 8th rank or black pawn reaching 1st rank
                        if (piece.color == chess.WHITE and to_square // 8 == 7) or \
                                (piece.color == chess.BLACK and to_square // 8 == 0):
                            move = chess.Move(from_square, to_square, promotion=chess.QUEEN)
                        else:
                            move = chess.Move(from_square, to_square)
                    else:
                        move = chess.Move(from_square, to_square)

                    # Validate and make move
                    if move in BOARD.legal_moves:
                        BOARD.push(move)
                        SELECTED_SQUARE = None

                        # If it's black's turn after white moves (or vice versa)
                        if BOARD.turn == chess.BLACK:
                            time_taken = chess_ai.black_move(BOARD)
                    else:
                        # Invalid move - deselect
                        SELECTED_SQUARE = None

        elif event.type == pygame.KEYDOWN:
            if pygame.K_0 <= event.key <= pygame.K_9:
                theme_index = event.key - pygame.K_0
                if theme_index >= len(THEMES):
                    theme_index = 0

    LIGHT_COLOR, DARK_COLOR = THEMES[theme_index]

    # Draw the chessboard by iterating over all rows and columns
    for screen_row in range(8):
        for screen_col in range(8):
            x = screen_col * SQUARE_SIZE
            y = screen_row * SQUARE_SIZE
            board_row = 7 - screen_row
            board_col = screen_col
            color = LIGHT_COLOR if (board_row + board_col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(SCREEN, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

            # Highlight selected square
            if SELECTED_SQUARE is not None:
                selected_row = 7 - (SELECTED_SQUARE // 8)
                selected_col = SELECTED_SQUARE % 8
                if selected_row == screen_row and selected_col == screen_col:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    highlight.set_alpha(100)
                    highlight.fill((0, 255, 255))
                    SCREEN.blit(highlight, (x, y))

            square = board_row * 8 + board_col
            piece = BOARD.piece_at(square)
            if piece:
                color = 'white' if piece.color else 'black'
                piece_type = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king'][piece.piece_type - 1]
                SCREEN.blit(IMAGES[(color, piece_type)], (x, y))

    # Draw legal move indicators
    draw_legal_moves(SCREEN, BOARD, SELECTED_SQUARE, SQUARE_SIZE)

    # Game over detection
    if winner:
        # Create a semi-transparent overlay
        overlay = pygame.Surface((800, 800))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        SCREEN.blit(overlay, (0, 0))
        
        # Winner announcement
        winner_font = pygame.font.Font('freesansbold.ttf', 48)
        winner_text = winner_font.render(f'{winner.upper()} WINS!', True, (255, 215, 0))  # Gold color
        winner_rect = winner_text.get_rect()
        winner_rect.center = (400, 350)
        
        # Winner background
        winner_bg = pygame.Rect(winner_rect.left - 30, winner_rect.top - 20, 
                               winner_rect.width + 60, winner_rect.height + 40)
        pygame.draw.rect(SCREEN, (30, 30, 30), winner_bg, border_radius=20)
        pygame.draw.rect(SCREEN, (255, 215, 0), winner_bg, width=3, border_radius=20)
        
        # Subtitle
        subtitle_font = pygame.font.Font('freesansbold.ttf', 24)
        subtitle_text = subtitle_font.render('Game Over', True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect()
        subtitle_rect.center = (400, 420)
        
        SCREEN.blit(winner_text, winner_rect)
        SCREEN.blit(subtitle_text, subtitle_rect)
        running = False
        break
    

    if BOARD.is_stalemate():
        # Create a semi-transparent overlay
        overlay = pygame.Surface((800, 800))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        SCREEN.blit(overlay, (0, 0))
        
        # Draw announcement
        draw_font = pygame.font.Font('freesansbold.ttf', 36)
        draw_text = draw_font.render('DRAW!', True, (255, 165, 0))  # Orange color
        draw_rect = draw_text.get_rect()
        draw_rect.center = (400, 350)
        
        # Draw background
        draw_bg = pygame.Rect(draw_rect.left - 30, draw_rect.top - 20, 
                             draw_rect.width + 60, draw_rect.height + 40)
        pygame.draw.rect(SCREEN, (30, 30, 30), draw_bg, border_radius=20)
        pygame.draw.rect(SCREEN, (255, 165, 0), draw_bg, width=3, border_radius=20)
        
        # Reason
        reason_font = pygame.font.Font('freesansbold.ttf', 20)
        reason_text = reason_font.render('Stalemate', True, (200, 200, 200))
        reason_rect = reason_text.get_rect()
        reason_rect.center = (400, 400)
        
        SCREEN.blit(draw_text, draw_rect)
        SCREEN.blit(reason_text, reason_rect)
        running = False
        break

    elif BOARD.is_insufficient_material():
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f'The Game is a draw due to insufficient material!', True, (255, 0, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (400, 400)
        SCREEN.blit(text, textRect)
        running = False
        break

    elif BOARD.is_fivefold_repetition():
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f'The Game is a draw due to fivefold repetition!', True, (255, 0, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (400, 400)
        SCREEN.blit(text, textRect)
        running = False
        break

    elif BOARD.is_seventyfive_moves():
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f'The Game is a draw due to seventyfive moves!', True, (255, 0, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (400, 400)
        SCREEN.blit(text, textRect)
        running = False
        break

    elif BOARD.is_repetition():
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f'The Game is a draw due to repetition!', True, (255, 0, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (400, 400)
        SCREEN.blit(text, textRect)
        running = False
        break

    elif BOARD.is_fifty_moves():
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f'The Game is a draw due to fifty moves!', True, (255, 0, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (400, 400)
        SCREEN.blit(text, textRect)
        running = False
        break

    # Update the display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
