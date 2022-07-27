import pygame as pg
from Chess import ChessBoard as cb
from Chess import ChessMain as cm
import numpy as np

'''pieces'''


class pieces:
    id = 0  # 0빈칸 1이면 white -1이면 black
    name = ''  # 이미지파일 로딩등에 사용
    moved = False
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def canMove(self, x, y, r, c, board):
        pass

    def statusPrint(self):
        print(self.x, self.y, self.name)


''' 말들의 구현'''

#정상작동
class Pawn(pieces):
    def canMove(self, x, y, r, c, board):
        try:
            if board[x][y].id == 1:  # white일때
                # 처음 칸으로 다시 돌아올 수 없음
                if x == 6 and self.moved == False:
                    if board[x - 2][y].id == 0 and x - 2 == r and y == c:
                        return True
                if board[x - 1][y].id == 0 and x - 1 == r and y == c:  # 앞에칸 id 0이고 좌표맞을때
                    return True
                elif board[x - 1][y - 1].id == -1 and x - 1 == r and y - 1 == c:
                    return True
                elif board[x - 1][y + 1].id == -1 and x - 1 == r and y + 1 == c:
                    return True
                else:
                    return False
            elif board[x][y].id == -1:  # black일때
                if x == 1 and self.moved == False:
                    if board[x + 2][y].id == 0 and x + 2 == r and y == c:
                        return True
                if board[x + 1][y].id == 0 and x + 1 == r and y == c:  # 앞에칸 id 0이고 좌표맞을때
                    return True
                elif board[x + 1][y - 1].id == 1 and x + 1 == r and y - 1 == c:
                    return True
                elif board[x + 1][y + 1].id == 1 and x + 1 == r and y + 1 == c:
                    return True
                else:
                    return False
            else:
                return False
        except IndexError:
            return False

# 정상작동
class Rook(pieces):
    # x시작, x끝, y시작, y끝 구하기
    def canMove(self, x, y, r, c, board):
        xRange, yRange = [], []
        try:
            # white일 때
            if board[x][y].id == 1:
                # x에서 위로
                for i in range(x - 1, -1, -1):
                    if board[i][y].id == 1:
                        break
                    elif board[i][y].id == -1:
                        xRange.append(i)
                        break
                    elif board[i][y].id == 0:
                        xRange.append(i)
                    # x에서 아래로
                for i in range(x + 1, 8, 1):
                    if board[i][y].id == 1:
                        break
                    elif board[i][y].id == -1:
                        xRange.append(i)
                        break
                    elif board[i][y].id == 0:
                        xRange.append(i)
                # Y에서 위로
                for i in range(y - 1, -1, -1):
                    if board[x][i].id == 1:
                        break
                    elif board[x][i].id == -1:
                        yRange.append(i)
                        break
                    elif board[x][i].id == 0:
                        yRange.append(i)
                    # Y에서 아래로
                for i in range(y + 1, 8, 1):
                    if board[x][i].id == 1:
                        break
                    elif board[x][i].id == -1:
                        yRange.append(i)
                        break
                    elif board[x][i].id == 0:
                        yRange.append(i)
            # black일 때
            elif board[x][y].id == -1:
                # 이동가능한 X 내 말에 막히면 그만하고, 적 말에 막히면 어팬드, 브레이크 안막히고 빈칸이면 어팬드
                # x에서 위로
                for i in range(x - 1, -1, -1):
                    if board[i][y].id == -1:
                        break
                    elif board[i][y].id == 1:
                        xRange.append(i)
                        break
                    elif board[i][y].id == 0:
                        xRange.append(i)
                    # x에서 아래로
                for i in range(x + 1, 8, 1):
                    if board[i][y].id == -1:
                        break
                    elif board[i][y].id == 1:
                        xRange.append(i)
                        break
                    elif board[i][y].id == 0:
                        xRange.append(i)
                # Y에서 위로
                for i in range(y - 1, -1, -1):
                    if board[x][i].id == -1:
                        break
                    elif board[x][i].id == 1:
                        yRange.append(i)
                        break
                    elif board[x][i].id == 0:
                        yRange.append(i)
                    # x에서 아래로
                for i in range(y + 1, 8, 1):
                    if board[x][i].id == -1:
                        break
                    elif board[x][i].id == 1:
                        yRange.append(i)
                        break
                    elif board[x][i].id == 0:
                        yRange.append(i)

            if r == x or c == y:
                if r in xRange or c in yRange:
                    return True
                else:
                    return False

        except IndexError:
            return False

