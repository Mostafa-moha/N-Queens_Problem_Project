import tkinter as tk
from tkinter import ttk, messagebox
import time

from backtracking import n_queens_backtracking
from best_first_search import solve_n_queens_best_first
from hill_climbing import solve_n_queens_hill_climbing
from genetic_algorithm import solve_n_queens_genetic

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
        solution = n_queens_backtracking(n, display_solution, root)
    elif algorithm == "Best-First Search":
        solution = solve_n_queens_best_first(n, display_solution, root)
    elif algorithm == "Hill-Climbing":
        solution = solve_n_queens_hill_climbing(n, display_solution, root)
    elif algorithm == "Genetic Algorithm":
        solution = solve_n_queens_genetic(n, display_solution, root)
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
tk.Label(root, text="Enter board size (N):").grid(row=0, column=0, padx=10
, pady=10)
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
