import turtle

SCREEN = turtle.Screen()
ROWS = 7
COLS = 6
STARTX = -450
STARTY = -450 * (ROWS / COLS)
WIDTH = -2 * STARTX
HEIGHT = -2 * STARTY
RADIUS = 48
BOARD = []
TURN = 1


def draw_rectangle(x, y, w, h, color):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.goto(x+w, y)
    turtle.goto(x+w, y+h)
    turtle.goto(x, y+h)
    turtle.goto(x, y)
    turtle.end_fill()


def draw_circle(x, y, r, color):
    turtle.penup()
    turtle.goto(x, y-r)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.circle(r)
    turtle.end_fill()


def draw_pieces(board, X, Y, radius, i, j):
    board_legend = {0 : "white", 1 : "red", 2 : "yellow"}
    for i in range(ROWS):
        for j in range(COLS):
            left_x = STARTX + j*(WIDTH/COLS)
            right_x = STARTX + (j+1)*(WIDTH/COLS)
            left_y = STARTY + i*(HEIGHT/ROWS)
            right_y = STARTY + (i+1)*(HEIGHT/ROWS)
            draw_circle((left_x+right_x)/2, (left_y+right_y)/2, radius, board_legend[board[i][j]])


def draw_board(board):
    draw_rectangle(STARTX, STARTY, WIDTH, HEIGHT, "blue")
    draw_pieces(board, STARTX, STARTY, RADIUS, WIDTH, HEIGHT)


def init_board():
    global BOARD, SCREEN

    SCREEN.setup(500, 500)
    SCREEN.setworldcoordinates(-500, -500, 500, 500)
    SCREEN.title("Connect 4")
    SCREEN.bgcolor("white")
    turtle.speed(0)
    turtle.hideturtle()
    SCREEN.tracer(0, 0)

    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(0)
        BOARD.append(row)

    draw_board(BOARD)


def play(x, y):
    global BOARD, TURN
    board_legend = {0 : "white", 1 : "red", 2 : "yellow"}
    TURN_DONE = False
    for i in range(ROWS):
        for j in range(COLS):
            left_x = STARTX + j*(WIDTH/COLS)
            right_x = STARTX + (j+1)*(WIDTH/COLS)
            if x >= left_x and x <= right_x:
                for k in range(ROWS):
                    if TURN_DONE:
                        break
                    if BOARD[k][j] == 0:
                        left_y = STARTY + (k)*(HEIGHT/ROWS)
                        right_y = STARTY + (k+1)*(HEIGHT/ROWS)
                        BOARD[k][j] = TURN
                        draw_circle((left_x+right_x)/2, (left_y+right_y)/2, RADIUS, board_legend[TURN])
                        TURN = 2 if TURN == 1 else 1
                        TURN_DONE = True

    # Getting all possible combinations
    combinations = []
    for i in range(ROWS):
        for j in range(COLS):
            combo_vertical, combo_horizontal, combo_diagonal_1, combo_diagonal_2 = [], [], [], []
            for k in range(4):
                if i+k < 7: combo_vertical.append(BOARD[i+k][j])
                if j+k < 6: combo_horizontal.append(BOARD[i][j+k])
                if i+k < 7 and j+k < 6: combo_diagonal_1.append(BOARD[i+k][j+k])
                if j+k < 6 and i-k >= 0: combo_diagonal_2.append(BOARD[i-k][j+k])
            combinations.append(combo_vertical)
            combinations.append(combo_horizontal)
            combinations.append(combo_diagonal_1)
            combinations.append(combo_diagonal_2)

    text = None
    for combo in combinations:
        if len(combo) == 4 and len(set(combo)) == 1 and combo[0] != 0:
            if combo[0] == 1: text = "PLAYER 'RED' WON."
            if combo[0] == 2: text = "PLAYER 'YELLOW' WON."

    if not text:
        empty = 0
        for i in range(ROWS):
            for j in range(COLS):
                if BOARD[i][j]: empty += 1
        if not empty: text = "IT IS A TIE."

    if text:
        turtle.textinput("GAME OVER", text + " Would you like to play again?")
        SCREEN.clear()
        BOARD = []
        TURN = 1
        init_board()
        SCREEN.onclick(play)
        SCREEN.mainloop()


if __name__ == "__main__":
    init_board()
    SCREEN.onclick(play)
    SCREEN.mainloop()