#정상작동
class kNight(pieces):
    def canMove(self, x, y, r, c, board):
        Range = []
        sq = ()
        try:
            if board[x][y].id == 1:  # white일때
                # 두칸 세로축이동의 경우
                if -1 < x - 2 < 8 and -1 < y - 1 < 8:
                    if board[x - 2][y - 1].id != 1:  # 이동할 칸이 우리팀이 아니고 좌표가 맞을 때
                        Range.append((x - 2, y - 1))
                if -1 < x - 2 < 8 and -1 < y + 1 < 8:
                    if board[x - 2][y + 1].id != 1:
                        Range.append((x - 2, y + 1))
                if -1 < x + 2 < 8 and -1 < y - 1 < 8:
                    if board[x + 2][y - 1].id != 1:
                        Range.append((x + 2, y - 1))
                if -1 < x + 2 < 8 and -1 < y + 1 < 8:
                    if board[x + 2][y + 1].id != 1:
                        Range.append((x + 2, y + 1))

                # 두칸 가로축이동의 경우
                if -1 < x - 1 < 8 and -1 < y - 2 < 8:
                    if board[x - 1][y - 2].id != 1:
                        Range.append((x - 1, y - 2))
                if -1 < x + 1 < 8 and -1 < y - 2 < 8:
                    if board[x + 1][y - 2].id != 1:
                        Range.append((x + 1, y - 2))
                if -1 < x - 1 < 8 and -1 < y + 2 < 8:
                    if board[x - 1][y + 2].id != 1:
                        Range.append((x - 1, y + 2))
                if -1 < x + 1 < 8 and -1 < y + 2 < 8:
                    if board[x + 1][y + 2].id != 1:
                        Range.append((x + 1, y + 2))

            elif board[x][y].id == -1:  # black일때
                # 두칸 x축이동의 경우
                if -1 < x - 2 < 8 and -1 < y - 1 < 8:
                    if board[x - 2][y - 1].id != -1:  # 이동할 칸이 우리팀이 아니고 좌표가 맞을 때
                        Range.append((x - 2, y - 1))
                if -1 < x - 2 < 8 and -1 < y + 1 < 8:
                    if board[x - 2][y + 1].id != -1:
                        Range.append((x - 2, y + 1))
                if -1 < x + 2 < 8 and -1 < y - 1 < 8:
                    if board[x + 2][y - 1].id != -1:
                        Range.append((x + 2, y - 1))
                if -1 < x + 2 < 8 and -1 < y + 1 < 8:
                    if board[x + 2][y + 1].id != -1:
                        Range.append((x + 2, y + 1))
                # 두칸 y축이동의 경우
                if -1 < x - 1 < 8 and -1 < y - 2 < 8:
                    if board[x - 1][y - 2].id != -1:
                        Range.append((x - 1, y - 2))
                if -1 < x + 1 < 8 and -1 < y - 2 < 8:
                    if board[x + 1][y - 2].id != -1:
                        Range.append((x + 1, y - 2))
                if -1 < x - 1 < 8 and -1 < y + 2 < 8:
                    if board[x - 1][y + 2].id != -1:
                        Range.append((x - 1, y + 2))
                if -1 < x + 1 < 8 and -1 < y + 2 < 8:
                    if board[x + 1][y + 2].id != -1:
                        Range.append((x + 1, y + 2))

            rc = (r, c)
            if rc in Range:
                return True
            else:
                return False

        except IndexError:
            return False


