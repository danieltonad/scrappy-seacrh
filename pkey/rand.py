from itertools import permutations, islice
import random, math

def fitness_function(n):
    """
    Example fitness function: Higher fitness for numbers divisible by 1000.
    """
    return 1 if n % 1000 == 0 else 0

def mutate(n):
    """
    Example mutation: Add a random number between -100 and 100.
    """
    return n + random.randint(-100, 100)

def crossover(a, b):
    """
    Example crossover: Take the average of two numbers.
    """
    return (a + b) // 2

def genetic_algorithm(population_size, generations, min: int, max: int):
    """
    Simple genetic algorithm to evolve numbers.
    """
    population = [random.randint(min, max) for _ in range(population_size)]
    for _ in range(generations):
        population = sorted(population, key=fitness_function, reverse=True)
        next_generation = population[:2]  # Keep top 2
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population[:10], 2)  # Select from top 10
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_generation.append(child)
        population = next_generation
    return population



def generate_combinations_chunked(number_str):
    for perm in permutations(number_str):
        yield ''.join(perm)

def generate_combinations_custom(number_str):
    digits = list(number_str)
    n = len(digits)
    
    def scramble(arr):
        """Scrambles the array by swapping elements in a semi-random way."""
        for i in range(n):
            # Randomly choose a position to swap with
            j = random.randint(0, n - 1)
            # Swap elements at positions i and j
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    # Yield the original combination
    yield ''.join(digits)
    
    # Keep scrambling to generate new combinations
    while True:
        scrambled_digits = scramble(digits.copy())
        yield ''.join(scrambled_digits)

def factorial_sequence(start):
    start = int(start)
    # n = 0
    # while math.factorial(n) < start:
    #     n += 1

    # Yield factorials in descending order
    # for i in range(n, -1, -1):
    #     yield math.factorial(i)
    
    while True:
        div = start // 2
        if div < 100000000000000000000000:
            break
        start = div
        yield div
            

# Example usage
# start_number = 2**256
# for factorial in factorial_sequence(start_number):
#     print(factorial)