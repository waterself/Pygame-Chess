'''
메인 파일
'''
import pygame
import pygame as pg
import tkinter as tk
from tkinter import *
from datetime import *
from Chess import ChessBoard as cb
import os

'''
전역변수 선언
'''
WIDTH, HEIGHT = 812, 512  # 창의 크기
ColumRow = 8  # 보드판의 좌우크기
squreSize = HEIGHT // ColumRow  # 그래픽 작업에 픽셀을 칸으로 다루게 해줄 변수
maxFps = 15
TEXTCOLOR = (0, 0, 0)
TEXTBGC = (255, 255, 255)
images = {}
alphaLowImages = {}
Player1, Player2 = '', ''
# isWrite = True
'''
이미지 불러오기
'''


def loadImage():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bK", "bQ"]
    for p in pieces:
        images[p] = pg.transform.scale(pg.image.load("images/" + p + ".png"), (squreSize, squreSize))
        alphaLowImages[p] = pg.transform.scale(pg.image.load("images/" + p + ".png"), (squreSize, squreSize))
        alphaLowImages[p].set_alpha(128)


'''
마우스 입력 및 그래픽 업데이트
'''


def main():
    pg.init()  # pygame초기화
    pg.display.set_caption("Chess Game")
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pg.Color("white"))
    gs = cb.GameState()
    loadImage()
    setting()
    global Player1
    global Player2
    print("%s, %s" % (Player1, Player2))
    fileName = boardOutInit()
    winMSG = ''
    turncnt = 0
    run = True
    whiteTurn = True  # 클릭가능 기물에 제한을 주기 위함
    clickCNT = 0  # 플레이어의 클릭수
    selectPC = ()  # 튜플, (row, col)
    selectSQ = ()
    # 마우스입력이벤트
    while run:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
            elif e.type == pg.MOUSEBUTTONDOWN: #마우스 클릭시
                location = pg.mouse.get_pos()  # 클릭한 지점의 좌표
                col = location[0] // squreSize
                row = location[1] // squreSize
                if clickCNT == 0:  # 처음 클릭, 비어있을 때
                    if whiteTurn == True and gs.board[row][col].id == 1:
                        selectPC = (row, col)
                        print(selectPC)
                        drawSelect(screen, selectPC)
                        clickCNT += 1
                    elif whiteTurn == False and gs.board[row][col].id == -1:
                        selectPC = (row, col)
                        print(selectPC)
                        clickCNT += 1
                    else:
                        continue
                    # 기물이동조건이 완료되면 이동가능위치 표시구현
                elif selectPC == (row, col) and clickCNT == 1:  # 두번쨰 클릭, 같은 칸 클릭
                    selectPC = ()  # 선택칸 비움
                    selectSQ = ()
                    clickCNT = 0
                    # 턴이 안넘어가게 작동 = whiteTurn변수 조작필요
                elif selectPC != (row, col) and clickCNT == 1:  # 두번쨰 클릭, 다른 칸 클릭
                    if gs.board[selectPC[0]][selectPC[1]].canMove(selectPC[0], selectPC[1], row, col, gs.board):
                    # if True:
                        selectSQ = (row, col)
                        outName = gs.board[selectPC[0]][selectPC[1]].name
                        gs.move(selectPC, selectSQ)
                        # 기물이동 성공시
                        clickCNT = 0
                        turncnt += 1
                        # 다음 턴을 바꿔주는 코드
                        whiteTurn = turnChange(whiteTurn)
                        boardPrint(gs, turncnt, outName, selectSQ, whiteTurn)
                        boardOut(gs, turncnt, selectPC, selectSQ, whiteTurn, fileName)
                        # 프로모션 확인
                        gs.isPromotion()
                        # 킹이 잡혔는지 확인
                        chk = gs.isChecked()
                        run = isGameEnd(chk, fileName)
                    else:
                        selectPC = ()  # 선택칸 비움
                        selectSQ = ()
                        clickCNT = 0

        # 그래픽 업데이트
        drawGameState(screen, gs, whiteTurn, turncnt, selectSQ)
        drawSelect(screen, selectPC)
        if len(selectPC) == 2:
            drawCanMove(screen, gs, selectPC)
        clock.tick(maxFps)
        pg.display.flip()


'''
게임 상태를 표시해주는 함수
'''


def drawGameState(screen, gs, whiteTurn, turncnt, selectSQ):
    drawBoard(screen)
    drawPieces(screen, gs)
    drawInfo(screen, gs, whiteTurn, turncnt, selectSQ)