#정상작동
class Bishop(pieces):
    def canMove(self, x, y, r, c, board):
        Range = []
        sq = ()
        try:
            # white일 때
            if board[x][y].id == 1:
                # 상, 좌
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y - i < 8:
                        if board[x - i][y - i].id == 1:
                            break
                        elif board[x - i][y - i].id == -1:
                            sq = (x - i, y - i)
                            Range.append(sq)
                            break
                        elif board[x - i][y - i].id == 0:
                            sq = (x - i, y - i)
                            Range.append(sq)
                    # x에서 하 우로 움직일 때
                for i in range(1, 8):
                    if -1 < x + i < 8 and -1 < y + i < 8:
                        if board[x + i][y + i].id == 1:
                            break
                        elif board[x + i][y + i].id == -1:
                            sq = (x + i, y + i)
                            Range.append(sq)
                            break
                        elif board[x + i][y + i].id == 0:
                            sq = (x + i, y + i)
                            Range.append(sq)
                    # Y에서 상, 우로 움직일 때
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y + i < 8:
                        if board[x - i][y + i].id == 1:
                            break
                        elif board[x - i][y + i].id == -1:
                            sq = (x - i, y + i)
                            Range.append(sq)
                            break
                        elif board[x - i][y + i].id == 0:
                            sq = (x - i, y + i)
                            Range.append(sq)
                    # y에서 하, 좌로 움직일 때
                for i in range(1, 8):
                    if -1 < x + i < 8 and -1 < y - i < 8:
                        if board[x + i][y - i].id == 1:
                            break
                        elif board[x + i][y - i].id == -1:
                            sq = (x + i, y - i)
                            Range.append(sq)
                            break
                        elif board[x + i][y - i].id == 0:
                            sq = (x + i, y - i)
                            Range.append(sq)


            elif board[x][y].id == -1:  # black일 때
                # 이동가능한 X 내 말에 막히면 그만하고, 적 말에 막히면 어팬드, 브레이크 안막히고 빈칸이면 어팬드
                # x에서 상좌
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y - i < 8:
                        if board[x - i][y - i].id == -1:
                            break
                        elif board[x - i][y - i].id == 1:
                            sq = (x - i, y - i)
                            Range.append(sq)
                            break
                        elif board[x - i][y - i].id == 0:
                            sq = (x - i, y - i)
                            Range.append(sq)
                    # x에서 하 우로 움직일 때
                for i in range(1, 8):
                    if -1 < x + i < 8 and -1 < y + i < 8:
                        if board[x + i][y + i].id == -1:
                            break
                        elif board[x + i][y + i].id == 1:
                            sq = (x + i, y + i)
                            Range.append(sq)
                            break
                        elif board[x + i][y + i].id == 0:
                            sq = (x + i, y + i)
                            Range.append(sq)
                    # Y에서 상, 우로 움직일 때
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y + i < 8:
                        if board[x - i][y + i].id == -1:
                            break
                        elif board[x - i][y + i].id == 1:
                            sq = (x - i, y + i)
                            Range.append(sq)
                            break
                        elif board[x - i][y + i].id == 0:
                            sq = (x - i, y + i)
                            Range.append(sq)
                    # y에서 하, 좌로 움직일 때
                for i in range(1, 8):
                    if -1 < x + i < 8 and -1 < y - i < 8:
                        if board[x + i][y - i].id == -1:
                            break
                        elif board[x + i][y - i].id == 1:
                            sq = (x + i, y - i)
                            Range.append(sq)
                            break
                        elif board[x + i][y - i].id == 0:
                            sq = (x + i, y - i)
                            Range.append(sq)

            rc = (r, c)
            if rc in Range:
                return True
            else:
                return False

        except IndexError:
            print("IndexError")
            return False


'''
비숍과 퀸을 합쳐 이동 가능한 칸의 튜플의 리스트를 append 할 것
'''

