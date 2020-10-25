from random import choices, sample, shuffle, random
from copy import deepcopy
from typing import List
from models.fixture import Fixture
from models.city import City
from models.team import Team
import statistics
import random
import math
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Genome = List[Team]
Population = List[Genome]


def find_team_of_size(genome: Genome, size) -> [int]:
    return [i for i, x in enumerate(genome) if x.size == size]

def who_played_against_big_teams(genome: Genome, fixture):
    big_teams_indexes = find_team_of_size(genome, 'Grande')
    very_big_teams_indexes = find_team_of_size(genome, 'Muy Grande')
    all_big_teams = very_big_teams_indexes + big_teams_indexes
    who_played = []
    for fixture_date in fixture:
      if fixture_date.local in all_big_teams:
        who_played.append([fixture_date.visitante, 'visitante', fixture_date.local in very_big_teams_indexes])
      elif fixture_date.visitante in all_big_teams:
        who_played.append([fixture_date.local, 'local', fixture_date.visitante in very_big_teams_indexes])

    return who_played

def consecutive_big_team_matches(genome: Genome, big_teams_matches) -> int:
    consecutive_count = 0
    for i in range(len(genome) - 2):
      for team_index in big_teams_matches[i * 5:i * 5 + 5]:
        if team_index[0] in [x[0] for x in big_teams_matches[i * 5 + 5:i * 5 + 10]]:
          consecutive_count += 1
    return consecutive_count


def required_matches_type_against_very_big_teams(genome: Genome, big_teams_matches) -> int:
    not_passing_count = 0
    team_names = [x.name for x in genome]
    for team in genome:
      try:
        team_index = team_names.index(team.name)
      except:
        team_index = -1
      matches = [x for x in big_teams_matches if x[2] and team_index == x[0]]
      if (len(matches) != 2 or matches[0][1] == matches[1][1]):
        not_passing_count += 1
    return not_passing_count

def required_matches_type_against_big_teams(genome: Genome, big_teams_matches) -> int:
    not_passing_count = 0
    team_names = [x.name for x in genome]
    for team in genome:
      try:
        team_index = team_names.index(team.name)
      except:
        team_index = -1
      matches = [x for x in big_teams_matches if x[2] == False and team_index == x[0]]
      if len(matches) != 3 or set([matches[0][1], matches[1][1], matches[2][1]]) != 2: #TODO parece que el set nunca va a funcionar
        not_passing_count += 1
    return not_passing_count


"""

fitness: it tells the fitness of a genome
params:
    genome: the given genome to calculate its fitness
    distances_avg: average of all distances between cities
    distances: matrix of distances between cities
    dates: dates to play a match
    fixture: template of a fixture, contains: date, localteam and visitor team
"""

def fitness(genome: Genome,distances_avg,distances,cities,dates,fixture: Fixture, show_kms = False) -> int:

    value = 0

    # Reinicio distancias de los equipos
    for team in genome:
        team.set_total_distance_traveled(0)

    #Desvio estandar en ida y vuelta por fecha
    for date in dates:
        for fixture_date in fixture:
            if date == fixture_date.date:
                local = genome[fixture_date.local - 1]
                visitante = genome[fixture_date.visitante - 1]
                for index, city_distance in enumerate(distances[visitante.city.name]):
                    if index == local.city.id:
                        visitante.set_total_distance_traveled(visitante.total_distance_traveled+city_distance*2)

    distances_travled_by_team = []
    for team in genome:
        distances_travled_by_team.append(team.total_distance_traveled)

    stdev = statistics.stdev(data=distances_travled_by_team, xbar=distances_avg)
    value = value + math.ceil(stdev)

    teams_names = []
    for team in genome:
        if team.name not in teams_names:
            teams_names.append(team.name)

    distinct_teams_length = len(teams_names)
    if distinct_teams_length != len(genome):
        value += 1000 * (len(genome) - distinct_teams_length)

    big_teams_matches = who_played_against_big_teams(genome, fixture)

    consecutive_matches = consecutive_big_team_matches(genome, big_teams_matches)

    value += 1000 * consecutive_matches

    value += 9999 * required_matches_type_against_very_big_teams(genome, big_teams_matches)

    value += 9999 * required_matches_type_against_big_teams(genome, big_teams_matches)


    if show_kms:
        print(show_kms)
        print(distances_travled_by_team)
        print(consecutive_matches)
        print(required_matches_type_against_very_big_teams(genome, big_teams_matches))
        print(required_matches_type_against_big_teams(genome, big_teams_matches))

    return value


