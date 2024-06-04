import time
import random
import fitness
import sys

def create_visualization_table(queens_row):
    for j in range(len(queens_row)):
        for i in range(len(queens_row)):
            queen_pos = queens_row[i]
            if queen_pos == j:
                print("Q ", end="")
            else:
                print("_ ", end="")
        print("")

def gather_user_input():
    pop_size = input("Establish the population size of each generation: ")
    pop_size = int(pop_size)
    num_queens = input("Establish the N x N size board to place N amount of queens on: ")
    num_queens = int(num_queens)
    num_of_iterations = input("How many generations should the algorithm birth?: ")
    num_of_iterations = int(num_of_iterations)
    return pop_size, num_queens, num_of_iterations

def gather_user_input2():
    symbol = input("type S to go again or E to exit: ")
    if symbol == "S":
        run_again = True
    else:
        run_again = False
    return run_again

    return pop_size, num_queens, num_of_iterations


def generate_initial_population(numberofqueens, pop):
    population_size = pop
    population = []
    for i in range(population_size):
        board_instance = {}
        board_instance['queens_row'] = [random.randint(1, numberofqueens) for j in range(numberofqueens)]
        board_instance['conflicts'] = fitness.detect_conflicts(board_instance['queens_row'])
        board_instance['fitness'] = fitness.fitness_function(board_instance['queens_row'])
        population.append(board_instance)
        #print(i, "CONFLICT COUNT", fitness.detect_conflicts(board_instance['queens_row']))
        #print(i, "FITNESS PERCENT", fitness.fitness_function(board_instance['queens_row']), "%")
    return population

def random_selection(population):
    fitness_values = [individual["fitness"] for individual in population]
    selected_parents = random.choices(population, weights=fitness_values, k=2)
    parent1 = selected_parents[0]
    parent2 = selected_parents[1]
    return parent1, parent2


def cross_parent(parents):
    # Choose a crossover point randomly

    parent1, parent2 = parents

    crossover_point = random.randint(0, len(parent1) - 1)

    parent1 = parent1["queens_row"]
    parent2 = parent2["queens_row"]
    #print("these parents", parent1, parent2)
    #time.sleep(.1)
    # Perform crossover
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    #print("made these children: ",child1, child2)
    #time.sleep(.1)
    return child1, child2

def mutate_children(children):
    child1 = children[0]
    child2 = children[1]

    mutate_point = random.randint(0, len(child1) - 1)
    mutate_value = random.randint(0, len(child1) - 1)

    child1.insert(mutate_point, mutate_value)
    child1.pop(mutate_point+1)

    mutate_point = random.randint(0, len(child1) - 1)
    mutate_value = random.randint(0, len(child1) - 1)

    child2.insert(mutate_point, mutate_value)
    child2.pop(mutate_point + 1)
    #print("here is one value mutated: ", child1, child2)
    return child1, child2


def mutate_population(population, numberofqueens, generation, current_best_generation, pop, best_board, best_fitness_total):
    population_size = pop
    mutated_population = []
    is_chad = False

    # Initialize best_board outside of the loop
    # and set it to the input parameter

    for i in range(population_size):
        board_instance = {}
        parent1, parent2 = random_selection(population)
        children = cross_parent((parent1, parent2))
        mutated_children = mutate_children(children)
        random_child = random.randint(0, 1)
        print(random_child)

        board_instance['queens_row'] = mutated_children[random_child]
        board_instance['conflicts'] = fitness.detect_conflicts(children[random_child])
        board_instance['fitness'] = fitness.fitness_function(children[random_child])

        if best_fitness_total < board_instance['fitness']:
            best_fitness_total = board_instance['fitness']
            best_board = board_instance
            current_best_generation = generation
        mutated_population.append(board_instance)

    #print(mutated_population)
    return mutated_population, best_board, best_fitness_total, current_best_generation


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    running = True
    while running == True:
        exit = False
        pop, queens, iterations = gather_user_input()
        runtime_timer_start = time.time()
        initial_population = generate_initial_population(queens, pop)
        species_extiniction = 0
        best_fitness_total = 0
        best_board = 0
        current_best_generation = 0
        #print(initial_population)
        while species_extiniction < iterations and exit == False:
            initial_population, best_board, best_fitness_total, current_best_generation = (mutate_population(initial_population, queens, species_extiniction, current_best_generation, pop, best_board, best_fitness_total))
            #print(best_board, best_fitness_total)
            if best_fitness_total == 1.0:
                #print("EXITING BY BEST TOTAL",  1.0)
                exit = True
            #print(initial_population)
            species_extiniction = species_extiniction + 1
        print("This is the best current board:", best_board, "He was created in generation: ", current_best_generation-1)
        create_visualization_table(best_board["queens_row"])
        runtime_timer_end = time.time()
        runtime_total = runtime_timer_end - runtime_timer_start
        print("Here was the total runtime of this genetic algo: ", runtime_total)
        running = gather_user_input2()



