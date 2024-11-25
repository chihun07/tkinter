import tkinter as tk
from tkinter import messagebox

def start_game():
    game_over = False
    # Initialize the game board and moves lists
    board = [" " for _ in range(9)]
    player_moves = []
    computer_moves = []
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    # Create the Tic Tac Toe game window
    game_window = tk.Toplevel()
    game_window.title("Tic Tac Toe")

    # Create a list to store button widgets for easy access
    buttons = []

    for i in range(9):
        button = tk.Button(game_window, text=" ", font=("Arial", 24), width=5, height=2,
                           command=lambda i=i: player_move(i))  # 각 버튼에 고유 인덱스 전달
        button.grid(row=i // 3, column=i % 3)
        buttons.append(button)

    def update_board():
        """Refresh the GUI to show current board state."""
        for i in range(9):
            buttons[i]["text"] = board[i]

    def check_win():
        nonlocal game_over  # 전역 변수 사용

        if game_over:  # 이미 게임이 종료된 경우, 함수를 종료
            return

        for win in win_conditions:
            if all(pos in player_moves for pos in win):
                label = tk.Label(game_window, text="승리!")
                label.grid(row=4, column=0, columnspan=3, pady=10)  # grid 사용
                game_over = True  # 게임 종료 상태 설정
                return
            elif all(pos in computer_moves for pos in win):
                label = tk.Label(game_window, text="패배!")
                label.grid(row=4, column=0, columnspan=3, pady=10)  # grid 사용
                game_over = True  # 게임 종료 상태 설정
                return

        # 무승부 확인
        if all(cell != " " for cell in board):
            label = tk.Label(game_window, text="무승부!")
            label.grid(row=4, column=0, columnspan=3, pady=10)  # grid 사용
            game_over = True  # 게임 종료 상태 설정

    def player_move(index):
        """플레이어가 선택한 셀을 처리하는 함수."""
        if board[index] == " " and not game_over:  # 게임이 종료되지 않았고 해당 칸이 비어있을 때
            board[index] = "O"
            buttons[index].config(text="O", state='disabled')  # 텍스트만 파란색으로 설정
            player_moves.append(index)
            check_win()  # 승리 조건을 확인
            if not game_over:  # 게임이 끝나지 않았다면 컴퓨터 턴으로 넘어감
                computer_move()

    def computer_move():
        """Computer's strategy for making a move."""
        # Check if computer can win
        for win in win_conditions:
            if sum(1 for pos in win if pos in computer_moves) == 2:
                empty_pos = [pos for pos in win if board[pos] == " "]
                if empty_pos:
                    board[empty_pos[0]] = "X"
                    computer_moves.append(empty_pos[0])
                    update_board()
                    check_win()
                    return
        for win in win_conditions:
            if sum(1 for pos in win if pos in player_moves) == 2:
                empty_pos = [pos for pos in win if board[pos] == " "]
                if empty_pos:
                    board[empty_pos[0]] = "X"
                    computer_moves.append(empty_pos[0])
                    update_board()
                    check_win()
                    return
        # Random move if no winning move is available
        empty_cells = [i for i in range(9) if board[i] == " "]
        if empty_cells:
            move = empty_cells[0]  # Select the first available cell
            board[move] = "X"
            computer_moves.append(move)
            update_board()
            check_win()

    def reset_game():
        """Reset the game to the initial state."""
        nonlocal game_over
        game_over = False
        # Reset the board and moves
        for i in range(9):
            board[i] = " "
            buttons[i].config(text=" ", state='normal')  # Reset button state
        player_moves.clear()
        computer_moves.clear()
        update_board()

    # 다시하기 버튼 생성
    reset_button = tk.Button(game_window, text="다시하기", command=reset_game)
    reset_button.grid(row=3, columnspan=3)  # 버튼을 보드 아래에 배치

    update_board()  # 초기 보드 상태 업데이트