"""
generate_genome: generates a genome with a given length
params:
    length: size of the genome.
    posible_genoms: list of posible genomes
    teams: list of the teams
"""
def generate_genome(length:int,posible_genomes: [int], teams:[Team]) -> Genome:

    new_team = deepcopy(teams)
    shuffle(x=new_team)
    teams_id = sample(posible_genomes,k=length)
    team_checker = {}
    for team in new_team:
        if team.id == 0:
            for new_id in teams_id:
                if team_checker.get(new_id) == None:
                    team.id = new_id
                    team_checker[new_id] = True
                    break
    return new_team
    # return sample(posible_genomes, k=length)
#

"""
generate_population: generates a population of genomes
params:
    population_size: size of the population
    genome_length: size of the each genome
    teams: list of the teams to generate the population
"""
def generate_population(population_size:int, genome_length:int,teams: [Team]) -> Population:
    return  [generate_genome(genome_length,[x+1 for x in range(len(teams))],teams) for _ in range(population_size)]


"""
selection_pair: selects a pair of the given population
params:
    population: the population to evaluate
"""
def selection_pair(population: Population,distances_avg,distances,cities,dates,fixture: Fixture) -> Population:
    fitness_result = [-fitness(gene,distances_avg,distances,cities,dates,fixture) for gene in population]

    pair = random.choices(
        population=population,
        weights=fitness_result,
        k=2
    )

    return pair

"""
crossover: cross two elements of the population
params:
    a: element 1
    b: element 2
"""
def crossover(a: Genome, b:Genome) -> Genome:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")
    length = len(a)
    if length < 2:
        return a, b

    p = (random.randint(1, length)) - 1
    return a[0:p] + b[p:], b[0:p] + a[p:]

def binomial_crossover(a: Genome, b:Genome) -> Genome:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")
    length = len(a)
    if length < 2:
        return a, b

    child_1 = []
    child_2 = []
    for i in range(length):
        random_number = random.uniform(0, 1)

        if random_number <= 0.5:
            child_1.append(a[i])
            child_2.append(b[i])
        else:
            child_1.append(b[i])
            child_2.append(a[i])

    return child_1, child_2

