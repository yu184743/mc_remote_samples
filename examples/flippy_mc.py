# Flippy (an Othello or Reversi clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Based on the "reversi.py" code that originally appeared in "Invent
# Your Own Computer Games with Python", chapter 15:
#   http://inventwithpython.com/chapter15.html

import random
import sys
import pygame
import time
import copy

from mc_remote.minecraft import Minecraft
import param_mc_remote as param
from param_mc_remote import PLAYER_ORIGIN as PO
from param_mc_remote import block

# Connect to minecraft and open a session as player with origin location
mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
mc.setPlayer(param.PLAYER_NAME, PO.x, PO.y, PO.z)
# mc.postToChat("Hello, Minecraft Server!! from yu184743")

#
# hintのドットを消すタイミングが難しい。
# pygameでは、毎フレーム描画するので、問題ない。
# マイクラでは、コンピューターのターンに入ったときと
# hintモードをオフにしたときに、hintのドットを消す必要がある。
# hintモードをオフにしたときに、hintのドットを消す必要がある。


block_colors = [block.RED_WOOL,
                block.LIME_WOOL,  # green
                block.BLUE_WOOL,
                block.YELLOW_WOOL,
                block.ORANGE_WOOL,
                block.MAGENTA_WOOL]  # purple


FPS = 30  # frames per second to update the screen
WINDOWWIDTH = 640  # width of the program's window, in pixels
WINDOWHEIGHT = 480  # height in pixels
SPACESIZE = 50  # width & height of each space on the board, in pixels
BOARDWIDTH = 8  # how many columns of spaces on the game board
BOARDHEIGHT = 8  # how many rows of spaces on the game board
WHITE_TILE = 'WHITE_TILE'  # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE'  # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE'  # an arbitrary but unique value
HINT_TILE = 'HINT_TILE'  # an arbitrary but unique value
ANIMATIONSPEED = 7  # integer from 1 to 100, higher is faster animation

# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN

WHITE_mc = param.WHITE_WOOL
BLACK_mc = param.BLACK_WOOL
HINTCOLOR_mc = param.BROWN_WOOL
GREEN_mc = param.GREEN_WOOL
CURSOR_mc = param.SEA_LANTERN_BLOCK

