import tkinter as tk
from tkinter import messagebox
import winsound   

board = [" " for _ in range(9)]
buttons = []

PLAYER = "X"
AI = "O"

player_score = 0
ai_score = 0
draw_score = 0

BG_COLOR = "#FDEDEC"
X_COLOR = "#1F618D"
O_COLOR = "#117864"
WIN_COLOR = "#F7DC6F"
BTN_COLOR = "white"

def click_sound():
    winsound.Beep(800, 100)

def win_sound():
    winsound.Beep(1200, 300)

def lose_sound():
    winsound.Beep(400, 400)

def draw_sound():
    winsound.Beep(700, 300)

def check_winner(b, player):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for w in wins:
        if b[w[0]] == b[w[1]] == b[w[2]] == player:
            return w
    return None

def is_draw(b):
    return " " not in b

def minimax(b, is_maximizing):
    if check_winner(b, AI):
        return 1
    if check_winner(b, PLAYER):
        return -1
    if is_draw(b):
        return 0

    if is_maximizing:
        best = -100
        for i in range(9):
            if b[i] == " ":
                b[i] = AI
                score = minimax(b, False)
                b[i] = " "
                best = max(best, score)
        return best
    else:
        best = 100
        for i in range(9):
            if b[i] == " ":
                b[i] = PLAYER
                score = minimax(b, True)
                b[i] = " "
                best = min(best, score)
        return best

def ai_move():
    best_score = -100
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = AI
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i

    board[move] = AI
    buttons[move].config(text=AI, fg=O_COLOR)
    check_game_over()

def button_click(i):
    if board[i] == " ":
        click_sound()
        board[i] = PLAYER
        buttons[i].config(text=PLAYER, fg=X_COLOR)
        if not check_game_over():
            window.after(300, ai_move)


def check_game_over():
    global player_score, ai_score, draw_score

    win_x = check_winner(board, PLAYER)
    win_o = check_winner(board, AI)

    if win_x:
        win_sound()
        highlight(win_x)
        player_score += 1
        update_score()
        messagebox.showinfo("Game Over", "🎉 You Win!")
        reset_board()
        return True

    if win_o:
        lose_sound()
        highlight(win_o)
        ai_score += 1
        update_score()
        messagebox.showinfo("Game Over", "🤖 AI Wins!")
        reset_board()
        return True

    if is_draw(board):
        draw_sound()
        draw_score += 1
        update_score()
        messagebox.showinfo("Game Over", "😐 It's a Draw")
        reset_board()
        return True

    return False

def highlight(cells):
    for i in cells:
        buttons[i].config(bg=WIN_COLOR)


def reset_board():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text=" ", bg=BTN_COLOR)


def restart_game():
    global player_score, ai_score, draw_score
    player_score = ai_score = draw_score = 0
    update_score()
    reset_board()


def update_score():
    score_label.config(
        text=f"You (X): {player_score}    AI (O): {ai_score}    Draws: {draw_score}"
    )

window = tk.Tk()
window.title("Colorful Tic-Tac-Toe AI")
window.config(bg=BG_COLOR)

score_label = tk.Label(
    window,
    text="You (X): 0    AI (O): 0    Draws: 0",
    font=("Arial", 12, "bold"),
    bg=BG_COLOR
)
score_label.pack(pady=10)

frame = tk.Frame(window, bg=BG_COLOR)
frame.pack()

for i in range(9):
    btn = tk.Button(
        frame,
        text=" ",
        font=("Arial", 22, "bold"),
        width=5,
        height=2,
        bg=BTN_COLOR,
        command=lambda i=i: button_click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

restart_btn = tk.Button(
    window,
    text="Restart Game",
    font=("Arial", 12, "bold"),
    bg="#FF69B4",

    fg="white",
    padx=10,
    command=restart_game
)
restart_btn.pack(pady=10)

window.mainloop()
