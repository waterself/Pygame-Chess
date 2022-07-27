from Chess import ChessPieces as cp


class GameState:
    canWhiteCastling = True
    canBlackCastling = True
    '''말들을 불러와서 초기화'''

    '''블랙 기물 생성'''

    bR1 = cp.Rook(-1, "bR")
    bR2 = cp.Rook(-1, "bR")
    bN1 = cp.kNight(-1, "bN")
    bN2 = cp.kNight(-1, "bN")
    bB1 = cp.Bishop(-1, "bB")
    bB2 = cp.Bishop(-1, "bB")
    bQ1 = cp.Queen(-1, "bQ")
    bK1 = cp.King(-1, "bK")
    bP1 = cp.Pawn(-1, "bP")
    bP2 = cp.Pawn(-1, "bP")
    bP3 = cp.Pawn(-1, "bP")
    bP4 = cp.Pawn(-1, "bP")
    bP5 = cp.Pawn(-1, "bP")
    bP6 = cp.Pawn(-1, "bP")
    bP7 = cp.Pawn(-1, "bP")
    bP8 = cp.Pawn(-1, "bP")

    '''white 기물 생성'''
    wR1 = cp.Rook(1, "wR")
    wR2 = cp.Rook(1, "wR")
    wN1 = cp.kNight(1, "wN")
    wN2 = cp.kNight(1, "wN")
    wB1 = cp.Bishop(1, "wB")
    wB2 = cp.Bishop(1, "wB")
    wQ1 = cp.Queen(1, "wQ")
    wK1 = cp.King(1, "wK")
    wP1 = cp.Pawn(1, "wP")
    wP2 = cp.Pawn(1, "wP")
    wP3 = cp.Pawn(1, "wP")
    wP4 = cp.Pawn(1, "wP")
    wP5 = cp.Pawn(1, "wP")
    wP6 = cp.Pawn(1, "wP")
    wP7 = cp.Pawn(1, "wP")
    wP8 = cp.Pawn(1, "wP")

    empty = cp.pieces(0, "NN")
#보드위치 정상규칙
    board = [
        [bR1, bN1, bB1, bK1, bQ1, bB2, bN2, bR2],
        [bP1, bP2, bP3, bP4, bP5, bP6, bP7, bP8],
        [empty, empty, empty, empty, empty, empty, empty, empty],
        [empty, empty, empty, empty, empty, empty, empty, empty],
        [empty, empty, empty, empty, empty, empty, empty, empty],
        [empty, empty, empty, empty, empty, empty, empty, empty],
        [wP1, wP2, wP3, wP4, wP5, wP6, wP7, wP8],
        [wR1, wN1, wB1, wQ1, wK1, wB2, wN2, wR2],
    ]

    outOfBoard = []

    def __init__(self):
        # 빈 칸에 빈 클래스로 채움
        for i in range(2, 5):
            for j in range(0, 8):
                self.board[i][j].x = i
                self.board[i][j].y = j
                self.board[i][j].name = "NN"
                # self.board[i][j].statusPrint()

    #무브 정상작동, 한번이라도 움직였는지 검사 작동
    # 행마법에 관한 룰을 각 기물의 move에 주고, move는 행마법에 맞는지 틀리는지를 true false로 반환해야 함
    # 조건 맞을 시 아래의 동작을 수행하여 빈칸과 기물의 위치를 전환
    def move(self, PC, SQ):
        # 해당 움직임이 캐슬링인지 검사
        self.isCastling(PC, SQ)
        if self.board[PC[0]][PC[1]].id == 1:
            if self.board[SQ[0]][SQ[1]].id == -1:  # 적 기물 있을 때
                self.board[PC[0]][PC[1]].moved = True # 한번 이상 이동시 True
                self.board[PC[0]][PC[1]], self.board[SQ[0]][SQ[1]] = self.board[SQ[0]][SQ[1]], self.board[PC[0]][
                    PC[1]]  # 위치교환
                self.outOfBoard.append(self.board[PC[0]][PC[1]])  # 아웃 보드에 대입
                self.board[PC[0]][PC[1]] = self.empty  # 원래자리의 기물 = 먹힌기물 빈칸처리
            elif self.board[SQ[0]][SQ[1]].id == 0:  # 빈 칸 일때
                self.board[PC[0]][PC[1]].moved = True
                self.board[PC[0]][PC[1]], self.board[SQ[0]][SQ[1]] = self.board[SQ[0]][SQ[1]], self.board[PC[0]][PC[1]]


        elif self.board[PC[0]][PC[1]].id == -1:
            if self.board[SQ[0]][SQ[1]].id == 1:  # 적 기물 일 때
                self.board[PC[0]][PC[1]].moved = True
                self.board[PC[0]][PC[1]], self.board[SQ[0]][SQ[1]] = self.board[SQ[0]][SQ[1]], self.board[PC[0]][
                    PC[1]]  # 위치교환
                self.outOfBoard.append(self.board[PC[0]][PC[1]])  # 아웃 보드에 대입
                self.board[PC[0]][PC[1]] = self.empty  # 원래자리의 기물 = 먹힌기물 빈칸처리
            elif self.board[SQ[0]][SQ[1]].id == 0:  # 빈칸일때
                self.board[PC[0]][PC[1]].moved = True # 한번 이상 이동시 True
                self.board[PC[0]][PC[1]], self.board[SQ[0]][SQ[1]] = self.board[SQ[0]][SQ[1]], self.board[PC[0]][PC[1]]

