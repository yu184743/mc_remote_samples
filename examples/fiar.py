import pygame
import pygame.freetype
import time
from pygame.locals import Rect

from mc_remote.minecraft import Minecraft
import param_mc_remote as param
from param_mc_remote import PLAYER_ORIGIN as PO
from param_mc_remote import block

# Connect to minecraft and open a session as player with origin location
mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
mc.setPlayer(param.PLAYER_NAME, PO.x, PO.y, PO.z)
# mc.postToChat("Hello, Minecraft Server!! from yu184743")
mc.setBlock(5, 68, 5, block.GOLD_BLOCK)


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([640,480])
pygame.display.set_caption("pygame FourInARow")

font1 = pygame.freetype.Font("fonts/natumemozi.ttf", 48)

running = True
gamenow = True
FPS = 30
WAIT = 0.15

ground = (202, 202, 202)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CURSOR = (0, 123, 0)



CTRL_KEYS = [[pygame.K_LEFT, "LEFT", -1],
             [pygame.K_RIGHT, "RIGHT", 1],
             [pygame.K_SPACE, "SPACE", 0],
             [pygame.K_0, "WIN", 0], # デバッグ用　---
             [pygame.K_1, "BOARD", 0],
             [pygame.K_2, "STONE", 0]]

win_flag = False
doCheck = True

def win_check() : # 注：古いコード 後で振り返るために残す
    # 勝利判定文 print()はデバッグ用
    win_flag = True
    doCheck = True
    if stonecount[cursor] > 3: #下
        for x in range(4):
            if color[sta + 9*x] != stonecolor:
                win_flag = False
        if win_flag == True:
            doCheck = False
    if cursor < 6 and doCheck == True: #右
        for x in range (4):
            if color[sta + x] != stonecolor:
                win_flag = False
        if win_flag == True:
            doCheck = False
    if cursor > 2 and doCheck == True: # 左
        for x in range(4):
            if color[sta - x] != stonecolor:
                win_flag = False
        if win_flag == True:
            doCheck = False
    if stonecount[cursor] < 7 and cursor < 6 and doCheck == True: #右上
        print("judge rightup")
        for x in range(4):
            print(sta - 8*x)
            if color[sta - 8*x] != stonecolor:
                win_flag = False
        if win_flag == True:
            doCheck = False
    if stonecount[cursor] > 3 and cursor < 6 and doCheck == True: #右下
        print("judge rightdown")
        for x in range(4):
            print(sta + 10*x)
            if color[sta + 10*x] != stonecolor:
                win_flag = False
        if win_flag == True:
            doCheck = False
    if stonecount[cursor] < 7 and cursor > 2 and doCheck == True: #左上
        print("judge leftup")
        for x in range(4):
            print(sta - 10*x)
            if color[sta - 10*x] != stonecolor:
                win_flag = False
        if win_flag == True:
            doCheck = False
    if stonecount[cursor] > 3 and cursor > 2 and doCheck == True: #左下
        print("judge leftdown")
        for x in range(4):
            print(sta + 8*x)
            if color[sta + 8*x] != stonecolor:
                win_flag = False
        if win_flag == True:
            doCheck = False