"""
mutation: mutates a genome according to the given probability
params:
    genome: genome to mutate
    probability: probability to mutate
    teams: all possible elements
"""
def mutation(genome: Genome, teams: Team, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = random.randrange(len(genome))
        genome[index] = genome[index] if random.random() > probability else random.choice(teams)
    return genome

"""
calculate_distances_average: calculates the average of distances between cities
params:
    - distances: it is the distance between one city and another
    - cities: cities that participates in the tournament
"""
def calculate_distances_average(cities,distances):
    distance_avg = 0
    """
    Since we have a symetric and square matrix of distances
    First: we sumarize every column
    Second: we divide by the total number of rows - 1
    Third: we divide again by the total number of rows - 1
    """

    for city in cities:
        for aux in distances[city.name]:
            distance_avg = distance_avg + aux
    distance_avg = distance_avg/(len(distances)-1)*2
    return distance_avg

"""
run_evolution: executes de genetic algorithm
params:
    - fixture: it is the template of the fixutre
    - distances: it is the distance between one city and another
    - cities: cities that participates in the tournament
    - dates: every date to play a match
    - population: population to evaluate in the evolution
"""

def selection_population_function(population: [Genome],distances_avg,distances,cities,dates,fixture):
    # TORNEO
    random_list = random.sample(range(0, len(population)), len(population))
    selected_population = []
    population_length = len(population)
    for i in range(int(len(population)/2)):

        fitness_1 = fitness(population[random_list[i]], distances_avg, distances, cities, dates, fixture)
        fitness_2 = fitness(population[random_list[population_length - i - 1]], distances_avg, distances, cities, dates, fixture)
        if fitness_1 <= fitness_2:
            selected_population.append(population[random_list[i]])
        else:
            selected_population.append(population[random_list[population_length - i - 1]])

    return selected_population

    # RULETA: Esta implementado tal cual lo vimos en los videos, lo unico distinto es que la ruleta esta ordenada y la seleccion es invertida al momento de usar la ruleta, esto lo hago
    # porque en nuestro caso el mejor valor es el que tiene la aptitud mas chica, no la mas grande.
    # selected_population = []
    # sorted_population = sorted(population, key=lambda genome: fitness(genome,distances_avg,distances,cities,dates,fixture))
    # fitness_list = []
    # for i in range(len(sorted_population)):
    #     fitness_list.append(fitness(sorted_population[i], distances_avg, distances, cities, dates, fixture, False))
    #
    # total_fitness = sum(fitness_list)
    # prob_list = []
    # for i in range(len(fitness_list)):
    #     prob_list.append(fitness_list[i]/total_fitness)
    #
    # cumulative_prob_list = []
    # for i in range(len(fitness_list)):
    #     if i == 0:
    #         cumulative_prob_list.append(prob_list[i])
    #     else:
    #         cumulative_prob_list.append(cumulative_prob_list[i-1] + prob_list[i])
    #
    # population_size = len(population)
    #
    # for j in range(len(population)):
    #     random_number = random.uniform(0, 1)
    #     for i in range(len(cumulative_prob_list)):
    #         if i == 0 and random_number <= cumulative_prob_list[i]:
    #             selected = (population_size -1) - i
    #             selected_population.append(sorted_population[selected])
    #         elif (random_number <= cumulative_prob_list[i]) and (random_number > cumulative_prob_list[i-1]):
    #             selected = (population_size -1) - i
    #             selected_population.append(sorted_population[selected])
    #
    # return selected_population


    # RANKING

    # sorted_population = sorted(population, key=lambda genome: fitness(genome, distances_avg, distances, cities, dates, fixture))
    #
    # selected_population = []
    #
    # for i in range(3):
    #     selected_population.append(sorted_population[0])
    # for i in range(2):
    #     selected_population.append(sorted_population[1])
    # selected_population.append(sorted_population[2])
    # selected_population += selected_population
    # random.shuffle(selected_population)
    #
    # return selected_population

def crossover_population_function(population: [Genome]):

    cross_population = []
    population_length = len(population)
    for i in range(int(len(population) / 2)):

        offspring_a, offspring_b = binomial_crossover(population[i], population[population_length-i-1])

        cross_population.append(offspring_a)
        cross_population.append(offspring_b)

    for i in range(int(len(population) / 2)):
        offspring_a, offspring_b = binomial_crossover(population[i], population[len(population) - 1 - i])

        cross_population.append(offspring_a)
        cross_population.append(offspring_b)

    return cross_population


def muatation_deviation_based(population: [Genome], teams:[Team],distances_avg,distances,cities,dates,fixture):
    fitness_values = []
    for genome in population:
        value = fitness(genome,distances_avg,distances,cities,dates,fixture)
        fitness_values.append(value)
    std = statistics.stdev(fitness_values)
    if std < 10:
        random_number_genome = random.randint(0, len(population)-1)
        random_number_team = random.randint(0, len(population[0])-1)
        team = random.choice(teams)
        mutated_population = population
        # print("mute",random_number_genome,random_number_team, mutated_population[random_number_genome][random_number_team], "por:",team)
        mutated_population[random_number_genome][random_number_team] = team
    else:
        return population
    return mutated_population

def mutation_population_function(population: [Genome], teams: Team, num: int = 1, probability: float = 0.7):
    random_number_genome = random.randint(0, len(population)-1)
    random_number_team = random.randint(0, len(population[0])-1)
    mutated_population = population

    team = random.choice(teams)

    mutated_population[random_number_genome][random_number_team] = team


    return mutated_population




def run_evolution(fixture, distances, cities, dates,population, generation_limit, teams, population_size):


    distances_avg = calculate_distances_average(cities, distances)
    best_value = 0
    for i in range(generation_limit):

        # SELECCION
        selected_population = selection_population_function(population,distances_avg,distances,cities,dates,fixture)
        # CRUZAMIENTO
        cross_population = crossover_population_function(selected_population)

        # # MUTACION SIMPLE
        # probability_mutation = 0.5

        # MUTACION ADAPTATIVA POR CONVERGENCIA
        genomes_fitness = []
        for genome in cross_population:
            genome_fitness = fitness(genome, distances_avg, distances, cities, dates, fixture)
            if genome_fitness not in genomes_fitness:
                genomes_fitness.append(genome_fitness)

        probability_mutation = 1 - (len(genomes_fitness) / len(cross_population))

        random_number = random.uniform(0, 1)
        if random_number <= probability_mutation:
            mutated_population = mutation_population_function(cross_population, teams)
        else:
            mutated_population = cross_population

        # mutated_population = muatation_deviation_based(cross_population, teams,distances_avg,distances,cities,dates,fixture)

        population = mutated_population

        # print("Iteracion: " + str(i))

        # if i % 1000 == 0:
        #     print("Iteracion: " + str(i) + ", Promedio: %f" % (population_fitness(population, fitness_func) / len(population)))
        #
        #     # print("Iteracion: " + str(i))
        population_print = deepcopy(population)
        lala = sorted(population_print, key=lambda genome: fitness(genome,distances_avg,distances,cities,dates,fixture))
        lele = []
        for k in range(len(population)):
            lele.append(fitness(lala[k],distances_avg,distances,cities,dates,fixture, False))
        print(lele)
        if best_value != str(fitness(lala[0],distances_avg,distances,cities,dates,fixture)):
            best_value = str(fitness(lala[0],distances_avg,distances,cities,dates,fixture))
            print("Iteracion: " + str(i))

            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Mejor gen: " + (str(fitness(lala[0],distances_avg,distances,cities,dates,fixture, False))),[x.name for x in lala[0]])

    print(population[0])
    print(sorted(population[0], key=lambda x: x.name))
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Mejor gen: " + str(
    fitness(lala[0], distances_avg, distances, cities, dates, fixture, True)))
    teams_names = []
    for team in population[0]:
        if team.name not in teams_names:
            teams_names.append(team.name)
    print(len(teams_names))