X0_mc, Y0_mc, Z0_mc = 8, 136, -80
wait = 0.01


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Flippy')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Set up the background image.
    boardImage = pygame.image.load('flippyboard.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('flippybackground.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    # Run the main game.
    while True:
        if not runGame():
            break


def runGame():
    # Plays a single game of reversi each time this function is called.

    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    showHints = False
    turn = random.choice(['computer', 'player'])

    draw_board_mc()  # 緑のボードを描いて、黒い枠線を引く　一番最初、先行後攻を決める前に描く

    # Draw the starting board and ask the player what color they want.
    drawBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()

    # Make the Surface and Rect objects for the "New Game" and "Hints" buttons
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)
    hintsSurf = FONT.render('Hints', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (WINDOWWIDTH - 8, 40)

    cursor_posx_mc, cursor_posy_mc = 0, 0
    x_change, y_change = 0, 0
    skip_frames = FPS * wait + 1
    update_flag = True
    while True: # main game loop
        # Keep looping for player and computer's turns.
        if turn == 'player':
            draw_cursor_mc(cursor_posx_mc, cursor_posy_mc, color=CURSOR_mc)  # カーソル表示

            # Player's turn:
            if getValidMoves(mainBoard, playerTile) == []:
                # If it's the player's turn but they
                # can't move, then end the game.
                break
            movexy = None
            while movexy is None:
                # Keep looping until the player clicks on a valid space.

                # Determine which board data structure to use for display.
                if showHints:
                    boardToDraw = getBoardWithValidMoves(mainBoard, playerTile)
                else:
                    boardToDraw = mainBoard

                checkForQuit()
                for event in pygame.event.get(): # event handling loop
                    if event.type == pygame.MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                            return True
                        elif hintsRect.collidepoint( (mousex, mousey) ):
                            # Toggle hints mode
                            showHints = not showHints
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        movexy = getSpaceClicked(mousex, mousey)
                        if movexy is not None and not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                            movexy = None
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            x_change = -1
                            update_flag = True
                        if event.key == pygame.K_RIGHT:
                            x_change = 1
                            update_flag = True
                        if event.key == pygame.K_UP:
                            y_change = -1
                            update_flag = True
                        if event.key == pygame.K_DOWN:
                            y_change = 1
                            update_flag = True
                        if event.key == pygame.K_RETURN:
                            movexy = (cursor_posx_mc, cursor_posy_mc)
                            if not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                                movexy = None
                            update_flag = True

                    if event.type == pygame.KEYUP:
                        if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                            x_change = 0
                        if event.key in {pygame.K_UP, pygame.K_DOWN}:
                            y_change = 0

                if update_flag and (skip_frames > FPS * wait):
                    skip_frames = 0
                    update_flag = False
                    draw_cursor_mc(cursor_posx_mc, cursor_posy_mc, color=BLACK_mc)  # 黒で消す
                    cursor_posx_mc += x_change
                    if cursor_posx_mc < 0:
                        cursor_posx_mc = 0
                    if cursor_posx_mc > 7:
                        cursor_posx_mc = 7
                    cursor_posy_mc += y_change
                    if cursor_posy_mc < 0:
                        cursor_posy_mc = 0
                    if cursor_posy_mc > 7:
                        cursor_posy_mc = 7
                    draw_cursor_mc(cursor_posx_mc, cursor_posy_mc)  # カーソル色で描く
                skip_frames += 1

                # Draw the game board.
                drawBoard(boardToDraw)
                drawInfo(boardToDraw, playerTile, computerTile, turn)

                # Draw the "New Game" and "Hints" buttons.
                DISPLAYSURF.blit(newGameSurf, newGameRect)
                DISPLAYSURF.blit(hintsSurf, hintsRect)

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            # Make the move and end the turn.
            makeMove(mainBoard, playerTile, movexy[0], movexy[1], True)
            if getValidMoves(mainBoard, computerTile) != []:
                # Only set for the computer's turn if it can make a move.
                turn = 'computer'

        else:
            draw_cursor_mc(cursor_posx_mc, cursor_posy_mc, color=BLACK_mc)  # カーソル消す
            # Computer's turn:
            if getValidMoves(mainBoard, computerTile) == []:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                break

            # Draw the board.
            drawBoard(mainBoard)
            drawInfo(mainBoard, playerTile, computerTile, turn)

            # Draw the "New Game" and "Hints" buttons.
            DISPLAYSURF.blit(newGameSurf, newGameRect)
            DISPLAYSURF.blit(hintsSurf, hintsRect)

            # Make it look like the computer is thinking by pausing a bit.
            pauseUntil = time.time() + random.randint(5, 15) * 0.1
            while time.time() < pauseUntil:
                pygame.display.update()

            # Make the move and end the turn.
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y, True)
            if getValidMoves(mainBoard, playerTile) != []:
                # Only set for the player's turn if they can make a move.
                turn = 'player'

    # Display the final score.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)

    # Determine the text of the message to display.
    if scores[playerTile] > scores[computerTile]:
        text = 'You beat the computer by %s points! Congratulations!' % \
               (scores[playerTile] - scores[computerTile])
    elif scores[playerTile] < scores[computerTile]:
        text = 'You lost. The computer beat you by %s points.' % \
               (scores[computerTile] - scores[playerTile])
    else:
        text = 'The game was a tie!'

    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    # Display the "Play again?" text with Yes and No buttons.
    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    # Make "Yes" button.
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    # Make "No" button.
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on Yes or No.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif noRect.collidepoint( (mousex, mousey) ):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)


