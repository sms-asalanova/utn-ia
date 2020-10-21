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

Genome = List[Team]
Population = List[Genome]


def find_big_teams(genome: Genome) -> [int]:
    try:
      names = [x.name for x in genome]
      return [names.index('River Plate'), names.index('Boca Juniors')]
    except ValueError:
      return [-1, -1]

def who_played_against_big_teams(genome: Genome, fixture) -> [int]:
    big_teams_indexes = find_big_teams(genome)
    who_played = []
    for fixture_date in fixture:
      if fixture_date.local in big_teams_indexes:
        who_played.append(fixture_date.visitante)
      elif fixture_date.visitante in big_teams_indexes:
        who_played.append(fixture_date.local)

    return who_played

def consecutive_big_team_matches(genome: Genome, fixture) -> int:
    who_played = who_played_against_big_teams(genome, fixture)
    consecutive_count = 0
    for i in range(len(genome) - 3):
      for team_index in who_played[i * 2:i * 2 + 2]:
        if team_index in who_played[i * 2 + 2:i * 2 + 4]:
          consecutive_count += 1
    return consecutive_count

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
    # stdev = statistics.stdev(data=[10000,10213,12320],xbar=distances_avg)
    stdev = statistics.stdev(data=distances_travled_by_team)
    value = value + stdev

    distinct_teams_length = len(set(genome))
    if distinct_teams_length != len(genome):
      value += 9999 * len(genome) - distinct_teams_length

    consecutive_matches = consecutive_big_team_matches(genome, fixture)
    value += 1000 * consecutive_matches

    for team in genome: # esto hay que sacarlo por lo que hice arriba?
        if team.last_match in ["Boca Juniors", "River Plate"]:
            value = value - 1
    #TODO #Si juega vs Boca o River o Visitante
    #TODO #Si juega de visitante vs Racing,Independiente o San Lorenzo

    if show_kms:
        print(show_kms)
        print(distances_travled_by_team)

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
def run_evolution(fixture, distances, cities, dates,population, generation_limit, teams, population_size):
    distances_avg = calculate_distances_average(cities, distances)

    best_value = 0
    for i in range(generation_limit):
        # Ordena poblacion segun su aptitud para tener los mejores en los primeros indices.
        population = sorted(population, key=lambda genome: fitness(genome,distances_avg,distances,cities,dates,fixture))

        # Si alcanza el limite de aptitud, termina la evolucion.
        # if fitness_func(population[0]) <= fitness_limit:
        #     break

        # Tomo los 2 mejores de la poblacion para que esten en la siguiente iteracion.
        best_quarter_size = int(round((population_size/4) / 2.0)) * 2
        next_generation = population[0:best_quarter_size]

        # -1 porque al tomar los 2 primeros ya me ahorro una iteracion.
        for j in range(int(len(population) / 2) - int((best_quarter_size / 2)) ):
            parents = selection_pair(population, distances_avg,distances,cities,dates,fixture)
            offspring_a, offspring_b = crossover(parents[0], parents[1])

            offspring_a = mutation(offspring_a, teams)
            offspring_b = mutation(offspring_b, teams)
            next_generation += [offspring_a, offspring_b]

        population = next_generation


        # if i % 1000 == 0:
        #     print("Iteracion: " + str(i) + ", Promedio: %f" % (population_fitness(population, fitness_func) / len(population)))
        #
        #     # print("Iteracion: " + str(i))

        if best_value != str(fitness(population[0],distances_avg,distances,cities,dates,fixture)):
            best_value = str(fitness(population[0],distances_avg,distances,cities,dates,fixture))
            print("Iteracion: " + str(i))
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Mejor gen: " + str(fitness(population[0],distances_avg,distances,cities,dates,fixture, False)))

    # print(population[0])
    #print(sorted(population[0], key=lambda x: x.name))
    # for genome in population:
    #     value = fitness(genome,distances_avg,distances,cities,dates,fixture)
    #     print(value)