import TTK 
import Minesweeper
import Sudoku
import tkinter as tk

# 메인 창 설정
root = tk.Tk()
root.title("메인 창")

# 라벨 배치
label = tk.Label(root, text="게임 메뉴")
label.pack(pady=(10, 20))  # 상단 여백 추가

# 버튼 배치 - 가로로 나열하고 중앙 정렬
button_frame = tk.Frame(root)
button_frame.pack()

button1 = tk.Button(button_frame, text="틱텍톡", command=TTK.start_game)
button1.grid(row=0, column=0, padx=10, pady=10)

button2 = tk.Button(button_frame, text="수도쿠", command=Sudoku.start_game)
button2.grid(row=0, column=1, padx=10, pady=10)

button3 = tk.Button(button_frame, text="지뢰찾기", command=Minesweeper.start_game)
button3.grid(row=0, column=2, padx=10, pady=10)

root.mainloop()
