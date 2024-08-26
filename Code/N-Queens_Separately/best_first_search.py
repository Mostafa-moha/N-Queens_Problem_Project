import random
import heapq

def solve_n_queens_best_first(n, display_solution, root):
    import time

    def calculate_heuristic(board):
        conflicts = 0
        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    pq = []
    initial_board = list(range(n))
    random.shuffle(initial_board)
    heapq.heappush(pq, (calculate_heuristic(initial_board), initial_board))

    while pq:
        heuristic, board = heapq.heappop(pq)
        display_solution(board, n)
        time.sleep(0.3)
        root.update()

        if heuristic == 0:
            return board

        for i in range(n):
            for j in range(i + 1, n):
                new_board = board[:]
                new_board[i], new_board[j] = new_board[j], new_board[i]
                new_heuristic = calculate_heuristic(new_board)
                if new_heuristic < heuristic:
                    heapq.heappush(pq, (new_heuristic, new_board))

    return None
