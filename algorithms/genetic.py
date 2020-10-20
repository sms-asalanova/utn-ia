from random import choices,sample,shuffle,random,randint
from copy import deepcopy
from typing import List
from models.fixture import Fixture 
from models.city import City
from models.team import Team
import math

from models.genome import Genome

import statistics

# Genome = List[Team]

Population = List[Genome]


"""
fitness: it tells the fitness of a genome
params:
    genome: the given genome to calculate its fitness
    distances_avg: average of all distances between cities
    distances: matrix of distances between cities
    dates: dates to play a match
    fixture: template of a fixture, contains: date, localteam and visitor team
"""

def fitness(genome: Genome,distances_avg,distances,cities,dates,fixture: Fixture) -> int:
    
    value = 0
    
   
    #Desvio estandar en ida y vuelta por fecha
    # print([(x.id,x.name) for x in genome.teams])
    
    for date in dates:
        for fixture_date in fixture:
            if date == fixture_date.date:
                for team in genome.teams:
                    # print('askjdhasjkhfbsajfsajfnsaofnsalfsalkf') if len(set(genome.teams)) != len(genome.teams)
                    if team.id == fixture_date.local:
                        local = team
                    if team.id == fixture_date.visitante:
                        visitante = team
                for index, city_distance in enumerate(distances[visitante.city.name]):
                    if index == local.city.id:
                        visitante.set_total_distance_traveled(visitante.total_distance_traveled+city_distance*2)
    
    distances_travled_by_team = []
    for team in genome.teams:
        distances_travled_by_team.append(team.total_distance_traveled)
    # stdev = statistics.stdev(data=[10000,10213,12320],xbar=distances_avg)
    stdev = statistics.stdev(data=distances_travled_by_team,xbar=distances_avg)
    value = value + stdev
                        
    #TODO #Agregar penalidad por efrentar a Boca o River de manera consecutiva
    for team in genome.teams:
        if team.last_match in ["Boca Juniors", "River Plate"]:
            value = value - 1 
    #TODO #Si juega vs Boca o River o Visitante
    #TODO #Si juega de visitante vs Racing,Independiente o San Lorenzo
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
    print(posible_genomes)
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
    population = []
    for _ in range(population_size):
        genome_teams = generate_genome(genome_length,[x+1 for x in range(len(teams))],teams)
        genome = Genome(teams=genome_teams,fitness_value=0)
        population.append(genome)
    return population
    # return  [generate_genome(genome_length,[x+1 for x in range(len(teams))],teams) for _ in range(population_size)]


"""
best_genome: selects the best genome
params: 
    a: genome a 
    b: genome b
"""
def best_genome(a:Genome, b:Genome) -> Genome:
    if a.fitness_value > b.fitness_value:
        return a
    else:
        return b

"""
selection: selects a subset of the given population
params: 
    population: the population to evaluate
    genome_length: size of the each genom
"""
def selection(population=Population) -> Population:
    new_population = []
    for index in range(math.ceil(len(population)/2) - 1):
        new_population.append(best_genome(a=population[index], b=population[len(population) - index - 1]))
    return new_population
        
"""
crossover: crossover 2 genomes
params: 
    a: the population to evaluate
    b: size of the each genom
"""
def crossover(a: Genome, b:Genome) -> Genome:
    if len(a.teams) != len(b.teams):
        raise ValueError("Genomes a and b must be of same length")
    team_length = len(a.teams)
    genome_teams = a.teams[0:(math.ceil(team_length/2))] + b.teams[math.ceil(team_length/2):team_length]
    return Genome(teams=genome_teams,fitness_value=0)


"""
mutation: crossover 2 genomes
params: 
    a: the population to evaluate
    b: size of the each genom
"""
def mutation(genome=Genome) -> Population:
    probability = random()
    random_index = randint(0, len(genome.teams) - 1)
    if probability > 0.5:
        genome.teams[random_index] = randint(0, len(genome.teams) - 1)
    # genome.teams[random_index] = randint(0, len(genome.teams) - 1) if probability > 0.5
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



def normalize_genome(genome=Genome, teams=[Team]):
    team_names = [x.name for x in genome.teams]
    distinct_teams = set(team_names)
    if len(distinct_teams) == len(genome.teams):
        return genome
    # for team in teams:
    #     if team.name not in distinct_teams:
    #         print(team.name)
    not_in_genome = [team for team in teams if team.name not in distinct_teams]
    print([(team.id,team.name) for team in not_in_genome])
    print([(team.id,team.name) for team in genome.teams])
    # print(len(distinct_teams),[name for name in distinct_teams])
    # teams_aux = []
    # for team_name in distinct_teams:
    #     for team in teams:
    #         if team_name == team.name:
    #             teams_aux.append(teams_aux)

    # genome_unique_teams = [x for x in genome.teams if x.name in distinct_teams]
    # print([team.name for team in genome_unique_teams ])
    # genome.teams = []
    # for index,team in enumerate(genome_unique_teams):
    #     if team.name in distinct_teams:
    #         teams[index] = index
    #         genome.teams.append(teams[index])
    # for index,team in enumerate(teams):
    #     if team.name not in distinct_teams:
    #         teams[index] = index + len(genome.teams) - 1
    #         genome.teams.append(teams[index])
    # # print([x.name for x in genome.teams])
    # print([x.name for x in genome.teams])

    # for team in genome.teams:



    return genome

"""
run_generation: executes de genetic algorithm 
params:
    - fixture: it is the template of the fixutre
    - distances: it is the distance between one city and another
    - cities: cities that participates in the tournament
    - dates: every date to play a match
    - population: population to evaluate in the evolution
"""
def run_generation(fixture, distances, cities, dates,population,teams) -> Population:
    # normalized_population = []
    # for genome in population:
    #     normalized_population.append(normalize_genome(genome, teams))
    distances_avg = calculate_distances_average(cities, distances)
    for genome in population:
        value = fitness(genome,distances_avg,distances,cities,dates,fixture)
        genome.set_fitness_value(value)
    # population.sort(key=lambda x:x.fitness_value, reverse=False)
    selected_population = selection(population=population)
    new_crossover_population = []
    for index in range(math.ceil(len(selected_population)/2) - 1):
       new_genome = crossover(a=selected_population[index],b=selected_population[len(selected_population)-1])
       new_crossover_population.append(new_genome)
    # return new_crossover_population
    mutated_population = []
    for genome in new_crossover_population:
        mutated_population.append(mutation(genome=genome))
    return mutated_population

