#五子棋.py
"""
Created on Mon May 18 21:27:22 2020

@author: Guocheng Lin
@email: lgc0208@bupt.edu.cn

Description:
    主要通过python的pygame库，实现一款支持人机对战和人人对战的五子棋小游戏。
在游戏初始界面会有5秒的规则介绍，五秒后自动进入人机对战模式。玩家可根据游戏中的提示
按下Q键切换为初始人人对战对接，按下E键切换为初始人机对战界面。在游戏进行过程中，程
序会记录并显示黑白两子的累计获胜局数，提高玩家体验。
"""

import pygame # 导入pygame库
pygame.display.init() # 初始化
import sys # 导入sys库
import pygame.gfxdraw # pygame 不会自动导入 pygame.gfxdraw 模块
# from board import Board, BLACK_CHESSMAN, WHITE_CHESSMAN, Point
from board import Board, WHITE_CHESSMAN
from machine import Machine, BLACK_CHESSMAN, Point
# 从board.py目录引入相关类和变量
from time import sleep


POINT_NUMBER = 15 # 五子棋盘每行每列的点数
POINT_SIZE = 30 # 棋盘中各个点的间隔
INSIDE_WIDTH = 10 # 边框与棋盘的间距
OUTSIDE_WIDTH = 30 # 边框与外部的间距
BORDER_WIDTH = 5 # 边框的宽度（粗细）
BORDER_LENGTH = POINT_SIZE * (POINT_NUMBER - 1) + 2 * INSIDE_WIDTH\
                +BORDER_WIDTH*2 # 边界的长度=各点间隔*（点数-1）+
                              # 2*边框与棋盘间距+边框宽度*2(不然下方和右方边框和棋盘宽度不够)
BOARD_START_PLACE = OUTSIDE_WIDTH + BORDER_WIDTH + INSIDE_WIDTH
                    # 棋盘的起始位置=外边界+边界宽+内边界

SCREEN_HEIGHT = POINT_SIZE * (POINT_NUMBER - 1) + OUTSIDE_WIDTH * 2 + BORDER_WIDTH + INSIDE_WIDTH * 2  # 屏幕高度
SCREEN_WIDTH = SCREEN_HEIGHT + 200  # 屏幕宽度

ORANGE_COLOR = (255, 165, 0) # 橙色(棋盘)
RED_COLOR = (200, 30, 30) # 红色(文字)
BLUE_COLOR = (30, 30, 200) # 蓝色(文字)
BLACK_COLOR = (0, 0, 0) # 黑色
WHITE_COLOR = (255, 255, 255) # 白色

PIECE_RADIUS_LEFT = POINT_SIZE//2 - 5 # 棋子的半径（左）
PIECE_RADIUS_RIGHT = POINT_SIZE//2 + 5 # 棋子的半径（右）

# 信息框文字起始位置
INFORMATION_PLACE = SCREEN_HEIGHT + 2*PIECE_RADIUS_RIGHT + 10

# 文字打印函数：在屏幕的(x,y)处打印文字，文字颜色默认为白色
def printText(screen, font, x, y, text, textColor = (255, 255, 255)):
    screenText = font.render(text, True, textColor) 
                            # 文本显示方法，第一个参数为
                            # 文本字符串，第二个参数为True时显示
                            # 更平滑，第三个参数为文本颜色
    screen.blit(screenText, (x, y)) # 在x，y处绘制需要显示的文字
    
# 棋盘的刻画
def drawBoard(screen):
    screen.fill(ORANGE_COLOR) # 填充背景色
    # 绘制最外层的矩形框
    pygame.draw.rect(screen, BLACK_COLOR, 
                     ((OUTSIDE_WIDTH, OUTSIDE_WIDTH), 
                      (BORDER_LENGTH,BORDER_LENGTH)), 
                      BORDER_WIDTH)

    # 绘制棋盘格子
    # 绘制横线
    for i in range(POINT_NUMBER):
        # 绘制线条，第三、第四个参数为起止点
        pygame.draw.line(screen, BLACK_COLOR, 
                        (BOARD_START_PLACE,BOARD_START_PLACE + POINT_SIZE * i),
                        (BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER - 1), 
                         BOARD_START_PLACE + POINT_SIZE * i),
                        1)
    # 绘制竖线
    for j in range(POINT_NUMBER):    
        # 绘制线条，第三、第四个参数为起止点
        pygame.draw.line(screen, BLACK_COLOR,
                         (BOARD_START_PLACE + POINT_SIZE * j, BOARD_START_PLACE),
                         (BOARD_START_PLACE + POINT_SIZE * j,
                          BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER - 1)),
                          1)
    # 绘制天元及星位
    for i in (3, 7, 11):
        for j in (3, 7, 11):
            if i == j :
                if i == 7:
                    radius = 3 # 天元
                else:
                    radius = 2 # 星位
            # 绘制平滑的圆形边框
            pygame.gfxdraw.aacircle(screen, 
                                    BOARD_START_PLACE + POINT_SIZE * i,
                                    BOARD_START_PLACE + POINT_SIZE * j,
                                    radius, BLACK_COLOR)
            # 绘制填充的圆形
            pygame.gfxdraw.filled_circle(screen,
                                         BOARD_START_PLACE + POINT_SIZE * i,
                                         BOARD_START_PLACE + POINT_SIZE * j,
                                         radius, BLACK_COLOR)

