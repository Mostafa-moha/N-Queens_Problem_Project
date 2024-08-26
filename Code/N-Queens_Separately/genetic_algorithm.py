import random

def solve_n_queens_genetic(n, display_solution, root, population_size=100, generations=1000):
    import time

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
