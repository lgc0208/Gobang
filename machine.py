#machine.py
"""
Created on Fri May 22 20:45:00 2020

@author: Guocheng Lin
@email: lgc0208@bupt.edu.cn

Description:五子棋人机对战的机器类实现
"""
from board import BLACK_CHESSMAN, Point, offset
import random

class Machine:
    # 初始化
    def __init__(self, pointNumber, chessMan):
        self._pointNumber = pointNumber # 棋盘点的数量
        self._my = chessMan # 己方执子
        self._rival = BLACK_CHESSMAN # 敌方执子
        # 初始化棋盘，所有元素置0
        self._board = [[0] * pointNumber for i in range(pointNumber)]
    
    # 得到对手落子位置
    def getRivalDrop(self, point):
        self._board[point.Y][point.X] = self._rival.Value
    
    # 判定所给位置方向上两格的落子情况（我方1、敌方2、空0）
    def getPiece(self, point, offsetX, offsetY, TorF):
        x = point.X + offsetX # 将x赋值为当前位置+偏移量
        y = point.Y + offsetY # 将y赋值为当前位置+偏移量
        if 0 <= x < self._pointNumber and 0 <= y < self._pointNumber: # 当偏移后的值在棋盘范围内时
            if self._board[y][x] == self._my.Value: # 若落子位置偏移方向有我方棋子
                return 1 # 返回1表示是我方棋子
            elif self._board[y][x] == self._rival.Value: # 若落子位置偏移方向有敌方棋子
                return 2 # 返回2表示是敌方棋子
            else: # 若无棋子
                if TorF: # 是否继续判断
                    # 当偏移超过两次不存在棋子时，不予继续考虑
                    return self.getPiece(Point(x, y),
                                         offsetX, offsetY,
                                         False)
                else:
                    return 0 # 表示该方向两格内不存在棋子
        else:
            return 0
        
    # 统计某方向棋子权重值
    def getDirectionScore(self, point, offsetX, offsetY):
        countSelf = 0   # 落子处我方连续子数
        countOpposite = 0  # 落子处对方连续子数
        spaceSelf = None   # 我方连续子中有无空格
        spaceOpposite = None  # 对方连续子中有无空格
        blockSelf = 0    # 我方连续子两端有无阻挡
        blockOpposite = 0   # 对方连续子两端有无阻挡

        # 如果是 1 表示是边上是我方子，2 表示敌方子， 0表示无子
        flagPositive = self.getPiece(point, offsetX, offsetY, True)
        if flagPositive != 0: # 传入的偏移方向上若存在棋子
            for i in range(1, 6): # 循环判断该方向连着几个棋子
                x = point.X + i * offsetX 
                y = point.Y + i * offsetY 
                # 若加上偏移量后仍在棋盘内
                if 0 <= x < self._pointNumber and 0 <= y < self._pointNumber:
                    if flagPositive == 1: # 若该偏移方向两格内有我方棋子
                        if self._board[y][x] == self._my.Value: #若该位置有我方棋子
                            countSelf += 1 # 我方连续棋子数+1
                            if spaceSelf is False: # 若已经出现过空格，且探测到我方棋子
                                spaceSelf = True  # 空格出现在我方连续棋子之间
                        elif self._board[y][x] == self._rival.Value: # 若该位置是敌方棋子
                            blockOpposite += 1 # 敌方棋子受阻挡+1
                            break # 落子后我方安全，跳出循环
                        else: # 若该位置不存在棋子
                            if spaceSelf is None: # 第一次检测到空格时生效
                                spaceSelf = False # 表示存在空格但不在白子之间
                            else:
                                break   # 遇到第二个空格退出循环
                    elif flagPositive == 2: # 若该偏移方向上有敌方棋子
                        if self._board[y][x] == self._my.Value:
                            blockOpposite += 1 # 敌方受阻挡+1
                            break # 我方安全，跳出循环
                        elif self._board[y][x] == self._rival.Value: # 该位置存在敌方棋子
                            countOpposite += 1 # 敌方连续棋子数+1
                            if spaceOpposite is False: # 若第二次出现空格
                                spaceOpposite = True # 对方连续棋子内出现空格事件为
                        else:
                            if spaceOpposite is None: # 若第一次出现空格
                                spaceOpposite = False # 敌方连续棋子内还未出现空格
                            else:
                                break # 若在出现敌方棋子前又出现空格，我方安全，跳出循环
                else: # 偏移后触碰到棋盘边界
                    if flagPositive == 1: # 若为己方棋子
                        blockSelf += 1 # 己方棋子被堵塞量+1
                    elif flagPositive == 2: # 若为敌方棋子
                        blockOpposite += 1 # 敌方棋子被堵塞量+1

        if spaceSelf is False: # 若己方连续棋子内不存在空格
            spaceSelf = None # 重置
        if spaceOpposite is False: # 若对方连续棋子内不存在空格
            spaceOpposite = None # 重置

        # 将设定的偏移量里的X,Y增量取反，重复上述操作
        flagNegative = self.getPiece(point, -offsetX, -offsetY, True)
        if flagNegative != 0:
            for i in range(1, 6):
                x = point.X - i * offsetX
                y = point.Y - i * offsetY
                if 0 <= x < self._pointNumber and 0 <= y < self._pointNumber:
                    if flagNegative == 1:
                        if self._board[y][x] == self._my.Value:
                            countSelf += 1
                            if spaceSelf is False:
                                spaceSelf = True
                        elif self._board[y][x] == self._rival.Value:
                            blockOpposite += 1
                            break
                        else:
                            if spaceSelf is None:
                                spaceSelf = False
                            else:
                                break   # 遇到第二个空格退出
                    elif flagNegative == 2:
                        if self._board[y][x] == self._my.Value:
                            blockOpposite += 1
                            break
                        elif self._board[y][x] == self._rival.Value:
                            countOpposite += 1
                            if spaceOpposite is False:
                                spaceOpposite = True
                        else:
                            if spaceOpposite is None:
                                spaceOpposite = False
                            else:
                                break
                else:
                    if flagNegative == 1:
                        blockSelf += 1
                    elif flagNegative == 2:
                        blockOpposite += 1
        '''
        权重值划分：
        （己方连续四子>敌方连续四子）>（己方连续三子无阻挡>敌方连续三子无阻挡）>（己方连续三子有一个阻挡&&己方连续两子无阻挡
        >敌方连续三子有阻挡&&敌方连续两子无阻挡）>（己方连续两子有阻挡>敌方连续两子有阻挡）
        无空格>有空格，两种情况应在同一数量级（紧跟在括号后）
        优先级量化 8 10 80 100 800 1000 8000 10000 五组（当数值相近的时候会变成人工智障，不知为啥）
        '''
        score = 0 # 初始化权重值，判断落子选择的优先级
        if countSelf == 4: # 若己方连续四子
            score = 10000 # 优先级参考备注
        elif countOpposite == 4: # 若敌方连续四子
            score = 8000 # 优先级参考备注
        elif countSelf == 3: # 若我方连续三子
            if blockSelf == 0: # 若我方连续三子无阻挡
                score = 1000 # 优先级参考备注
            elif blockSelf == 1: # 若我方连续三子中有一个阻挡
                score = 100 # 优先级参考备注
            else:
                score = 0 # 优先级最低
        elif countOpposite == 3: # 若敌方连续三子
            if blockOpposite == 0: # 若敌方连续三子无阻挡
                score = 800 # 优先级参考备注
            elif blockOpposite == 1: # 若敌方连续三子中有一个阻挡
                score = 80 # 优先级参考备注
            else: 
                score = 0 # 优先级最低
        elif countSelf == 2: # 若己方连续两子
            if blockSelf == 0: # 若己方两子间没有阻挡
                score = 100 # 优先级参考备注
            elif blockSelf == 1: # 若两子间有一个阻挡
                score = 80 # 优先级参考备注
            else:
                score = 0 # 优先级最低
        elif countOpposite == 2: # 若敌方连续两子
            if blockOpposite == 0: # 若敌方两子间没有阻挡
                score = 10 # 优先级参考备注
            elif blockOpposite == 1: # 若敌方两子间有一个阻挡
                score = 8 # 优先级参考备注
            else: 
                score = 0 # 优先级为0
        elif countSelf == 1: # 若己方只有单个落子
            score = 10 # 优先级参考备注
        elif countOpposite == 1: # 若对方只有单个落子
            score = 8 # 优先级参考备注
        else:
            score = 0 # 优先级最低

        if spaceSelf or spaceOpposite: # 若己方或对方连续棋子内存在空格
            score /= 2 # 优先级降低

        return score # 返回优先级
    
    # 统计落子优先级
    def getPointScore(self, point):
        score = 0
        for i in offset: # 利用偏移量计算横竖撇捺落子优先级
            score += self.getDirectionScore(point, i[0], i[1])
        return score
    
    # 机器落子
    def machineDrop(self):
        point = None 
        score = 0
        # 遍历棋盘
        for i in range(self._pointNumber):
            for j in range(self._pointNumber):
                if self._board[j][i] == 0: # 寻找尚未落子的位置
                    scoreTemp = self.getPointScore(Point(i, j)) # 判断落子优先级
                    # 寻找优先级最高的落子位置
                    if scoreTemp > score: 
                        score = scoreTemp
                        point = Point(i, j)
                    elif scoreTemp == score and scoreTemp > 0:
                        radius = random.randint(0, 100)
                        if radius % 2 == 0:
                            point = Point(i, j)
        self._board[point.Y][point.X] = self._my.Value # 在优先级最高的位置落子
        return point # 返回优先级最高的位置信息