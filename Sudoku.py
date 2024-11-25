import tkinter as tk
import random

def start_game():
    # Sudoku 보드의 초기 상태를 저장할 배열
    origin_board = [[0 for j in range(9)] for i in range(9)]
    # 최종 퍼즐을 저장할 배열
    global board  # 전역 변수로 선언
    board = [[0 for j in range(9)] for i in range(9)]
    # 원래 비어있던 셀의 상태를 저장할 배열
    global Missing_board  # 전역 변수로 선언
    Missing_board = [[0 for j in range(9)] for i in range(9)]
    # 각 행, 열, 대각선에서 사용된 숫자를 추적하는 배열
    row = [[0 for j in range(10)] for i in range(10)]  # 가로축
    col = [[0 for j in range(10)] for i in range(10)]  # 세로축
    diag = [[0 for j in range(10)] for i in range(10)]  # 대각선

    global terminate_flag  # 전역 변수로 선언
    terminate_flag = False

    def board_init():
        seq_diag = [0, 4, 8]  # 각 서브 그리드의 대각선 인덱스
        for offset in range(0, 9, 3):  # 3x3 서브 그리드를 순회합니다
            seq = [i for i in range(1, 10)]  # 1부터 9까지의 숫자 리스트
            random.shuffle(seq)  # 숫자를 무작위로 섞습니다
            for idx in range(0, 9):  # 현재 서브 그리드의 9개의 셀을 순회합니다
                i, j = idx // 3, idx % 3  # 셀의 행과 열을 계산합니다
                row[offset + i][seq[idx]] = 1  # 행 배열 업데이트
                col[offset + j][seq[idx]] = 1  # 열 배열 업데이트
                k = seq_diag[offset // 3]  # 현재 서브 그리드의 대각선 인덱스
                diag[k][seq[idx]] = 1  # 대각선 배열 업데이트
                origin_board[offset + i][offset + j] = seq[idx]  # 보드에 숫자를 배치합니다

    def make_sudoku(k):
        global terminate_flag  # 전역 변수로 선언
        global board  # 전역 변수로 선언

        if terminate_flag:
            return True

        if k > 80:  # 모든 셀을 채운 경우
            for i in range(9):
                for j in range(9):
                    board[i][j] = origin_board[i][j]  # 최종 보드를 origin_board로 설정합니다
            terminate_flag = True
            return True

        i, j = k // 9, k % 9  # 현재 위치의 행과 열을 계산합니다
        start_num = random.randint(1, 9)  # 현재 셀에 넣을 숫자를 랜덤으로 선택합니다

        if origin_board[i][j] != 0:  # 현재 셀이 이미 채워져 있는 경우
            return make_sudoku(k + 1)

        for m in range(1, 10):  # 1부터 9까지의 숫자를 시도합니다
            m = 1 + (m + start_num) % 9  # 숫자를 순환하여 시도합니다
            d = (i // 3) * 3 + (j // 3)  # 현재 셀이 위치한 3x3 서브 그리드의 대각선 인덱스 계산
            if row[i][m] == 0 and col[j][m] == 0 and diag[d][m] == 0:  # 숫자가 유효한지 확인합니다
                row[i][m], col[j][m], diag[d][m] = 1, 1, 1  # 사용된 숫자로 표시합니다
                origin_board[i][j] = m  # 보드에 숫자를 배치합니다
                if make_sudoku(k + 1):  # 다음 셀을 채우기 위해 재귀 호출합니다
                    return True
                row[i][m], col[j][m], diag[d][m] = 0, 0, 0  # 백트래킹: 숫자를 지우고 다시 시도합니다
                origin_board[i][j] = 0

    def Cutnum():
        filled_cells = 81
        while filled_cells > 40:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if board[i][j] != " ":
                board[i][j] = " "
                Missing_board[i][j] = board[i][j]  # 원래 보드의 비어있던 상태를 저장
                filled_cells -= 1

    board_init()  # 보드 초기화
    make_sudoku(0)  # 퍼즐 생성
    Cutnum()  # 일부 숫자를 제거하여 퍼즐을 만듦

    def create_board():
        # Tkinter 윈도우 생성
        game_window = tk.Toplevel()
        game_window.title("Sudoku")

        def button_left_click(event, row, col):
            """ 좌클릭으로 숫자를 입력하는 함수 """
            if Missing_board[row][col] == " ":  # 원래 비어있던 셀일 때만 수정 가능
                select_num = tk.Toplevel()
                select_num.title("번호 선택")
                
                # 창을 마우스 위치에 맞춰 배치
                offset_x = 75  # 가로 크기의 절반
                offset_y = 75  # 세로 크기의 절반
                select_num.geometry(f"+{event.x_root - offset_x}+{event.y_root - offset_y}")
                
                # 숫자 선택을 반영하는 함수
                def select_number(number):
                    board[row][col] = number
                    buttons[row][col].config(text=number, fg='red')  # 선택된 숫자를 표시
                    select_num.destroy()  # 창 닫기

                # 1부터 9까지의 숫자 선택 버튼 생성
                for i in range(3):
                    for j in range(3):
                        number = i * 3 + j + 1
                        button = tk.Button(
                            select_num, 
                            text=str(number), 
                            width=3, 
                            height=1, 
                            font=("Arial", 16),
                            command=lambda n=number: select_number(n)  # 클릭 시 숫자 선택
                        )
                        button.grid(row=i, column=j, sticky='nsew')

        def button_right_click(event, row, col):
            """ 우클릭으로 숫자를 입력하는 함수 (예: 다른 색으로 표시) """
            if Missing_board[row][col] == " ":  # 원래 비어있던 셀일 때만 수정 가능
                selected_number = spinbox.get()  # Spinbox에서 선택한 숫자 가져오기
                board[row][col] = selected_number
                buttons[row][col].config(text=selected_number, fg='blue')  # 다른 색으로 표시

        def check_solution():
            """ 현재 보드가 정답인지 확인하는 함수 """
            for r in range(9):
                for c in range(9):
                    if board[r][c] != origin_board[r][c]:
                        return False
            return True

        def submit_answer():
            """ 제출 버튼 클릭 시 정답 확인 """
            if check_solution():
                checkup_text.set("정답입니다! 대단합니다!")
            else:
                checkup_text.set("틀렸습니다. 다시 시도하세요!")
        frame = tk.Frame(game_window)  # game_window로 변경
        frame.pack()

        buttons = [[None for _ in range(9)] for _ in range(9)]

        for r in range(9):
            for c in range(9):
                button_color = 'white'
                if (r // 3 + c // 3) % 2 == 0:
                    button_color = 'lightgrey'
                button = tk.Button(frame, text=board[r][c], width=5, height=3, bg=button_color, font=("Arial", 16))
                button.grid(row=r, column=c, sticky='nsew')
                
                # 좌클릭 및 우클릭 이벤트 바인딩
                button.bind("<Button-1>", lambda event, row=r, col=c: button_left_click(event, row, col))
                button.bind("<Button-3>", lambda event, row=r, col=c: button_right_click(event, row, col))
                
                buttons[r][c] = button

        # 모든 행과 열의 크기를 동일하게 설정
        for i in range(9):
            frame.grid_rowconfigure(i, weight=1)
            frame.grid_columnconfigure(i, weight=1)

        # Label을 위한 StringVar 생성
        checkup_text = tk.StringVar()
        checkup_text.set("")  # 초기 텍스트는 빈 문자열

        # 중앙 정렬을 위한 프레임 생성
        center_frame = tk.Frame(game_window)  # game_window로 변경
        center_frame.pack(expand=True)

        # 숫자 선택 Spinbox와 제출 버튼을 수평으로 배치할 프레임 생성
        control_frame = tk.Frame(center_frame)
        control_frame.pack(pady=20)

        spinbox = tk.Spinbox(control_frame, from_=1, to=9, width=10, font=("Helvetica", 20))
        spinbox.pack(side=tk.LEFT, padx=10)

        submit_button = tk.Button(control_frame, text="제출", command=submit_answer, font=("Helvetica", 16))
        submit_button.pack(side=tk.LEFT, padx=10)

        # Label 생성 및 변수 연결

        label1 = tk.Label(center_frame, text="↑ 키 킵력후 우클릭으로 메모 가능 ↑", font=("Helvetica", 10))
        label1.pack(anchor='w', padx=10, pady=0)  # 'w'는 왼쪽 정렬

        label = tk.Label(center_frame, textvariable=checkup_text, font=("Helvetica", 20))
        label.pack(pady=10)

        # Tkinter 루프 실행
        game_window.mainloop()  # game_window에서 루프를 실행

    for i in range(9):
        print(origin_board[i], end="")  # 각 행을 출력
        if (i + 1) % 3 == 0:  # 3번째 행마다 줄바꿈
            print()  # 줄바꿈
    # 보드 생성 함수 호출
    create_board()