# 정상작동
class Queen(pieces):
    def canMove(self, x, y, r, c, board):
        Range = []
        sq = ()
        try:
            # white일 때
            if board[x][y].id == 1:
                # 상, 좌
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y - i < 8:
                        if board[x - i][y - i].id == 1:
                            break
                        elif board[x - i][y - i].id == -1:
                            sq = (x - i, y - i)
                            Range.append(sq)
                            break
                        elif board[x - i][y - i].id == 0:
                            sq = (x - i, y - i)
                            Range.append(sq)
                    # x에서 하 우로 움직일 때
                for i in range(1, 8):
                    if -1 < x + i < 8 and -1 < y + i < 8:
                        if board[x + i][y + i].id == 1:
                            break
                        elif board[x + i][y + i].id == -1:
                            sq = (x + i, y + i)
                            Range.append(sq)
                            break
                        elif board[x + i][y + i].id == 0:
                            sq = (x + i, y + i)
                            Range.append(sq)
                    # Y에서 상, 우로 움직일 때
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y + i < 8:
                        if board[x - i][y + i].id == 1:
                            break
                        elif board[x - i][y + i].id == -1:
                            sq = (x - i, y + i)
                            Range.append(sq)
                            break
                        elif board[x - i][y + i].id == 0:
                            sq = (x - i, y + i)
                            Range.append(sq)
                    # y에서 하, 좌로 움직일 때
                for i in range(1, 8):
                    if -1 < x + i < 8 and -1 < y - i < 8:
                        if board[x + i][y - i].id == 1:
                            break
                        elif board[x + i][y - i].id == -1:
                            sq = (x + i, y - i)
                            Range.append(sq)
                            break
                        elif board[x + i][y - i].id == 0:
                            sq = (x + i, y - i)
                            Range.append(sq)
                # 상하좌우 체크
                # 상
                for i in range(1, 8):
                    if -1 < x - i < 8:
                        if board[x - i][y].id == 1:
                            break
                        elif board[x - i][y].id == -1:
                            sq = (x - i, y)
                            Range.append(sq)
                            break
                        elif board[x - i][y].id == 0:
                            sq = (x - i, y)
                            Range.append(sq)
                    # 하
                for i in range(1, 8):
                    if -1 < x + i < 8:
                        if board[x + i][y].id == 1:
                            break
                        elif board[x + i][y].id == -1:
                            sq = (x + i, y)
                            Range.append(sq)
                            break
                        elif board[x + i][y].id == 0:
                            sq = (x + i, y)
                            Range.append(sq)
                    # 우
                for i in range(1, 8):
                    if -1 < y + i < 8:
                        if board[x][y + i].id == 1:
                            break
                        elif board[x][y + i].id == -1:
                            sq = (x, y + i)
                            Range.append(sq)
                            break
                        elif board[x][y + i].id == 0:
                            sq = (x, y + i)
                            Range.append(sq)
                    # 우
                for i in range(1, 8):
                    if -1 < y - i < 8:
                        if board[x][y - i].id == 1:
                            break
                        elif board[x][y - i].id == -1:
                            sq = (x, y - i)
                            Range.append(sq)
                            break
                        elif board[x][y - i].id == 0:
                            sq = (x, y - i)
                            Range.append(sq)




            elif board[x][y].id == -1:  # black일 때
                # 이동가능한 X 내 말에 막히면 그만하고, 적 말에 막히면 어팬드, 브레이크 안막히고 빈칸이면 어팬드
                # x에서 상좌
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y - i < 8:
                        if board[x - i][y - i].id == -1:
                            break
                        elif board[x - i][y - i].id == 1:
                            sq = (x - i, y - i)
                            Range.append(sq)
                            break
                        elif board[x - i][y - i].id == 0:
                            sq = (x - i, y - i)
                            Range.append(sq)
                    # x에서 하 우로 움직일 때
                for i in range(1, 8):
                    if -1 < x + i < 8 and -1 < y + i < 8:
                        if board[x + i][y + i].id == -1:
                            break
                        elif board[x + i][y + i].id == 1:
                            sq = (x + i, y + i)
                            Range.append(sq)
                            break
                        elif board[x + i][y + i].id == 0:
                            sq = (x + i, y + i)
                            Range.append(sq)
                    # Y에서 상, 우로 움직일 때
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y + i < 8:
                        if board[x - i][y + i].id == -1:
                            break
                        elif board[x - i][y + i].id == 1:
                            sq = (x - i, y + i)
                            Range.append(sq)
                            break
                        elif board[x - i][y + i].id == 0:
                            sq = (x - i, y + i)
                            Range.append(sq)
                    # y에서 하, 좌로 움직일 때
                for i in range(1, 8):
                    if -1 < x - i < 8 and -1 < y + i < 8:
                        if board[x + i][y - i].id == -1:
                            break
                        elif board[x + i][y - i].id == 1:
                            sq = (x + i, y - i)
                            Range.append(sq)
                            break
                        elif board[x + i][y - i].id == 0:
                            sq = (x + i, y - i)
                            Range.append(sq)
                # 상하좌우 체크
                # 상
                for i in range(1, 8):
                    if -1 < x - i < 8:
                        if board[x - i][y].id == -1:
                            break
                        elif board[x - i][y].id == 1:
                            sq = (x - i, y)
                            Range.append(sq)
                            break
                        elif board[x - i][y].id == 0:
                            sq = (x - i, y)
                            Range.append(sq)
                    # 하
                for i in range(1, 8):
                    if -1 < x + i < 8:
                        if board[x + i][y].id == -1:
                            break
                        elif board[x + i][y].id == 1:
                            sq = (x + i, y)
                            Range.append(sq)
                            break
                        elif board[x + i][y].id == 0:
                            sq = (x + i, y)
                            Range.append(sq)
                    # 우
                for i in range(1, 8):
                    if -1 < y + i < 8:
                        if board[x][y + i].id == -1:
                            break
                        elif board[x][y + i].id == 1:
                            sq = (x, y + i)
                            Range.append(sq)
                            break
                        elif board[x][y + i].id == 0:
                            sq = (x, y + i)
                            Range.append(sq)
                    # 우
                for i in range(1, 8):
                    if -1 < y - i < 8:
                        if board[x][y - i].id == -1:
                            break
                        elif board[x][y - i].id == 1:
                            sq = (x, y - i)
                            Range.append(sq)
                            break
                        elif board[x][y - i].id == 0:
                            sq = (x, y - i)
                            Range.append(sq)

            rc = (r, c)
            if rc in Range:
                return True
            else:
                return False

        except IndexError:
            print("IndexError")
            return False

