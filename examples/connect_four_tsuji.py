from pathlib import Path

import param_mc_remote as param
import pygame
import pygame.freetype
from mc_remote.minecraft import Minecraft
from param_mc_remote import PLAYER_ORIGIN as PO
from param_mc_remote import block
from pygame.locals import Rect

# Connect to minecraft and open a session as player with origin location
mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
mc.setPlayer(param.PLAYER_NAME, PO.x, PO.y, PO.z)
# mc.postToChat("Hello, Minecraft Server!! from yu184743")


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([480, 480])
pygame.display.set_caption("pygame FourInARow")

# font1 = pygame.freetype.Font("./fonts/natumemozi.ttf", 48)
font_path = Path(__file__).resolve().parent / "fonts" / "natumemozi.ttf"
font1 = pygame.freetype.Font(str(font_path), 48)

running = True
gamenow = True
FPS = 30
WAIT = 0.15
FALL_INTERVAL_MS = 120
BLINK_INTERVAL_MS = 180
BLINK_COUNT = 2
WIN_BLINK_COUNT = 4

ground = (202, 202, 202)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

CTRL_KEYS = [[pygame.K_LEFT, "LEFT", -1],
             [pygame.K_RIGHT, "RIGHT", 1],
             [pygame.K_SPACE, "SPACE", 0],
             [pygame.K_0, "WIN", 0],  # デバッグ用　---
             [pygame.K_1, "BOARD", 0],
             [pygame.K_2, "STONE", 0]]


BOARD_SIZE = 9
N = 4

# Minecraft内の盤面レイアウト
BOARD_X = 5
BOARD_Y = 69
BOARD_Z = 0
CELL_SIZE = 2
GRID_WIDTH = 1
CELL_STEP = CELL_SIZE + GRID_WIDTH
BOARD_BLOCK_SIZE = BOARD_SIZE * CELL_SIZE + (BOARD_SIZE + 1) * GRID_WIDTH
BOARD_END_X = BOARD_X + BOARD_BLOCK_SIZE - 1
BOARD_END_Y = BOARD_Y + BOARD_BLOCK_SIZE - 1
CURSOR_GAP = 0


#  盤内チェック
def in_bounds(x_coord, y_coord, board_size=BOARD_SIZE):
    return 0 <= x_coord < board_size and 0 <= y_coord < board_size


def check_win(x_coord, y_coord, board, player_value, n=N):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        line = []

        # 負の方向に連続する石を、端から中心へ並べる。
        nx, ny = x_coord - dx, y_coord - dy
        while in_bounds(nx, ny) and board[nx][ny] == player_value:
            line.append((nx, ny))
            nx -= dx
            ny -= dy
        line.reverse()
        line.append((x_coord, y_coord))

        # 正の方向に連続する石を追加する。
        nx, ny = x_coord + dx, y_coord + dy
        while in_bounds(nx, ny) and board[nx][ny] == player_value:
            line.append((nx, ny))
            nx += dx
            ny += dy

        if len(line) >= n:
            center_index = line.index((x_coord, y_coord))
            start = min(max(center_index - n + 1, 0), len(line) - n)
            return line[start:start + n]

    return []


def pygame_stone_color(stone):
    if stone == 1:
        return RED
    if stone == 2:
        return BLUE
    return WHITE


def minecraft_stone_block(stone):
    if stone == 1:
        return block.RED_CONCRETE
    if stone == 2:
        return block.BLUE_CONCRETE
    return block.WHITE_CONCRETE


def board_startup():
    """上下左右に格子を残して、空の盤面を描画する。"""
    mc.setBlocks(
        BOARD_X, BOARD_Y, BOARD_Z,
        BOARD_END_X, BOARD_END_Y, BOARD_Z,
        block.GRAY_CONCRETE,
    )

    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            x = BOARD_X + GRID_WIDTH + column * CELL_STEP
            y = BOARD_Y + GRID_WIDTH + row * CELL_STEP
            mc.setBlocks(
                x, y, BOARD_Z,
                x + CELL_SIZE - 1, y + CELL_SIZE - 1, BOARD_Z,
                block.WHITE_CONCRETE,
            )


