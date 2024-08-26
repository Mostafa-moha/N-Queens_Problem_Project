import random

def solve_n_queens_hill_climbing(n, display_solution, root):
    import time

    def get_conflicts(board):
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    board = list(range(n))
    random.shuffle(board)
    current_conflicts = get_conflicts(board)

    while True:
        display_solution(board, n)
        time.sleep(0.3)
        root.update()

        best_board = board[:]
        best_conflicts = current_conflicts
        for i in range(n):
            for j in range(i + 1, n):
                new_board = board[:]
                new_board[i], new_board[j] = new_board[j], new_board[i]
                new_conflicts = get_conflicts(new_board)
                if new_conflicts < best_conflicts:
                    best_conflicts = new_conflicts
                    best_board = new_board

        if best_conflicts == current_conflicts:
            break
        board = best_board
        current_conflicts = best_conflicts

    return board if current_conflicts == 0 else None
