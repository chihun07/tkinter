import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random

def start_game():
    class Minesweeper:
        def __init__(self, root, rows=10, cols=10, mines=10):
            self.root = root
            self.root.title("Minesweeper")
            
            self.rows = rows
            self.cols = cols
            self.mines = mines
            self.buttons = {}
            self.mine_positions = set()
            self.game_over = False

            self.setup_board()

        def setup_board(self):
            self.mine_positions = set(random.sample(range(self.rows * self.cols), self.mines))
            for i in range(self.rows):
                for j in range(self.cols):
                    button = Button(self.root, text="", width=6, height=2, bg="#BFFD9F")
                    button.grid(row=i+1, column=j, padx=5, pady=5)
                    button.bind("<Button-1>", lambda e, r=i, c=j: self.left_click(r, c))
                    button.bind("<Button-3>", lambda e, r=i, c=j: self.right_click(r, c))
                    self.buttons[(i, j)] = button

            # 다시하기 버튼 추가
            reset_button = Button(self.root, text="다시하기", command=self.reset_game, font=("Arial", 16))
            reset_button.grid(row=0, column=0, columnspan=self.cols // 2, pady=5)  # 왼쪽에 위치

            # 레벨 선택 버튼 추가
            level_frame = Frame(self.root)
            level_frame.grid(row=0, column=self.cols // 2, columnspan=self.cols // 2, pady=5)  # 오른쪽에 위치
            Button(level_frame, text="쉬움", font=("Arial", 16), command=lambda: self.start_game(9, 9, 10)).pack(side=LEFT, padx=5)
            Button(level_frame, text="보통", font=("Arial", 16), command=lambda: self.start_game(12, 12, 20)).pack(side=LEFT, padx=5)
            Button(level_frame, text="어려움", font=("Arial", 16), command=lambda: self.start_game(15, 15, 30)).pack(side=LEFT, padx=5)

        def start_game(self, rows, cols, mines):
            for widget in self.root.winfo_children():
                widget.destroy()  # 레벨 선택 창 닫기

            # 새로운 Minesweeper 인스턴스 생성
            new_game = Minesweeper(self.root, rows, cols, mines)
            
        def reset_game(self):
            # 게임 재설정
            self.game_over = False
            self.setup_board()

        def left_click(self, row, col):
            if self.game_over:
                return
            if (row * self.cols + col) in self.mine_positions:
                self.buttons[(row, col)].config(text="*", bg="red", state='disabled')  # 지뢰를 표시하고 버튼 비활성화
                self.game_over = True
                self.show_mines()  # 모든 지뢰 드러내기
            else:
                self.reveal_cell(row, col)  # 셀 드러내기 로직 구현

        def right_click(self, row, col):
            if self.game_over:
                return
            
            current_button = self.buttons[(row, col)]
            if current_button.cget("state") == 'disabled':
                return  # 버튼이 비활성화 상태일 경우 아무 작업도 수행하지 않음
            
            current_text = current_button.cget("text")
            
            if current_text == "F":
                # 플래그를 해제
                current_button.config(text="", bg="#BFFD9F")
            else:
                # 플래그 설정
                current_button.config(text="F", bg="yellow")

            self.check_win_condition()
            
        def reveal_cell(self, row, col):
            # 주변 지뢰 수를 계산합니다.
            mine_count = sum(
                (r * self.cols + c) in self.mine_positions
                for r in range(max(0, row-1), min(self.rows, row+2))
                for c in range(max(0, col-1), min(self.cols, col+2))
            )

            # 주변 지뢰 수가 0이면 버튼에 아무것도 표시하지 않고 비활성화합니다.
            if mine_count == 0:
                self.buttons[(row, col)].config(text='', state='disabled', bg="white")  # 아무것도 표시하지 않음
            else:
                self.buttons[(row, col)].config(text=str(mine_count), state='disabled', bg="white")  # 주변 지뢰 수 표시 및 비활성화

            # 주변 셀을 확인하여 지뢰가 없을 경우 재귀적으로 드러내기
            if mine_count == 0:
                for r in range(max(0, row-1), min(self.rows, row+2)):
                    for c in range(max(0, col-1), min(self.cols, col+2)):
                        if (r, c) != (row, col) and self.buttons[(r, c)].cget("state") != 'disabled':
                            self.reveal_cell(r, c)  # 재귀적으로 드러내기

            # 승리 조건 체크
            self.check_win_condition()

        def show_mines(self):
            for mine in self.mine_positions:
                row, col = divmod(mine, self.cols)
                self.buttons[(row, col)].config(text="*", bg="red", state='disabled')  # 지뢰 표시 및 버튼 비활성화

        def check_win_condition(self):
            flagged_mines = sum(
                1 for mine in self.mine_positions if self.buttons[divmod(mine, self.cols)].cget("text") == "F"
            )
            if flagged_mines == self.mines:
                messagebox.showinfo("우승", "모든 지뢰를 찾았습니다! 우승하셨습니다!")
                self.game_over = True

    game_window = tk.Toplevel()
    game_window.title("Minesweeper")
    game_instance = Minesweeper(game_window)
    game_window.mainloop()