def animateTileChange(tilesToFlip, tileColor, additionalTile):
    # Draw the additional tile that was just laid down. (Otherwise we'd
    # have to completely redraw the board & the board info.)

    # tileColorは、置いたdiscの色

    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
        tileColor_mc = WHITE_mc
        tileColor_mc_original = BLACK_mc  # 裏の色
    else:
        additionalTileColor = BLACK
        tileColor_mc = BLACK_mc
        tileColor_mc_original = WHITE_mc

    # 置いたdisc
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    put_disc_mc(additionalTile[0], additionalTile[1], tileColor_mc)

    # 裏返しアニメーション pygame版が使っている0-255 に合わせて、パターンを変えつつ色も変える。
    anime_index_last = -1
    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        anime_index = rgbValues // 29  # 0-8の9段階で変化
        anime = (0, 1, 2, 3, 4, 3, 2, 1, 0)  # オリジナルのパターン（0）から細く（1,2,3）、なくなり（4）、色が変わって太く（3, 2, 1）、フル（０）。
        if anime_index < 4:
            color_mc = tileColor_mc_original  # 表＝元の色から
        else:
            color_mc = tileColor_mc  # 裏返し＝置いた色に

        if tileColor == WHITE_TILE:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif tileColor == BLACK_TILE:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for x, y in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
            if anime_index != anime_index_last:
                put_disc_mc(x, y, color_mc, pattern_num=anime[anime_index])
        anime_index_last = anime_index

        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()


def drawBoard(board):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT + 1):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    # draw_board_mc()  # 緑のボードを描いて、黒い枠線を引く　毎回やるとまずいので、分離

    # Draw the black & white tiles or hint spots.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                    tileColor_mc = WHITE_mc
                else:
                    tileColor = BLACK
                    tileColor_mc = BLACK_mc
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
                put_disc_mc(x, y, tileColor_mc)
            elif board[x][y] == HINT_TILE:
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx - 4, centery - 4, 8, 8))
                put_hint_mc(x, y)
            else:
                clear_cell_mc(x, y)


DISC_PATTERN = [[0] * 8 for i in range(8)]
DISC_PATTERN[0] = ((0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 1, 1, 1, 1, 0, 0),
                   (0, 1, 1, 1, 1, 1, 1, 0),
                   (0, 1, 1, 1, 1, 1, 1, 0),
                   (0, 0, 1, 1, 1, 1, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0))

DISC_PATTERN[1] = ((0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 1, 1, 1, 1, 0, 0),
                   (0, 0, 1, 1, 1, 1, 0, 0),
                   (0, 0, 1, 1, 1, 1, 0, 0),
                   (0, 0, 1, 1, 1, 1, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0))

DISC_PATTERN[2] = ((0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 0, 1, 1, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0))

DISC_PATTERN[3] = ((0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0))

DISC_PATTERN[4] = ((0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0))


# small pattern
# DISC_PATTERN[0] = ((0, 0, 0, 0, 0, 0),
#                    (0, 0, 1, 1, 0, 0),
#                    (0, 1, 1, 1, 1, 0),
#                    (0, 1, 1, 1, 1, 0),
#                    (0, 0, 1, 1, 0, 0),
#                    (0, 0, 0, 0, 0, 0))


def draw_board_mc():
    # mc.setBlocks(X0_mc, Y0_mc, Z0_mc, X0_mc + 9 * 8, Y0_mc - 9 * 8, Z0_mc, param.AIR)
    mc.setBlocks(X0_mc, Y0_mc, Z0_mc, X0_mc + 9 * 8, Y0_mc - 9 * 8, Z0_mc, param.GREEN_WOOL)
    for _x in range(9):
        mc.setBlocks(X0_mc + 9 * _x, Y0_mc, Z0_mc, X0_mc + 9 * _x, Y0_mc - 9 * 8, Z0_mc, param.BLACK_WOOL)
    for _y in range(9):
        mc.setBlocks(X0_mc, Y0_mc - 9 * _y, Z0_mc, X0_mc + 9 * 8, Y0_mc - 9 * _y, Z0_mc, param.BLACK_WOOL)


def put_hint_mc(x, y):
    mc.setBlocks(X0_mc + 9 * x + 4, Y0_mc - 9 * y - 4, Z0_mc,
                 X0_mc + 9 * x + 5, Y0_mc - 9 * y - 5, Z0_mc, HINTCOLOR_mc)


