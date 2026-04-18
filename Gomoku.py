import pygame
import sys

pygame.init()
BOARD_SIZE = 15
CELL_SIZE = 50
MARGIN = 50
PANEL_WIDTH = 280
WINDOW_WIDTH = MARGIN * 2 + (BOARD_SIZE - 1) * CELL_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = MARGIN * 2 + (BOARD_SIZE - 1) * CELL_SIZE
BOARD_PX = MARGIN * 2 + (BOARD_SIZE - 1) * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (220, 179, 92)
LINE_COLOR = (50, 50, 50)
HOVER_COLOR = (100, 100, 100, 80)
BTN_COLOR = (180, 140, 60)
BTN_HOVER = (210, 170, 80)
TEXT_COLOR = (40, 40, 40)
EMPTY = 0
BLACK_STONE = 1
WHITE_STONE = 2
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gomoku")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont("Microsoft YaHei", 36, bold=True)
font_medium = pygame.font.SysFont("Microsoft YaHei", 24)
font_small = pygame.font.SysFont("Microsoft YaHei", 18)

board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
game_over = False
winner = None
current_player = BLACK_STONE
hover_pos = None
last_move = None
move_count = 0

DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

def pos_to_pixel(row, col):
    return MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE

def pixel_to_pos(x, y):
    col = round((x - MARGIN) / CELL_SIZE)
    row = round((y - MARGIN) / CELL_SIZE)
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        px, py = pos_to_pixel(row, col)
        if abs(x - px) < CELL_SIZE // 2 and abs(y - py) < CELL_SIZE // 2:
            return row, col
    return None

def draw_board():
    screen.fill(BOARD_COLOR)
    for i in range(BOARD_SIZE):
        x_start = MARGIN
        x_end = MARGIN + (BOARD_SIZE - 1) * CELL_SIZE
        y = MARGIN + i * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (x_start, y), (x_end, y), 1)
    for i in range(BOARD_SIZE):
        y_start = MARGIN
        y_end = MARGIN + (BOARD_SIZE - 1) * CELL_SIZE
        x = MARGIN + i * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (x, y_start), (x, y_end), 1)
    stars = [(3, 3), (3, 7), (3, 11), (7, 3), (7, 7), (7, 11), (11, 3), (11, 7), (11, 11)]
    for r, c 在 stars:
        px, py = pos_to_pixel(r, c)
        pygame.draw.circle(screen, LINE_COLOR, (px, py), 4)