# 绘制棋子
def drawChess(screen, Point, pieceColor):
    # 绘制平滑的圆形边框
    pygame.gfxdraw.aacircle(screen, BOARD_START_PLACE + POINT_SIZE * Point.X,
                            BOARD_START_PLACE + POINT_SIZE * Point.Y, 
                            PIECE_RADIUS_LEFT, pieceColor)

    pygame.gfxdraw.filled_circle(screen, BOARD_START_PLACE + POINT_SIZE * Point.X,
                            BOARD_START_PLACE + POINT_SIZE * Point.Y, 
                            PIECE_RADIUS_LEFT, pieceColor)

# 绘制填充的圆形
def drawChessInformation(screen, pos, color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], PIECE_RADIUS_RIGHT, color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], PIECE_RADIUS_RIGHT, color)
    
# 下一个执子方
def getNextRunner(currentRunner):
    if currentRunner == BLACK_CHESSMAN: # 若黑方执子,返回白方
        return WHITE_CHESSMAN
    else: #若白方执子，返回黑方
        return BLACK_CHESSMAN

# 绘制信息栏
def drawInfomation(screen, font, currentRunner, 
                   SumOfBlackWin, SumOfWhiteWin):
    # 绘制黑子
    drawChess(screen, (SCREEN_HEIGHT + PIECE_RADIUS_RIGHT,
                       BOARD_START_PLACE + PIECE_RADIUS_RIGHT),
                        BLACK_CHESSMAN.pieceColor)
    # 绘制白子
    drawChess(screen, (SCREEN_HEIGHT + PIECE_RADIUS_RIGHT,
                       BOARD_START_PLACE + PIECE_RADIUS_RIGHT),
                        WHITE_CHESSMAN.pieceColor)
    # 打印信息文字
    printText(screen, font, INFORMATION_PLACE, BOARD_START_PLACE + 3,
              "玩家1", BLUE_COLOR)
    printText(screen, font, INFORMATION_PLACE, 
              BOARD_START_PLACE + PIECE_RADIUS_RIGHT + 3,
              "玩家2", BLUE_COLOR)

# 获取鼠标点击位置，传入参数为pygame库获取的鼠标点击位置
def getClick(clickPlace): 
    placeX = clickPlace[0] - BOARD_START_PLACE # 点击的位置在棋盘中的横坐标
    placeY = clickPlace[1] - BOARD_START_PLACE # 点击的位置在棋盘中的纵坐标
    if placeX < -INSIDE_WIDTH or placeY < -INSIDE_WIDTH: # 若越界
        return None
    x = placeX // POINT_SIZE # 以棋子的大小为单位计算
    y = placeY // POINT_SIZE
    
    # 修正点击位置，当用户点击位置与交点有偏差时自动修正
    if placeX % POINT_SIZE > PIECE_RADIUS_LEFT: 
        x += 1
    if placeY % POINT_SIZE > PIECE_RADIUS_LEFT:
        y += 1
    if x >= POINT_NUMBER or y >= POINT_NUMBER: # 恰好在中间位置时不修正
        return None
    return Point(x, y) # 返回游戏区的坐标
    