def clear_cell_mc(x, y):
    mc.setBlocks(X0_mc + 9 * x + 4, Y0_mc - 9 * y - 4, Z0_mc,
                 X0_mc + 9 * x + 5, Y0_mc - 9 * y - 5, Z0_mc, GREEN_mc)


def put_disc_mc(x, y, color, pattern_num=0):
    for dy in range(8):
        for dx in range(8):
            if DISC_PATTERN[pattern_num][dy][dx] == 1:
                mc.setBlock(X0_mc + 9 * x + dx + 1, Y0_mc - 9 * y - dy - 1, Z0_mc, color)
            else:
                mc.setBlock(X0_mc + 9 * x + dx + 1, Y0_mc - 9 * y - dy - 1, Z0_mc, GREEN_mc)


def draw_cursor_mc(x, y, color=CURSOR_mc):
    mc.setBlocks(X0_mc + 9 * x, Y0_mc - 9 * y, Z0_mc,
                 X0_mc + 9 * (x + 1), Y0_mc - 9 * y, Z0_mc, color)
    mc.setBlocks(X0_mc + 9 * x, Y0_mc - 9 * y, Z0_mc,
                 X0_mc + 9 * x, Y0_mc - 9 * (y + 1), Z0_mc, color)
    mc.setBlocks(X0_mc + 9 * x, Y0_mc - 9 * (y + 1), Z0_mc,
                 X0_mc + 9 * (x + 1), Y0_mc - 9 * (y + 1), Z0_mc, color)
    mc.setBlocks(X0_mc + 9 * (x + 1), Y0_mc - 9 * y, Z0_mc,
                 X0_mc + 9 * (x + 1), Y0_mc - 9 * (y + 1), Z0_mc, color)


def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
               mousex < (x + 1) * SPACESIZE + XMARGIN and \
               mousey > y * SPACESIZE + YMARGIN and \
               mousey < (y + 1) * SPACESIZE + YMARGIN:
                return (x, y)
    return None


def drawInfo(board, playerTile, computerTile, turn):
    # Draws scores and whose turn it is at the bottom of the screen.
    scores = getScoreOfBoard(board)
    scoreSurf = FONT.render("Player Score: %s    Computer Score: %s    %s's Turn" % (str(scores[playerTile]), str(scores[computerTile]), turn.title()), True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def resetBoard(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE

    # Add starting pieces to the center
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[4][4] = WHITE_TILE


def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == WHITE_TILE:
        otherTile = BLACK_TILE
    else:
        otherTile = WHITE_TILE

    tilesToFlip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # The piece belongs to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break # break out of while loop, continue in for loop
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse
                # direction until we reach the original space, noting all
                # the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = EMPTY_SPACE # make space empty
    if len(tilesToFlip) == 0: # If no tiles flipped, this move is invalid
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT


def getBoardWithValidMoves(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = HINT_TILE
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of (x,y) tuples of all valid moves.
    validMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if isValidMove(board, tile, x, y):
                validMoves.append((x, y))
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles.
    xscore = 0
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == WHITE_TILE:
                xscore += 1
            if board[x][y] == BLACK_TILE:
                oscore += 1
    return {WHITE_TILE:xscore, BLACK_TILE:oscore}


def enterPlayerTile():
    # Draws the text and handles the mouse click events for letting
    # the player choose which color they want to be.  Returns
    # [WHITE_TILE, BLACK_TILE] if the player chooses to be White,
    # [BLACK_TILE, WHITE_TILE] if Black.

    # Create the text.
    textSurf = FONT.render('Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    return [WHITE_TILE, BLACK_TILE]
                elif oRect.collidepoint( (mousex, mousey) ):
                    return [BLACK_TILE, WHITE_TILE]

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def makeMove(board, tile, xstart, ystart, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if not tilesToFlip:
        return False

    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or \
           (x == BOARDWIDTH and y == 0) or \
           (x == 0 and y == BOARDHEIGHT) or \
           (x == BOARDWIDTH and y == BOARDHEIGHT)


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = copy.deepcopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def checkForQuit():
    for event in pygame.event.get(pygame.QUIT): # event handling loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
