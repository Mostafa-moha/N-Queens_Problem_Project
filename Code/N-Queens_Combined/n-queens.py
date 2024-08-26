import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
import heapq

def n_queens_backtracking(n):
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

def solve_n_queens_best_first(n):
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
                if new_heuristic < heuristic:  # Only push if new board is better
                    heapq.heappush(pq, (new_heuristic, new_board))

    return None

def solve_n_queens_hill_climbing(n):
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

        if best_conflicts == current_conflicts:  # If no better move is found, stop
            break
        board = best_board
        current_conflicts = best_conflicts

    return board if current_conflicts == 0 else None


def solve_n_queens_genetic(n, population_size=100, generations=1000):
    def create_population(size, n):
        return [random.sample(range(n), n) for _ in range(size)]

    def fitness(board):
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def selection(population):
        population.sort(key=fitness)
        return population[:len(population)//2]

    def crossover(parent1, parent2):
        point = random.randint(1, n - 2)
        child = parent1[:point] + [gene for gene in parent2 if gene not in parent1[:point]]
        return child

    def mutate(board):
        i, j = random.sample(range(n), 2)
        board[i], board[j] = board[j], board[i]

    population = create_population(population_size, n)
    for _ in range(generations):
        population = selection(population)
        next_generation = []
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)
            if random.random() < 0.1:
                mutate(child)
            next_generation.append(child)
        population = next_generation
        best_solution = min(population, key=fitness)
        
        display_solution(best_solution, n)
        time.sleep(0.3)
        root.update()
        
        if fitness(best_solution) == 0:
            return best_solution

    return None

# GUI Functions
def display_solution(solution, n):

    if isinstance(solution[0], list):  # Backtracking Solution (2D board)
        for row in range(n):
            for col in range(n):
                if solution[row][col] == 1:
                    board[row][col].config(text="Q", bg="lightblue")
                else:
                    board[row][col].config(text="", bg="white")
    else:  # Other Algorithms (1D board)
        for row in range(n):
            for col in range(n):
                if col == solution[row]:
                    board[row][col].config(text="Q", bg="lightblue")
                else:
                    board[row][col].config(text="", bg="white")

def solve():
    n = int(board_size_entry.get())
    if n < 4:
        messagebox.showerror("Error", "Invalid Number. The number must be 4 or more.")
        return
    algorithm = algorithm_choice.get()
    # Clear the current board
    for widget in board_frame.winfo_children():
        widget.destroy()
    # Create a new board with the specified size
    create_board(n)
    # Start timing
    start_time = time.time()
    
    if algorithm == "Backtracking":
        solution = n_queens_backtracking(n)
    elif algorithm == "Best-First Search":
        solution = solve_n_queens_best_first(n)
    elif algorithm == "Hill-Climbing":
        solution = solve_n_queens_hill_climbing(n)
    elif algorithm == "Genetic Algorithm":
        solution = solve_n_queens_genetic(n)
    else:
        messagebox.showerror("Error", "Invalid algorithm selected.")
        return
    
    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if solution:
        messagebox.showinfo("Solution Found", f"Solution found in {elapsed_time:.2f} seconds.")
    else:
        messagebox.showinfo("No Solution", f"No solution found for {n}-Queens problem. Time taken: {elapsed_time:.2f} seconds.")

def create_board(n):
    global board
    board = []
    for i in range(n):
        row = []
        for j in range(n):
            label = tk.Label(board_frame, text="", width=2, height=1, bg="white", font=("Arial", 24), relief="groove")
            label.grid(row=i, column=j)
            row.append(label)
        board.append(row)


def reset_board():
    for widget in board_frame.winfo_children():
        widget.destroy()
    create_board()

# GUI Setup
root = tk.Tk()
root.title("N-Queens Problem Solver")

# Input for Board Size
tk.Label(root, text="Enter board size (N):").grid(row=0, column=0, padx=10, pady=10)
board_size_entry = tk.Entry(root)
board_size_entry.grid(row=0, column=1, padx=10, pady=10)
board_size_entry.insert(0, "8")

# Algorithm Selection
tk.Label(root, text="Choose algorithm:").grid(row=1, column=0, padx=10, pady=10)
algorithm_choice = ttk.Combobox(root, values=["Backtracking", "Best-First Search", "Hill-Climbing", "Genetic Algorithm"])
algorithm_choice.grid(row=1, column=1, padx=10, pady=10)
algorithm_choice.current(0)

# Solve Button
solve_button = tk.Button(root, text="Solve", command=solve)
solve_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)



# Board Frame for displaying the chessboard
board_frame = tk.Frame(root)
board_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Reset Button
reset_button = tk.Button(root, text="Reset Board", command=reset_board)
reset_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Initialize board display
create_board(8)

# Start the GUI event loop
root.mainloop()