# 主函数
def main():
    pygame.init() # 初始化pygame
    # 根据定义的屏幕长宽，初始化准备显示的窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 设置窗口标题
    pygame.display.set_caption("五子棋_Python程序设计作业_林郭城_2019210471")
    pygame.font.init()
    font=pygame.font.SysFont("SimHei", 72) # 使用系统自带字体,否则显示会出现异常
    fontSmall = pygame.font.SysFont("SimHei", 36)
    fontSmallText = pygame.font.SysFont("SimHei", 18)
    textWidth, textHeight = font.size("某方获胜") # 确定表示文本的空间
     # 打印初始菜单
    screen.fill(ORANGE_COLOR) # 填充背景色
    printText(screen, fontSmall, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4, 
                      "游戏规则", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+100, 
                      "该五子棋游戏包括人人对战模式和人机对战模式", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+130, 
                      "若按下Q键切换为人人对战，按下E键切换为人机对战", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+160, 
                      "祝您游戏愉快！！！", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+190, 
                      "注：该屏幕五秒后自动消失", BLACK_COLOR)
    pygame.display.flip() # 更新屏幕
    sleep(5)
              
    
    board = Board(POINT_NUMBER) # 创建棋盘对象
    currentRunner = BLACK_CHESSMAN # 黑方先执子
    winner = None # 胜者初始化
    computer = Machine(POINT_NUMBER, WHITE_CHESSMAN) #AI#
    
    blackWinCount = 0
    whiteWinCount = 0
    
    gameType = 1 # 游戏模式，默认为人机对战。0为人人，1为人机
    while True:
        for event in pygame.event.get(): # 监听用户事件
            if event.type == pygame.QUIT: # 若用户点击'X'键
                pygame.quit() # 否则点击退出键后程序会变成未响应
                sys.exit() # 停止程序运行
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # 棋局结束后按下回车键重启游戏
                    if winner is not None: # 当有胜者出现时
                        winner = None # 重置胜者
                        currentRunner = BLACK_CHESSMAN # 重置执子方
                        board = Board(POINT_NUMBER) # 重置对象
                        if gameType == 1:
                            computer = Machine(POINT_NUMBER, WHITE_CHESSMAN) #重置电脑
                if event.key == pygame.K_q: # Q键切换为人人模式
                    gameType = 0
                    winner = None # 重置胜者
                    currentRunner = BLACK_CHESSMAN # 重置执子方
                    board = Board(POINT_NUMBER) # 重置对象
                if event.key == pygame.K_e: # E键切换为人机模式
                    gameType = 1
                    winner = None # 重置胜者
                    currentRunner = BLACK_CHESSMAN # 重置执子方
                    board = Board(POINT_NUMBER) # 重置对象
                    computer = Machine(POINT_NUMBER, WHITE_CHESSMAN) #重置电脑
            elif gameType == 1 and event.type == pygame.MOUSEBUTTONDOWN: # 人机模式下按下鼠标
                if winner is None:
                    pressArray = pygame.mouse.get_pressed() # 获取鼠标当前点击操作，返回一个三元组，分别对应左键、中键、右键
                    if pressArray[0] or pressArray[2]: # 若按下的是鼠标左键或右键
                        clickPlace = pygame.mouse.get_pos() # 获取鼠标当前位置，返回值为元组类型(x, y)
                        clickPoint = getClick(clickPlace) # 将获取的鼠标位置转换为棋盘上的坐标位置
                        if clickPoint is not None: # 若点击的位置在棋盘上
                            if board.ifDropChess(clickPoint): # 判断鼠标单击位置是否可以落子
                                winner = board.dropChess(currentRunner, clickPoint) # 判断落子后是否获胜
                                if winner is None: # 若还未出现胜者
                                    currentRunner = getNextRunner(currentRunner) # 交换执子方
                                    computer.getRivalDrop(clickPoint) # 电脑获取玩家落子
                                    machinePoint = computer.machineDrop() # 电脑落子
                                    winner = board.dropChess(currentRunner, machinePoint) # 判断电脑落子后是否获胜
                                    if winner is not None: # 若有胜者
                                        whiteWinCount += 1 
                                    currentRunner = getNextRunner(currentRunner)
                                else:
                                    blackWinCount += 1 # 胜利局数
                            else:
                                print("您点击的位置已有棋子")
                        else:
                            print("您点击的位置超出了棋盘区域")
            elif gameType == 0 and event.type == pygame.MOUSEBUTTONDOWN: # 人人模式下按下鼠标
                if winner is None:
                    pressArray = pygame.mouse.get_pressed() # 获取鼠标当前点击操作，返回一个三元组，分别对应左键、中键、右键
                    if pressArray[0] or pressArray[2]: # 若按下的是鼠标左键或右键
                        clickPlace = pygame.mouse.get_pos() # 获取鼠标当前位置，返回值为元组类型(x, y)
                        clickPoint = getClick(clickPlace) # 将获取的鼠标位置转换为棋盘上的坐标位置
                        if clickPoint is not None: # 若点击的位置在棋盘上
                            if board.ifDropChess(clickPoint): # 判断鼠标单击位置是否可以落子
                                winner = board.dropChess(currentRunner, clickPoint) # 判断落子后是否获胜
                                # 交换执子方
                                if currentRunner == BLACK_CHESSMAN: 
                                    currentRunner = WHITE_CHESSMAN
                                else:
                                    currentRunner = BLACK_CHESSMAN
                                if winner is not None: # 若有胜者
                                    if winner is WHITE_CHESSMAN:
                                        whiteWinCount += 1 
                                    elif winner is BLACK_CHESSMAN:
                                        blackWinCount += 1 # 胜利局数
                            else:
                                print("您点击的位置已有棋子")
                        else:
                            print("您点击的位置超出了棋盘区域")
        
        drawBoard(screen) # 绘制棋盘
        
        for y, row in enumerate(board.board): # 按行遍历数组化的棋盘
            for x, column in enumerate(row): # 遍历棋盘中每个点对应数组的元素
                if column == BLACK_CHESSMAN.Value: # 若x列对应的值为黑子，则画黑子
                    drawChess(screen, Point(x, y), BLACK_CHESSMAN.Color)
                elif column == WHITE_CHESSMAN.Value: # 若是白子，则画白子
                    drawChess(screen, Point(x, y), WHITE_CHESSMAN.Color)
        if gameType == 1:
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 130, 
                      "您正在进行的是：人机对战", BLACK_COLOR)
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 110, 
                      "按下Q键可切换为人人对战", BLACK_COLOR)
        elif gameType == 0:
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 130, 
                      "您正在进行的是：人人对战", BLACK_COLOR)
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 110, 
                      "按下E键可切换为人机对战", BLACK_COLOR)
        # 画信息栏中的黑白子
        drawChessInformation(screen, (SCREEN_WIDTH - PIECE_RADIUS_RIGHT - 160, 
                                      BOARD_START_PLACE + 20), BLACK_COLOR)
        drawChessInformation(screen, (SCREEN_WIDTH - PIECE_RADIUS_RIGHT - 160, 
                                      BOARD_START_PLACE + 20 + PIECE_RADIUS_RIGHT*3), WHITE_COLOR)
        # 刻画胜利局数
        printText(screen, fontSmallText, SCREEN_WIDTH - 200,
                      SCREEN_HEIGHT - 80, 
                      "黑子获胜局数："+str(blackWinCount), BLACK_COLOR)
        printText(screen, fontSmallText, SCREEN_WIDTH - 200,
                      SCREEN_HEIGHT - 50, 
                      "白子获胜局数："+str(whiteWinCount), BLACK_COLOR)
        if winner:
            # 在屏幕中央显示获胜和开始新一轮游戏的方法
            printText(screen, font, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//2, 
                      winner.Name+"获胜", RED_COLOR)
            printText(screen, fontSmall, 
                      (SCREEN_WIDTH - textWidth)//2 - 0.25*textWidth,
                      (SCREEN_HEIGHT - textHeight)//2 + textHeight*1.5, 
                      "请按回车开始新一局游戏", RED_COLOR)         
            # 在信息栏部分显示获胜
            if winner == WHITE_CHESSMAN:
                printText(screen, fontSmall, INFORMATION_PLACE,
                          BOARD_START_PLACE + PIECE_RADIUS_RIGHT*3, 
                          "获胜", BLUE_COLOR)
            else:
                printText(screen, fontSmall, INFORMATION_PLACE, BOARD_START_PLACE, 
                          "获胜", BLUE_COLOR)
        else: # 在信息栏部分显示当前落子状态
            if gameType == 0:
                if currentRunner == BLACK_CHESSMAN:
                    printText(screen, fontSmall, INFORMATION_PLACE, BOARD_START_PLACE, 
                          "落子中", BLUE_COLOR)
                else:
                    printText(screen, fontSmall, INFORMATION_PLACE,
                          BOARD_START_PLACE + PIECE_RADIUS_RIGHT*3, 
                          "落子中", BLUE_COLOR)
            elif gameType == 1:
                printText(screen, fontSmall, INFORMATION_PLACE, BOARD_START_PLACE, 
                          "玩家", BLUE_COLOR)
                printText(screen, fontSmall, INFORMATION_PLACE,
                          BOARD_START_PLACE + PIECE_RADIUS_RIGHT*3, 
                          "电脑", BLUE_COLOR)
                
           
        pygame.display.flip() # 更新屏幕
                        

                    
if __name__ == "__main__":
    main()