'''
drawGameState 구현부
'''


def drawBoard(screen):
    colors = [pg.Color("white"), pg.Color("gray")]
    for r in range(ColumRow):
        for c in range(ColumRow):
            '''white와 black을 번갈아 불러옴'''
            color = colors[((r + c) % 2)]
            pg.draw.rect(screen, color, pg.Rect(c * squreSize, r * squreSize, squreSize, squreSize))


def drawPieces(screen, gs):
    for r in range(ColumRow):
        for c in range(ColumRow):
            if gs.board[r][c].name == 'NN':
                # print("skip")
                continue
            piece = gs.board[r][c].name
            # print(piece)
            '''보드가 비어있지 않을 때, 칸에 있는 이름의 이미지를 복사해서 넣는다.'''
            if piece != "NN":
                screen.blit(images[piece], pg.Rect(c * squreSize, r * squreSize, squreSize, squreSize))


def drawCanMove(screen, gs, selectPC):
    x = selectPC[0]
    y = selectPC[1]
    # print(x, y)
    # print(gs.board[x][y].name)
    # print("drawCanMove")
    piece = gs.board[x][y].name
    for r in range(ColumRow):
        for c in range(ColumRow):
            '''canMove의 조건이 True일 때, 반투명 이미지를 출력한다.'''
            if not gs.board[x][y].canMove(x, y, r, c, gs.board):
                continue
            if gs.board[x][y].canMove(x, y, r, c, gs.board):
                screen.blit(alphaLowImages[piece], pg.Rect(c * squreSize, r * squreSize, squreSize, squreSize))


'''게임정보들을 그려줌'''

def drawSelect(screen, selectedPC):
    font = pg.font.SysFont("batang", 30, True, True)
    if len(selectedPC) == 2:
        col = 8 - selectedPC[0]
        row = chr(selectedPC[1] + 97)
    else:
        col = "      "
        row = "      "
    selectText = font.render("selected: " + str(row) + " " + str(col), True, TEXTCOLOR, TEXTBGC)
    screen.blit(selectText, pg.Rect(HEIGHT + 20, 220, 20, 10))

def drawInfo(screen, gs, whiteTurn, turncnt, selectSQ):
    global Player1
    global Player2
    turn = ''
    if whiteTurn:
        turn = "White's Turn"
    else:
        turn = "Black's Turn"
    font = pg.font.SysFont("batang", 30, True, True)
    P1Text = font.render("White: " + Player1, True, TEXTCOLOR, TEXTBGC)
    P2Text = font.render("Black: " + Player2, True, TEXTCOLOR, TEXTBGC)
    turnText = font.render(turn, True, TEXTCOLOR, TEXTBGC)
    turncntText = font.render(str(turncnt), True, TEXTCOLOR, TEXTBGC)
    screen.blit(P1Text, pg.Rect(HEIGHT + 20, 20, 20, 10))
    screen.blit(P2Text, pg.Rect(HEIGHT + 20, 70, 20, 10))
    screen.blit(turnText, pg.Rect(HEIGHT + 20, 120, 20, 10))
    screen.blit(turncntText, pg.Rect(HEIGHT + 20, 170, 20, 10))
    if len(selectSQ) == 2:
        col = selectSQ[0]
        row = chr(selectSQ[1] + 97)
        selectText = font.render("Moved: " + str(row) + " " + str(col), True, TEXTCOLOR, TEXTBGC)
        screen.blit(selectText, pg.Rect(HEIGHT + 20, 270, 20, 10))



'''게임에 필요한 조작함수'''

# 게임이 끝났는지 체크
def isGameEnd(chk, fileName):
    if chk == 1:
        endMSG("WhiteWin")
        gameLog = open("C:/ChessLog/" + fileName + ".txt", 'a')
        gameLog.write("\nWhiteWin")
        gameLog.close()
        return False
    elif chk == -1:
        endMSG("blackWin")
        gameLog = open("C:/ChessLog/" + fileName + ".txt", 'a')
        gameLog.write("\nblackWin")
        gameLog.close()
        return False
    else:
        return True

# 게임이 끝났을 때 출력할 메세지
def endMSG(msg):
    win = tk.Tk()
    win.title("ChessGame_Setting")
    win.geometry('300x150')
    win.resizable(False, False)
    # 라벨
    tk.Label(win, text=msg, font=('batang', 30, 'bold')).pack()
    tk.Label(win).pack()

    def click_me():
        win.destroy()

    # 버튼
    ok = tk.Button(win, text="Game Exit", command=click_me, font=('batang', 30, 'bold'))
    ok.pack()
    win.mainloop()

