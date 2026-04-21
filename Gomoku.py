import pygame
import sys
import math
import time
import threading

BOARD_SIZE = 15
CELL_SIZE = 50
MARGIN = 40
WIDTH = CELL_SIZE * (BOARD_SIZE - 1) + MARGIN * 2
HEIGHT = WIDTH + 60

BG_COLOR = (222, 184, 135)
LINE_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

EMPTY = 0
BLACK_STONE = 1
WHITE_STONE = 2

POSITION_WEIGHT = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        d = max(abs(i - 7), abs(j - 7))
        POSITION_WEIGHT[i][j] = max(0, 14 - d * 2)

SCORES = {
    (5, 0): 10000000, (5, 1): 10000000, (5, 2): 10000000,
    (4, 0): 500000,   (4, 1): 50000,
    (3, 0): 50000,    (3, 1): 5000,
    (2, 0): 5000,     (2, 1): 500,
    (1, 0): 500,      (1, 1): 50
}

MAX_DEPTH = 4
MAX_CANDIDATES = 20

class Gomoku:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK_STONE
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.history_table = {}

    def drop_piece(self, row, col, player):
        if self.board[row][col] == EMPTY:
            self.board[row][col] = player
            self.last_move = (row, col)
            if self.check_win(row, col, player):
                self.game_over = True
                self.winner = player
            elif self.is_board_full():
                self.game_over = True
                self.winner = EMPTY
            return True
        return False

    def is_board_full(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY:
                    return False
        return True

    def check_win(self, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False

    def get_candidates(self):
        candidates = set()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] != EMPTY:
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board[nr][nc] == EMPTY:
                                candidates.add((nr, nc))
        if not candidates:
            candidates.add((BOARD_SIZE // 2, BOARD_SIZE // 2))
        
        scored = []
        for r, c in candidates:
            white_score = self.evaluate_point(r, c, WHITE_STONE)
            black_score = self.evaluate_point(r, c, BLACK_STONE)
            total_score = white_score + black_score + POSITION_WEIGHT[r][c]
            scored.append((total_score, r, c))
        scored.sort(reverse=True)
        return [(r, c) for _, r, c in scored[:MAX_CANDIDATES]]

    def evaluate_point(self, row, col, player):
        opponent = WHITE_STONE if player == BLACK_STONE else BLACK_STONE
        total_score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            block = 0
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE) or self.board[r][c] == opponent:
                block += 1
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE) or self.board[r][c] == opponent:
                block += 1
            
            if block == 2 and count < 5:
                continue
            count = min(count, 5)
            total_score += SCORES.get((count, block), 0)
        return total_score

    def evaluate_board(self):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY:
                    continue
                    
                player = self.board[r][c]
                pos_weight = POSITION_WEIGHT[r][c] if player == WHITE_STONE else -POSITION_WEIGHT[r][c]
                score += pos_weight
                
                for dr, dc in directions:
                    pr, pc = r - dr, c - dc
                    if 0 <= pr < BOARD_SIZE and 0 <= pc < BOARD_SIZE and self.board[pr][pc] == player:
                        continue
                        
                    count = 0
                    nr, nc = r, c
                    while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board[nr][nc] == player:
                        count += 1
                        nr += dr
                        nc += dc
                        
                    block = 0
                    if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE) or self.board[nr][nc] != EMPTY:
                        block += 1
                    if not (0 <= pr < BOARD_SIZE and 0 <= pc < BOARD_SIZE) or self.board[pr][pc] != EMPTY:
                        block += 1
                        
                    if block == 2 and count < 5:
                        continue
                        
                    count = min(count, 5)
                    val = SCORES.get((count, block), 0)
                    score += val if player == WHITE_STONE else -val
        return score

    def sort_moves(self, candidates, is_maximizing):
        scored = []
        player = WHITE_STONE if is_maximizing else BLACK_STONE
        for r, c in candidates:
            base_score = self.evaluate_point(r, c, player) + POSITION_WEIGHT[r][c]
            history_score = self.history_table.get((r, c), 0)
            scored.append((base_score + history_score, r, c))
        scored.sort(reverse=True)
        return [(r, c) for _, r, c in scored]

    def minimax(self, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.game_over:
            return self.evaluate_board()

        candidates = self.get_candidates()
        candidates = self.sort_moves(candidates, is_maximizing)

        if is_maximizing:
            max_score = -math.inf
            for r, c in candidates:
                self.board[r][c] = WHITE_STONE
                if self.check_win(r, c, WHITE_STONE):
                    self.board[r][c] = EMPTY
                    return 10000000 + depth
                
                score = self.minimax(depth - 1, alpha, beta, False)
                self.board[r][c] = EMPTY
                
                if score > max_score:
                    max_score = score
                    self.history_table[(r, c)] = self.history_table.get((r, c), 0) + depth * depth
                    
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = math.inf
            for r, c in candidates:
                self.board[r][c] = BLACK_STONE
                if self.check_win(r, c, BLACK_STONE):
                    self.board[r][c] = EMPTY
                    return -10000000 - depth
                
                score = self.minimax(depth - 1, alpha, beta, True)
                self.board[r][c] = EMPTY
                
                if score < min_score:
                    min_score = score
                    self.history_table[(r, c)] = self.history_table.get((r, c), 0) + depth * depth
                    
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score

    def get_best_move(self):
        candidates = self.get_candidates()
        best_move = None
        best_score = -math.inf

        for r, c in candidates:
            self.board[r][c] = WHITE_STONE
            if self.check_win(r, c, WHITE_STONE):
                self.board[r][c] = EMPTY
                return (r, c)
            self.board[r][c] = EMPTY

        for r, c in candidates:
            self.board[r][c] = BLACK_STONE
            if self.check_win(r, c, BLACK_STONE):
                self.board[r][c] = EMPTY
                return (r, c)
            self.board[r][c] = EMPTY

        start_time = time.time()

        for depth in range(1, MAX_DEPTH + 1):
            current_best_move = None
            current_best_score = -math.inf

            sorted_candidates = self.sort_moves(candidates, True)
            
            for r, c in sorted_candidates:
                self.board[r][c] = WHITE_STONE
                score = self.minimax(depth - 1, -math.inf, math.inf, False)
                self.board[r][c] = EMPTY
                if score > current_best_score:
                    current_best_score = score
                    current_best_move = (r, c)
            
            if current_best_score >= 10000000:
                return current_best_move
                
            best_move = current_best_move
            best_score = current_best_score
            
            if time.time() - start_time > 2.0:
                break

        return best_move

def get_font(size):
    available_fonts = pygame.font.get_fonts()
    cjk_fonts = ['simhei', 'microsoftyahei', 'pingfang', 'heiti', 'notosanssc', 'wenquanyimicrohei']
    for font_name in cjk_fonts:
        if font_name in available_fonts:
            return pygame.font.SysFont(font_name, size)
    return pygame.font.Font(None, size)

def draw_board(screen, game, mouse_pos=None):
    screen.fill(BG_COLOR)
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, 
                         (MARGIN + i * CELL_SIZE, MARGIN), 
                         (MARGIN + i * CELL_SIZE, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE))
        pygame.draw.line(screen, LINE_COLOR, 
                         (MARGIN, MARGIN + i * CELL_SIZE), 
                         (MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, MARGIN + i * CELL_SIZE))
    stars = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
    for r, c in stars:
        pygame.draw.circle(screen, LINE_COLOR, (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE), 4)

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if game.board[r][c] != EMPTY:
                color = BLACK if game.board[r][c] == BLACK_STONE else WHITE
                border_color = WHITE if game.board[r][c] == BLACK_STONE else BLACK
                pos = (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE)
                pygame.draw.circle(screen, color, pos, CELL_SIZE // 2 - 2)
                pygame.draw.circle(screen, border_color, pos, CELL_SIZE // 2 - 2, 1)

    if mouse_pos and not game.game_over and game.current_player == BLACK_STONE:
        x, y = mouse_pos
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and game.board[row][col] == EMPTY:
            pos = (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
            shadow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surface, (0, 0, 0, 100), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            screen.blit(shadow_surface, (pos[0] - CELL_SIZE // 2, pos[1] - CELL_SIZE // 2))

    if game.last_move:
        r, c = game.last_move
        pos = (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE)
        pygame.draw.circle(screen, RED, pos, 5)

    font = get_font(24)
    if game.game_over:
        if game.winner == BLACK_STONE:
            text = font.render("黑棋(你) 胜！按R重开", True, RED)
        elif game.winner == WHITE_STONE:
            text = font.render("白棋(AI) 胜！按R重开", True, RED)
        else:
            text = font.render("平局！按R重开", True, RED)
    else:
        if game.current_player == BLACK_STONE:
            text = font.render("当前回合: 黑棋(你)", True, BLACK)
        else:
            text = font.render("当前回合: 白棋(AI思考中...)", True, BLACK)
    screen.blit(text, (MARGIN, HEIGHT - 45))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("五子棋 (优化版)")
    clock = pygame.time.Clock()
    game = Gomoku()
    mouse_pos = None
    
    ai_thread = None
    ai_move = None
    ai_done_event = threading.Event()
    ai_lock = threading.Lock()

    def ai_think():
        nonlocal ai_move
        move = game.get_best_move()
        with ai_lock:
            ai_move = move
        ai_done_event.set()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Gomoku()
                    ai_move = None
                    ai_done_event.clear()
                    if ai_thread and ai_thread.is_alive():
                        ai_thread.join()
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                if game.current_player == BLACK_STONE:
                    x, y = pygame.mouse.get_pos()
                    col = round((x - MARGIN) / CELL_SIZE)
                    row = round((y - MARGIN) / CELL_SIZE)
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        if game.drop_piece(row, col, BLACK_STONE):
                            if not game.game_over:
                                game.current_player = WHITE_STONE
                                ai_done_event.clear()
                                ai_thread = threading.Thread(target=ai_think)
                                ai_thread.daemon = True
                                ai_thread.start()

        if not game.game_over and game.current_player == WHITE_STONE and ai_done_event.is_set():
            with ai_lock:
                move = ai_move
                ai_move = None
            if move:
                game.drop_piece(move[0], move[1], WHITE_STONE)
                if not game.game_over:
                    game.current_player = BLACK_STONE
            ai_done_event.clear()

        draw_board(screen, game, mouse_pos)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