# 정상작동
class King(pieces):
    def canMove(self, x, y, r, c, board):
        xm1, xp1, ym1, yp1 = x - 1, x + 1, y - 1, y + 1
        Range = []
        sq = ()
        try:
            # white일 때
            if board[x][y].id == 1:
                # 우측캐슬링
                if self.moved == False and board[7][7].id == 1 and board[7][7].moved == False:
                    cnt = 0
                    for i in range(1, 3):
                        if board[x][y + i].id == 0:
                            cnt += 1
                    if cnt == 2:
                        Range.append((x, y + 2))
                #좌측 캐슬링
                if self.moved == False and board[7][0].id == 1 and board[7][0].moved == False:
                    cnt = 0
                    for i in range(1, 4):
                        if board[x][y - i].id == 0:
                            cnt += 1
                    if cnt == 3:
                        Range.append((x, y - 2))
                # 상
                if -1 < xm1 < 8:
                    if board[xm1][y].id != 1:
                        Range.append((xm1, y))
                # 하
                if -1 < xp1 < 8:
                    if board[xp1][y].id != 1:
                        Range.append((xp1, y))
                # 우
                if -1 < yp1 < 8:
                    if board[x][yp1].id != 1:
                        Range.append((x, yp1))
                # 좌
                if -1 < ym1 < 8:
                    if board[x][ym1].id != 1:
                        Range.append((x, ym1))
                # 좌상
                if -1 < xm1 < 8 and -1 < ym1 < 8:
                    if board[xm1][ym1].id != 1:
                        Range.append((xm1, ym1))
                # 좌하
                if -1 < xp1 < 8 and -1 < ym1 < 8:
                    if board[xp1][ym1].id != 1:
                        Range.append((xp1, ym1))
                # 우상
                if -1 < xm1 < 8 and -1 < yp1 < 8:
                    if board[xm1][yp1].id != 1:
                        Range.append((xm1, yp1))
                if -1 < xp1 < 8 and -1 < yp1 < 8:
                    if board[x + 1][y + 1].id != 1:
                        Range.append((x + 1, y + 1))

            # black일 때
            elif board[x][y].id == -1:
                # 우측캐슬링
                if self.moved == False and board[0][7].id == -1 and board[0][7].moved == False:
                    cnt = 0
                    for i in range(1, 4):
                        if board[x][y + i].id == 0:
                            cnt += 1
                    if cnt == 3:
                        Range.append((x, y + 2))
                #좌측 캐슬링
                if self.moved == False and board[0][0].id == -1 and board[0][0].moved == False:
                    cnt = 0
                    for i in range(1, 3):
                        if board[x][y - i].id == 0:
                            cnt += 1
                    if cnt == 2:
                        Range.append((x, y - 2))
                # 상
                if -1 < xm1 < 8:
                    if board[xm1][y].id != -1:
                        Range.append((xm1, y))
                # 하
                if -1 < xp1 < 8:
                    if board[xp1][y].id != -1:
                        Range.append((xp1, y))
                # 우
                if -1 < yp1 < 8:
                    if board[x][yp1].id != -1:
                        Range.append((x, yp1))
                # 좌
                if -1 < ym1 < 8:
                    if board[x][ym1].id != -1:
                        Range.append((x, ym1))
                # 좌상
                if -1 < xm1 < 8 and -1 < ym1 < 8:
                    if board[xm1][ym1].id != -1:
                        Range.append((xm1, ym1))
                # 좌하
                if -1 < xp1 < 8 and -1 < ym1 < 8:
                    if board[xp1][ym1].id != -1:
                        Range.append((xp1, ym1))
                # 우상
                if -1 < xm1 < 8 and -1 < yp1 < 8:
                    if board[xm1][yp1].id != -1:
                        Range.append((xm1, yp1))
                if -1 < xp1 < 8 and -1 < yp1 < 8:
                    if board[x + 1][y + 1].id != -1:
                        Range.append((x + 1, y + 1))

            rc = (r, c)
            if rc in Range:
                return True
            else:
                return False

        except IndexError:
            return False