def run_evolution_with_graph(fixture,distances,cities, dates,population, generation_limit, teams, population_size):
    distances_avg = calculate_distances_average(cities, distances)
    fig = plt.figure()
    fig.suptitle('Poblacion:'+str(population_size)+'\n'+'Generaciones:'+str(generation_limit))
    x,y = [],[]
    plt.grid()
    ani = animation.FuncAnimation(fig,animate,fargs=(x,y,),interval=1000)

    best_value = 0
    for i in range(generation_limit):
        #SELECCION
        selected_population = selection_population_function(population,distances_avg,distances,cities,dates,fixture)
        # CRUZAMIENTO
        cross_population = crossover_population_function(selected_population)
        # # MUTACION
        random_number = random.uniform(0, 1)
        if random_number <= 0.7:
            mutated_population = mutation_population_function(cross_population, teams)
        else:
            mutated_population = cross_population
        population = mutated_population
        sorted_population = sorted(population, key=lambda genome: fitness(genome,distances_avg,distances,cities,dates,fixture))
        if best_value != str(fitness(sorted_population[0],distances_avg,distances,cities,dates,fixture)):
            x.append(i)
            y.append(fitness(sorted_population[0],distances_avg,distances,cities,dates,fixture))
    print(population[0])
    print(sorted(population[0], key=lambda x: x.name))
    teams_names = []
    for team in population[0]:
        if team.name not in teams_names:
            teams_names.append(team.name)
    print(len(teams_names))

    plt.show()


def animate(i,x,y):
    plt.cla()
    plt.grid()
    plt.xlabel('Vuelta')
    plt.ylabel('Aptitud')
    plt.plot(x,y)