def mc_disc(column, row, stone):
    """盤の1マスを、石の色（0なら空白）で描画する。"""
    x = BOARD_X + GRID_WIDTH + column * CELL_STEP
    y = BOARD_Y + GRID_WIDTH + (BOARD_SIZE - 1 - row) * CELL_STEP
    mc.setBlocks(
        x, y, BOARD_Z,
        x + CELL_SIZE - 1, y + CELL_SIZE - 1, BOARD_Z,
        minecraft_stone_block(stone),
    )


def mc_clear_cursor():
    """Minecraft側のカーソル表示領域を消去する。"""
    cursor_y = BOARD_END_Y + CURSOR_GAP + 1
    mc.setBlocks(
        BOARD_X, cursor_y, BOARD_Z,
        BOARD_END_X, cursor_y + CELL_SIZE - 1, BOARD_Z,
        block.AIR,
    )


def mc_cursor(column, stone):
    """カーソルを消してから、現在の手番の色で描き直す。"""
    mc_clear_cursor()
    cursor_y = BOARD_END_Y + CURSOR_GAP + 1
    x = BOARD_X + GRID_WIDTH + column * CELL_STEP
    mc.setBlocks(
        x, cursor_y, BOARD_Z,
        x + CELL_SIZE - 1, cursor_y + CELL_SIZE - 1, BOARD_Z,
        minecraft_stone_block(stone),
    )


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            gamenow = False

    whichturn = False
    #  False = red, True = blue

    #  二次元配列
    boardcolor = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    stonecolor = 1
    #  0 = nothing, 1 = red, 2 = blue

    cursor = 4
    #  初期位置

    cursor_change = 0
    skip_frames = FPS * WAIT + 1
    update_flag = True

    stonecount = [0] * BOARD_SIZE
    gamenow = True

    # 落下中の石は盤面に確定させず、別の状態として描画する。
    animation_phase = None
    animation_column = 0
    animation_row = 0
    animation_target_row = 0
    animation_color = 0
    animation_visible = False
    animation_next_tick = 0
    blink_toggles = 0
    winner = None
    winning_cells = []

    mc.setBlocks(0, 64, -1, 48, 127, 48, block.AIR)
    board_startup()

    mc_cursor(cursor, stonecolor)

    print("game start")
    while gamenow:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gamenow = False
            elif event.type == pygame.KEYDOWN:
                for key in CTRL_KEYS:
                    if event.key == key[0]:
                        if (key[1] == "LEFT" or key[1] == "RIGHT") and animation_phase is None and winner is None:
                            cursor_change = key[2]
                            update_flag = True
                        elif key[1] == "SPACE" and animation_phase is None:
                            if winner is not None:
                                gamenow = False
                            elif stonecount[cursor] < BOARD_SIZE:
                                animation_phase = "falling"
                                animation_column = cursor
                                animation_row = 0
                                animation_target_row = BOARD_SIZE - 1 - stonecount[cursor]
                                animation_color = stonecolor
                                animation_visible = True
                                animation_next_tick = pygame.time.get_ticks() + FALL_INTERVAL_MS
                                mc_disc(animation_column, animation_row, animation_color)
                        elif key[1] == "WIN":
                            #  以下デバッグ用
                            print("game end debug")
                            gamenow = False
                        elif key[1] == "BOARD":
                            for i in range(BOARD_SIZE):
                                for j in range(BOARD_SIZE):
                                    print(boardcolor[j][i], end=" ")
                                print(" ")
                            update_flag = True
                        elif key[1] == "STONE":
                            for i in range(BOARD_SIZE):
                                print(stonecount[i], end=" ")
                            print(" ")
                            update_flag = True
            elif event.type == pygame.KEYUP:
                for key in CTRL_KEYS:
                    if event.key == key[0] and (key[1] == "LEFT" or key[1] == "RIGHT"):
                        cursor_change = 0

        if update_flag and (skip_frames > FPS * WAIT):
            update_flag = False
            skip_frames = 0
            if 0 <= cursor + cursor_change < BOARD_SIZE:
                cursor += cursor_change
                mc_cursor(cursor, stonecolor)
            cursor_change = 0

        now = pygame.time.get_ticks()

        if animation_phase == "falling" and now >= animation_next_tick:
            if animation_row < animation_target_row:
                # 今の位置を消し、すぐ下の位置へ石を移す。
                mc_disc(animation_column, animation_row, 0)
                animation_row += 1
                mc_disc(animation_column, animation_row, animation_color)
                animation_next_tick = now + FALL_INTERVAL_MS
            else:
                animation_phase = "blinking"
                blink_toggles = BLINK_COUNT * 2
                animation_next_tick = now + BLINK_INTERVAL_MS

        elif animation_phase == "blinking" and now >= animation_next_tick:
            animation_visible = not animation_visible
            mc_disc(
                animation_column,
                animation_row,
                animation_color if animation_visible else 0,
            )
            blink_toggles -= 1
            animation_next_tick = now + BLINK_INTERVAL_MS

            if blink_toggles == 0:
                # 点滅が終わってから盤面へ石を確定する。
                boardcolor[animation_column][animation_target_row] = animation_color
                stonecount[animation_column] += 1
                winning_cells = check_win(
                    animation_column,
                    animation_target_row,
                    boardcolor,
                    animation_color,
                )
                animation_phase = None
                animation_visible = False

                if winning_cells:
                    winner = animation_color
                    animation_phase = "win_blinking"
                    animation_visible = True
                    blink_toggles = WIN_BLINK_COUNT * 2
                    animation_next_tick = now + BLINK_INTERVAL_MS
                    mc_clear_cursor()
                else:
                    whichturn = not whichturn
                    stonecolor = 2 if whichturn else 1
                    mc_cursor(cursor, stonecolor)

        elif animation_phase == "win_blinking" and now >= animation_next_tick:
            animation_visible = not animation_visible
            for column, row in winning_cells:
                mc_disc(column, row, winner if animation_visible else 0)
            blink_toggles -= 1
            animation_next_tick = now + BLINK_INTERVAL_MS

            if blink_toggles == 0:
                # 勝利した4枚を表示した状態で、スペースキー入力を待つ。
                animation_phase = None
                animation_visible = True
                for column, row in winning_cells:
                    mc_disc(column, row, winner)
                print("game over - press SPACE to start a new game")

        screen.fill(ground)  # background color

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                displayed_stone = boardcolor[x][y]
                if (
                    animation_phase == "win_blinking"
                    and not animation_visible
                    and (x, y) in winning_cells
                ):
                    displayed_stone = 0
                pygame.draw.rect(
                    screen,
                    pygame_stone_color(displayed_stone),
                    Rect(48 + x * 32, 70 + y * 32, 24, 24),
                )

        if animation_phase in ("falling", "blinking") and animation_visible:
            pygame.draw.rect(
                screen,
                pygame_stone_color(animation_color),
                Rect(
                    48 + animation_column * 32,
                    70 + animation_row * 32,
                    24,
                    24,
                ),
            )

        if winner is None:
            pygame.draw.rect(
                screen,
                pygame_stone_color(stonecolor),
                Rect(48 + cursor * 32, 24, 24, 24),
            )
            message = str(cursor)
        elif animation_phase is None:
            message = "space: New Game"
        else:
            message = "WIN!"

        text1, rect1 = font1.render(message, pygame_stone_color(winner or stonecolor))
        rect1.center = (220, 430)
        screen.blit(text1, rect1)

        skip_frames += 1
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