# 턴을 전환해주는 함수
def turnChange(whiteTurn):
    if whiteTurn == True:
        return False
    else:
        return True


def boardPrint(gs, turncnt, PC, SQ, turn):
    if turn != True:
        print("white's Turn")
    elif turn != False:
        print("black's Turn")
    print("Turn: %d" % (turncnt))
    print("선택한 기물: ", end=': ')
    print(PC)
    print("이동한 위치: ", end=": ")
    print(SQ)
    for i in range(0, 8):
        for j in range(0, 8):
            print(gs.board[i][j].name, end='\t')
        print()
    print("판 밖의 기물: ", end='')
    for i in gs.outOfBoard:
        print(i.name, end=', ')
    print()
    print("--------------------------------------------------")

# 파일에 기록을 남기는 함수
def boardOut(gs, turncnt, PC, SQ, turn, fileName):
    global Player1
    global Player2
    PCC = 8 - PC[0]
    PCR = chr(PC[1] + 97)
    SQC = 8 - SQ[0]
    SQR = chr(SQ[1] + 97)
    gameLog = open("C:/ChessLog/" + fileName + ".txt", 'a')
    if turn != True:
        gameLog.write("\nwhite's Turn\n")
    elif turn != False:
        gameLog.write("\nblack's Turn\n")
    gameLog.write("Turn: ")
    gameLog.write(str(turncnt))
    gameLog.write('\n')
    gameLog.write("선택한 기물: ")
    gameLog.write(str(PCR) + ', ' + str(PCC))
    gameLog.write('\n')
    gameLog.write("이동한 위치: ")
    gameLog.write(str(SQR) + ', ' + str(SQC))
    gameLog.write('\n')
    for i in range(0, 8):
        for j in range(0, 8):
            gameLog.write(gs.board[i][j].name + '\t')
        gameLog.write('\n')
    gameLog.write("판 밖의 기물: ")
    for i in gs.outOfBoard:
        gameLog.write(i.name + ', ')
    gameLog.write('\n')
    gameLog.write("----------------------------------------------------------------------------")
    gameLog.close()


'''초기설정함수'''


def setting():
    # setting = False
    win = tk.Tk()
    # 창설정
    win.title("ChessGame_Setting")
    win.geometry('300x100')
    win.resizable(False, False)
    # 라벨
    tk.Label(win, text="P1Name: ").grid(column=0, row=0)
    tk.Label(win, text="P2Name: ").grid(column=0, row=1)
    tk.Label(win, text="logDir = C:\ChessLog\ ").grid(column=0, row=2)
    # 변수 설정
    P1 = StringVar()
    P2 = StringVar()
    # chk = BooleanVar()
    # chk.set(True)
    # dir = StringVar()
    # 텍스트박스
    P1_in = tk.Entry(win, width=' 20', textvariable=P1)
    P1_in.grid(column=1, row=0, )
    P1_in.insert(END, "P1")
    P2_in = tk.Entry(win, width=' 20', textvariable=P2)
    P2_in.grid(column=1, row=1)
    P2_in.insert(END, "P2")

    # chkBox = Checkbutton(win, text="isFreeMode?", variable=chk)
    # chkBox.grid(column=1, row=2)
    # dir_in = tk.Entry(win, width='20', textvariable=dir)
    # dir_in.grid(column=1, row=2)
    # 게임실행
    def click_me():
        global Player1
        global Player2
        global isWrite
        Player1 = str(P1.get())
        Player2 = str(P2.get())
        # isWrite = bool(chk)
        win.destroy()

    # 버튼
    ok = tk.Button(win, text="Chess Start", command=click_me)
    ok.grid(column=1, row=3)
    win.mainloop()


# 로그파일을 생성
def boardOutInit():
    global Player1
    global Player2
    now = datetime.now()
    currentTime = now.strftime("%Y%m%d%H.%M.%S")
    fileName = Player1 + "_vs_" + Player2 + "_" + currentTime
    try:
        if not os.path.exists("C:/ChessLog/"):
            os.mkdir("C:/ChessLog/")
    except OSError:
        print("폴더 생성 에러")
    gameLog = open("C:/ChessLog/" + fileName + ".txt", 'w')
    gameLog.write(fileName + '\n')
    gameLog.write("----------------------------------------------------------------------------")
    gameLog.close()
    return fileName


# 메인 함수일 경우에만 실행
if __name__ == "__main__":
    main()