# 체크 정상작동
    def isChecked(self):
        for i in self.outOfBoard:
            if i.name == "bK":
                return 1
            elif i.name == "wK":
                return -1
            else:
                continue
        return 0
#프로모션 정상작동
    def isPromotion(self):
        for i in range(0, 8):
            if self.board[0][i].name == "wP":
                self.board[0][i] = cp.Queen(1, "wQ")
            elif self.board[7][i].name == "bP":
                self.board[7][i] = cp.Queen(-1, "bQ")
            else:
                continue
#캐슬링 정상작동
    def isCastling(self, PC, SQ):
        # PC는 원래 왕이 있던 자리, SQ는 현재 왕이 있는 자리
        if self.board[PC[0]][PC[1]].name == "wK" and self.canWhiteCastling == True and self.board[PC[0]][PC[1]].moved == False:
            if SQ[1] == PC[1] + 2: # 우측캐슬링
                rook =(7, 7)
                if self.board[rook[0]][rook[1]].moved == False:
                    self.board[rook[0]][rook[1]], self.board[7][5] = self.board[7][5], self.board[rook[0]][
                        rook[1]]
                    self.canWhiteCastling = False
            elif SQ[1] == PC[1] - 2: # 좌측캐슬링
                rook =(7, 0)
                if self.board[rook[0]][rook[1]].moved == False:
                    self.board[rook[0]][rook[1]], self.board[7][3] = self.board[7][3], self.board[rook[0]][
                        rook[1]]
                    self.canWhiteCastling = False
        elif self.board[PC[0]][PC[1]].name == "bK" and self.canBlackCastling == True and self.board[PC[0]][PC[1]].moved == False:
            if SQ[1] == PC[1] + 2:  # 우측캐슬링
                rook = (0, 7)
                if self.board[rook[0]][rook[1]].moved == False:
                    self.board[rook[0]][rook[1]], self.board[0][4] = self.board[0][4], self.board[rook[0]][
                        rook[1]]
                    self.canBlackCastling = False
            elif SQ[1] == PC[1] - 2: #좌측 캐슬링
                rook = (0, 0)
                if self.board[rook[0]][rook[1]].moved == False:
                    self.board[rook[0]][rook[1]], self.board[0][2] = self.board[0][2], self.board[rook[0]][
                        rook[1]]
                    self.canBlackCastling = False





