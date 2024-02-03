import random
import sys
import math

# Якщо функція y=f(x) має екстремум в точці x=x0, тоді в цій точці похідна функції або дорівнює нулю, або не існує.
#f(x) = x^3-5x+10
#f'(x) = 3x^2-5
def fitness_function(x):
    #return abs(3*(x**2)-5)
    #return abs(x**3 + 1)
    return math.sqrt(abs(x))
    #return abs(2 / x)
    #return abs(math.log2(abs(x)))
    #return abs(2*x-5)

# def crossover(parent1, parent2):
#     offspring = (parent1 + parent2) / 2.0
#     return offspring

def crossover(parent1, parent2, alpha=0.7):
    offspring = alpha * parent1 + (1 - alpha) * parent2
    return offspring

def mutate(child):
    mutation_value = random.uniform(-1, 1)
    child += mutation_value
    return child

#random.seed(42)

population_size = 1000
num_generations = 10
population = [random.uniform(-100, 100) for _ in range(population_size)]
for generation in range(num_generations):
    fitness_values = [fitness_function(individual) for individual in population]

    parent1 = population[fitness_values.index(min(fitness_values))]
    fitness_values.pop(fitness_values.index(min(fitness_values)))
    parent2 = population[fitness_values.index(min(fitness_values))]
    sys.stdout.write("\rGeneration " + str(generation) + "; Best values = " + str(parent1))

    offspring = crossover(parent1, parent2)
    offspring = mutate(offspring)

    index_least_fit = fitness_values.index(max(fitness_values))
    population[index_least_fit] = offspring
    sys.stdout.flush()
print()

best_solution = min(population, key=fitness_function)
print("Best solution:", best_solution)