def draw_stones():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:
                px, py = pos_to_pixel(r, c)
                color = BLACK if board[r][c] == BLACK_STONE else WHITE
                pygame.draw.circle(screen, color, (px, py), CELL_SIZE // 2 - 2)
                if board[r][c] == WHITE_STONE:
                    pygame.draw.circle(screen, LINE_COLOR, (px, py), CELL_SIZE // 2 - 2, 1)
    if last_move:
        r, c = last_move
        px, py = pos_to_pixel(r, c)
        mark_color = WHITE if board[r][c] == BLACK_STONE else BLACK
        pygame.draw.circle(screen, mark_color, (px, py), 4)

def draw_hover():
    if hover_pos and not game_over and current_player == BLACK_STONE:
        r, c = hover_pos
        if board[r][c] == EMPTY:
            px, py = pos_to_pixel(r, c)
            s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw。circle(s, (0, 0, 0, 80), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            screen.blit(s, (px - CELL_SIZE // 2, py - CELL_SIZE // 2))

def draw_panel():
    panel_x = BOARD_PX
    pygame.draw.rect(screen, (200, 160, 70), (panel_x, 0, PANEL_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(screen, LINE_COLOR, (panel_x, 0), (panel_x, WINDOW_HEIGHT), 2)

    title = font_large.render("五子棋", True, TEXT_COLOR)
    screen.blit(title, (panel_x + (PANEL_WIDTH - title.get_width()) // 2, 35))

    if game_over:
        if winner == BLACK_STONE:
            msg = "黑棋获胜!"
        elif winner == WHITE_STONE:
            msg = "白棋获胜!"
        else:
            msg = "平局!"
        status = font_medium.render(msg, True, (200, 30, 30))
    else:
        if current_player == BLACK_STONE:
            status = font_medium.render("你的回合", True, TEXT_COLOR)
        else:
            status = font_medium.render("AI思考中...", True, (30, 30, 180))
    screen.blit(status, (panel_x + (PANEL_WIDTH - status.get_width()) // 2, 100))

    info = font_small.render(f"步数: {move_count}", True, TEXT_COLOR)
    screen.blit(info, (panel_x + (PANEL_WIDTH - info.get_width()) // 2, 155))

    btn_rect = pygame.Rect(panel_x + 40, 220, PANEL_WIDTH - 80, 55)
    mouse = pygame.mouse.get_pos()
    hovered = btn_rect.collidepoint(mouse)
    color = BTN_HOVER if hovered else BTN_COLOR
    pygame.draw.rect(screen, color, btn_rect, border_radius=8)
    pygame.draw.rect(screen, LINE_COLOR, btn_rect, 2, border_radius=8)
    btn_text = font_medium.render("重新开始", True, TEXT_COLOR)
    screen.blit(btn_text, (btn_rect.x + (btn_rect.width - btn_text.get_width()) // 2,
                           btn_rect.y + (btn_rect.height - btn_text.get_height()) // 2))

    pygame.draw.circle(screen, BLACK, (panel_x + 50, 340), 14)
    you_text = font_small.render("你 (黑棋)", True, TEXT_COLOR)
    screen.blit(you_text, (panel_x + 75, 332))

    pygame.draw.circle(screen, WHITE, (panel_x + 50, 390), 14)
    pygame.draw.circle(screen, LINE_COLOR, (panel_x + 50, 390), 14, 1)
    ai_text = font_small.render("AI (白棋)", True, TEXT_COLOR)
    screen.blit(ai_text, (panel_x + 75, 382))

    return btn_rect

def check_win(bd, player):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if bd[r][c] == player:
                for dr, dc in DIRECTIONS:
                    count = 1
                    for i in range(1, 5):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and bd[nr][nc] == player:
                            count += 1
                        else:
                            break
                    if count >= 5:
                        return True
    return False

def is_board_full(bd):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if bd[r][c] == EMPTY:
                return False
    return True

def evaluate_line(line, player):
    score = 0
    opp = 3 - player
    length = len(line)
    for window_len in [5, 6]:
        if length < window_len:
            continue
        for i in range(length - window_len + 1):
            window = line[i:i + window_len]
            if opp in window:
                continue
            p_count = window.count(player)
            if window_len == 5:
                if p_count == 5:
                    score += 1000000
                elif p_count == 4:
                    score += 10000
                elif p_count == 3:
                    score += 500
                elif p_count == 2:
                    score += 50
                elif p_count == 1:
                    score += 5
            elif window_len == 6:
                if p_count == 5:
                    score += 100000
                elif p_count == 4 and window[0] == 0 and window[-1] == 0:
                    score += 5000
                elif p_count == 3 and window[0] == 0 and window[-1] == 0:
                    score += 200
    return score

def evaluate_position(bd, player):
    score = 0
    opp = 3 - player
    lines = []
    for r in range(BOARD_SIZE):
        lines.append([bd[r][c] for c in range(BOARD_SIZE)])
    for c in range(BOARD_SIZE):
        lines.append([bd[r][c] for r in range(BOARD_SIZE)])
    for d in range(-(BOARD_SIZE - 1), BOARD_SIZE):
        diag = []
        for r in range(BOARD_SIZE):
            c = r - d
            if 0 <= c < BOARD_SIZE:
                diag.append(bd[r][c])
        if len(diag) >= 5:
            lines.append(diag)
    for d in range(-(BOARD_SIZE - 1), BOARD_SIZE):
        diag = []
        for r in range(BOARD_SIZE):
            c = d + (BOARD_SIZE - 1 - r)
            if 0 <= c < BOARD_SIZE:
                diag.append(bd[r][c])
        if len(diag) >= 5:
            lines.append(diag)
    for line in lines:
        score += evaluate_line(line, player)
        score -= evaluate_line(line, opp) * 1.1
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if bd[r][c] == player:
                dist = abs(r - 7) + abs(c - 7)
                score += max(0, 14 - dist)
            elif bd[r][c] == opp:
                dist = abs(r - 7) + abs(c - 7)
                score -= max(0, 14 - dist) * 0.5
    return score

def get_candidates(bd, radius=2):
    candidates = set()
    has_stone = False
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if bd[r][c] != EMPTY:
                has_stone = True
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and bd[nr][nc] == EMPTY:
                            candidates.add((nr, nc))
    if not has_stone:
        return [(7, 7)]
    return list(candidates)

def minimax(bd, depth, alpha, beta, maximizing, ai_player):
    opp = 3 - ai_player
    if check_win(bd, ai_player):
        return 10000000 + depth
    if check_win(bd, opp):
        return -10000000 - depth
    if is_board_full(bd):
        return 0
    if depth == 0:
        return evaluate_position(bd, ai_player)

    candidates = get_candidates(bd, 1)
    if not candidates:
        return 0

    def sort_key(pos):
        r, c = pos
        bd[r][c] = ai_player if maximizing else opp
        s = evaluate_position(bd, ai_player)
        bd[r][c] = EMPTY
        return s

    candidates.sort(key=sort_key, reverse=maximizing)
    candidates = candidates[:12]

    if maximizing:
        max_eval = float('-inf')
        for r, c in candidates:
            bd[r][c] = ai_player
            val = minimax(bd, depth - 1, alpha, beta, False, ai_player)
            bd[r][c] = EMPTY
            max_eval = max(max_eval, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for r, c in candidates:
            bd[r][c] = opp
            val = minimax(bd, depth - 1, alpha, beta, True, ai_player)
            bd[r][c] = EMPTY
            min_eval = min(min_eval, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval

def ai_move():
    global board, current_player, game_over, winner, last_move, move_count
    ai_player = WHITE_STONE
    opp = BLACK_STONE

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                board[r][c] = ai_player
                if check_win(board, ai_player):
                    last_move = (r, c)
                    move_count += 1
                    game_over = True
                    winner = ai_player
                    current_player = BLACK_STONE
                    return
                board[r][c] = EMPTY

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                board[r][c] = opp
                if check_win(board, opp):
                    board[r][c] = ai_player
                    last_move = (r, c)
                    move_count += 1
                    if check_win(board, ai_player):
                        game_over = True
                        winner = ai_player
                    current_player = BLACK_STONE
                    return
                board[r][c] = EMPTY

    candidates = get_candidates(board, 2)
    if not candidates:
        return

    best_score = float('-inf')
    best_moves = []
    depth = 2 if move_count > 3 else 1

    for r, c in candidates:
        board[r][c] = ai_player
        score = minimax(board, depth, float('-inf'), float('inf'), False, ai_player)
        board[r][c] = EMPTY
        if score > best_score:
            best_score = score
            best_moves = [(r, c)]
        elif score == best_score:
            best_moves.append((r, c))

    if best_moves:
        import random
        r, c = random.choice(best_moves)
        board[r][c] = ai_player
        last_move = (r, c)
        move_count += 1
        if check_win(board, ai_player):
            game_over = True
            winner = ai_player
        elif is_board_full(board):
            game_over = True
            winner = None
        current_player = BLACK_STONE

def reset_game():
    global board, game_over, winner, current_player, hover_pos, last_move, move_count
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    game_over = False
    winner = None
    current_player = BLACK_STONE
    hover_pos = None
    last_move = 无
    move_count = 0

def main():
    global hover_pos, current_player, game_over, winner, last_move, move_count

    ai_thinking = False

    while True:
        btn_rect = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                pos = pixel_to_pos(event.pos[0], event.pos[1])
                hover_pos = pos
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pixel_to_pos(event.pos[0], event.pos[1])
                panel_x = BOARD_PX
                btn_rect_check = pygame.Rect(panel_x + 30, 200, PANEL_WIDTH - 60, 45)
                if btn_rect_check.collidepoint(event.pos):
                    reset_game()
                    ai_thinking = False
                elif pos and not game_over and current_player == BLACK_STONE:
                    r, c = pos
                    if board[r][c] == EMPTY:
                        board[r][c] = BLACK_STONE
                        last_move = (r, c)
                        move_count += 1
                        if check_win(board, BLACK_STONE):
                            game_over = True
                            winner = BLACK_STONE
                        elif is_board_full(board):
                            game_over = True
                            winner = None
                        else:
                            current_player = WHITE_STONE
                            ai_thinking = True

        draw_board()
        draw_hover()
        draw_stones()
        btn_rect = draw_panel()
        pygame.display.flip()
        clock.tick(60)

        if ai_thinking and not game_over:
            ai_move()
            ai_thinking = False

if __name__ == "__main__":
    main()