def win_check2(): #自作 判定が怪しい 長い
    wincount = 0
    for x in range(4):
        if sta + 9*x < 81: # 下
            if color[sta + 9*x] == stonecolor:
                wincount += 1
            else:
                break
    if wincount >= 4:
        return True

    wincount = 0
    for x in range(4):
        if sta + x < (sta // 9 + 1) * 9: # 右
            if color[sta + x] == stonecolor:
                wincount += 1
            else:
                break
        if sta - x >= (sta // 9) * 9: # 左
            if color [sta - x] == stonecolor:
                wincount += 1
            else:
                break
    if wincount >= 4:
        return True

    wincount = 0
    for x in range(4):
        if sta - 8*x >= 0 and cursor + x < 9: # 右上
            if color[sta - 8*x] == stonecolor:
                wincount += 1
            else:
                break
        if sta + 8*x < 81 and cursor - x > 0: # 左下
            if color[sta + 8*x] == stonecolor:
                wincount += 1
            else:
                break
    if wincount >= 4:
        return True
        
    wincount = 0
    for x in range(4):
        if sta + 10*x < 81 and cursor + x < 9: #右下
            if color[sta + 10*x] == stonecolor:
                wincount += 1
            else:
                break
        if sta - 10*x >= 0 and cursor - x > 0: # 左上
            if color[sta - 10*x] == stonecolor:
                wincount += 1
            else:
                break
    if wincount >= 4:
        return True
    return False


BOARD_SIZE = 9
N = 4

def inBounds(x, y, board_size=BOARD_SIZE): #盤内チェック
    if x < 0 or y < 0 or x >= board_size or y >= board_size:
        return False
    else:
        return True

def checkWin(x, y, board, n=N):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    playerValue = stonecolor
    for dx, dy in directions:
        win_count = 1  # 中心の石
        
        # 正の方向
        nx, ny = x + dx, y + dy
        while inBounds(nx, ny) and board[nx][ny] == playerValue:
            win_count += 1
            nx += dx
            ny += dy
        # 負の方向
        nx, ny = x - dx, y - dy
        while inBounds(nx, ny) and board[nx][ny] == playerValue:
            win_count += 1
            nx += dx
            ny += dy
        if win_count >= n:
            return True
    return False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            gamenow = False
    
    mc.setBlocks(5, 68, 0, 21, 84, 0, block.AIR)
    mc.setBlocks(5, 68, -1, 21, 84, -1, block.GRAY_CONCRETE)
    mc.setBlocks(5, 86, 0, 21, 86, 0, block.AIR)

    whichturn = False
    # False = red, True = blue

    boardcolor = [[0 for i in range(9)] for j in range(9)] # 二次元配列
    color = [0]*81 # 一次元配列
    stonecolor = 1
    # 0 = nothing, 1 = red, 2 = blue

    cursor = 4
    #初期位置

    cursor_change = 0
    skip_frames = FPS *WAIT + 1
    update_flag = True

    stonecount = [0]*9
    gamenow = True
    win_flag = False
    doCheck = False

    print("game start")
    while gamenow == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gamenow = False
            elif event.type == pygame.KEYDOWN:
                for key in CTRL_KEYS:
                    if event.key == key[0]:
                        if key[1] == "LEFT":
                            cursor_change = key[2]
                            update_flag = True
                            mc.setBlocks(5, 86, 0, 21, 86, 0, block.AIR)
                        elif key[1] == "RIGHT":
                            cursor_change = key[2]
                            update_flag = True
                            mc.setBlocks(5, 86, 0, 21, 86, 0, block.AIR)
                        elif key[1] == "SPACE":
                            sta = cursor+(8-stonecount[cursor])*9
                            if stonecount[cursor] < 9:
                                color[sta] = stonecolor #一次元配列
                                boardcolor[cursor][8-stonecount[cursor]] = stonecolor #二次元配列
                                
                                print(str(cursor) + ", " + str(8 - stonecount[cursor]))
                                if checkWin(cursor, 8-stonecount[cursor], boardcolor) :
                                    gamenow = False
                                    time.sleep(2)
                                '''
                                if win_check2():
                                    gamenow = False
                                    time.sleep(2)
                                '''
                                stonecount[cursor] += 1
                                if whichturn == False:
                                    whichturn = True
                                else:
                                    whichturn = False
                            update_flag = True
                        elif key[1] == "WIN":
                            print("game end debug")
                            gamenow = False
                        elif key[1] == "BOARD":
                            for i in range(9):
                                for j in range(9):
                                    print(boardcolor[j][i], end = " ")
                                print(" ")
                            update_flag = True
                        elif key[1] == "STONE":
                            for i in range(9):
                                print(stonecount[i], end = " ")
                            print(" ")
                            update_flag = True
            elif event.type == pygame.KEYUP:
                for key in CTRL_KEYS:
                    if event.type == key[0]:
                        if key[1] == "LEFT":
                            cursor_change = 0
                        elif key[1] == "RIGHT":
                            cursor_change = 0

                     
    
        if update_flag and (skip_frames > FPS * WAIT):
            update_flag = False
            skip_frames = 0
            if cursor + cursor_change >= 0 and cursor + cursor_change <= 8:
                cursor += cursor_change
            cursor_change = 0

        if(whichturn == False):
            stonecolor = 1
        else:  
            stonecolor = 2

        screen.fill(ground) # background color


        '''
        for x in range(81): # 四角を描くコード 一次元配列版 正常に動作
            y = x//9
            if color[x] == 0:
                pygame.draw.rect(screen, WHITE, Rect(48 + x%9 * 32, 70 + y * 32, 24, 24))
            elif color[x] == 1:
                pygame.draw.rect(screen, RED, Rect(48 + x%9 * 32, 70 + y * 32, 24, 24))
            else:
                pygame.draw.rect(screen, BLUE, Rect(48 + x%9 * 32, 70 + y * 32, 24, 24))
        '''

        for y in range(9):
            for x in range(9):
                if boardcolor[x][y] == 0:
                    pygame.draw.rect(screen, WHITE, Rect(48 + x * 32, 70 + y * 32, 24, 24))
                elif boardcolor[x][y] == 1:
                    pygame.draw.rect(screen, RED, Rect(48 + x * 32, 70 + y * 32, 24, 24))
                elif boardcolor[x][y] == 2:
                    pygame.draw.rect(screen, BLUE, Rect(48 + x * 32, 70 + y * 32, 24, 24))
                
        for x in range(81): # ブロック設置
            y1 = (2*(9-(x//9)))+66
            x1 = 5+((x%9)*2)
            if color[x] == 0:
                mc.setBlock(x1, y1, 0, block.WHITE_CONCRETE)
            elif color[x] == 1:
                mc.setBlock(x1, y1, 0, block.RED_CONCRETE)
            else:
                mc.setBlock(x1, y1, 0, block.BLUE_CONCRETE)

     
        pygame.draw.rect(screen, CURSOR, Rect(48 + cursor * 32, 24 + 0 * 32, 24, 24)) # カーソル設置
        mc.setBlock(5+2*cursor, 86, 0, block.GREEN_CONCRETE)
            
    
        text1, rect1 = font1.render(str(cursor), WHITE)
        rect1.center = (360, 360)
        screen.blit(text1, rect1)


        skip_frames += 1
        pygame.display.flip()
        clock.tick(30)

pygame.quit()