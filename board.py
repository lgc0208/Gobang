#board.py
"""
Created on Wed May 20 16:03:37 2020

@author: Guocheng Lin
@email: lgc0208@bupt.edu.cn

Description:五子棋的棋盘及基本功能判断实现
"""

import collections # 从collections导入nametuple

# 存储棋子及其颜色序列
chessMan = collections.namedtuple("chess", ["Name", "Value", "Color"]) 
Point = collections.namedtuple("point", ["X", "Y"]) # 存取点坐标序列

offset = [(1, 0), (0, 1), (1, 1), (1, -1)] #横竖撇捺判断棋子附近是否有其它棋子

# 初始化黑白子参数，黑子用1替代进行判断，白子用2替代进行判断
BLACK_CHESSMAN = chessMan("黑子", 1, (0, 0, 0))
WHITE_CHESSMAN = chessMan("白子", 2, (255, 255, 255))

# 创建棋盘类
class Board: 
    
    # 构造函数(!!!双下划线)
    def __init__(self, pointNumber): 
        self._linePoints = pointNumber # 定义成员
        # 用数组实例化棋盘，建立pointNumber个数组成员，初始值都赋值为0
        self._board = [[0] * pointNumber for i in range(pointNumber)]
    
    # 返回_board成员
    def _getBoard(self): 
        return self._board
   
    board = property(_getBoard) # 调用类中的函数
     
    # 判断是否落子
    def ifDropChess(self, point):
        if self._board[point.Y][point.X] == 0: # 若该位置无棋子
            return True
        else: 
            return False
    
    #通过横竖撇捺四个方向计算是否五子连珠
    def countDirection(self, point, value, offsetX, offsetY):
        count = 1 # 计算连珠个数
        
        # 判断所下棋子右侧是否五子连珠
        for i in range(1, 5):
            x = point.X + i*offsetX
            y = point.Y + i*offsetY
            if 0 <= x < self._linePoints \
            and 0 <= y < self._linePoints \
            and value == self._board[y][x]:
                count += 1
            else:
                break
            
        # 判断所下棋子左侧是否五子连珠
        for i in range(1, 5):
            x = point.X - i*offsetX
            y = point.Y - i*offsetY
            if 0 <= x < self._linePoints \
                and 0 <= y < self._linePoints \
                and value == self._board[y][x]:
                count += 1
            else:
                break
            
        judgeWin = (count >= 5) # 判断是否达成五子连珠，达成为True
        return judgeWin # 返回判断结果
    
    # 判断是否胜利
    def win(self, point):
        currentValue = self._board[point.Y][point.X] #得到当前值
        for offsetArray in offset: # 循环判断四个方向是否五子连珠
            if self.countDirection(point, currentValue, 
                                   offsetArray[0], 
                                   offsetArray[1]):
                return True # 若if中的判断结果为True，则返回True
            
    #落子 chessMan表示棋子，point表示落子位置
    def dropChess(self, chessMan, point):
        # print带f可执行字符串中的表达式
        print(f"{chessMan.Name}({point.X}, {point.Y})")
        self._board[point.Y][point.X] = chessMan.Value
        if self.win(point): #若胜利，显示结果；若失败，不执行
            print(f"{chessMan.Name}获胜啦！")
            return chessMan 


