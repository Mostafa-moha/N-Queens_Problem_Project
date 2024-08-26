def n_queens_backtracking(n, display_solution, root):
    import time
    board = [[0] * n for _ in range(n)]
    
    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True
    
    def solve_recursive(board, col):
        if col >= n:
            return True
        for i in range(n):
            if is_safe(board, i, col):
                board[i][col] = 1
                display_solution(board, n)
                time.sleep(0.3)
                root.update()
                
                if solve_recursive(board, col + 1):
                    return True
                
                board[i][col] = 0
                display_solution(board, n)
                time.sleep(0.3)
                root.update()
        return False
    
    if solve_recursive(board, 0):
        return board
    return None
