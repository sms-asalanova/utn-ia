from random import choices,sample,shuffle
from copy import deepcopy
from typing import List
from models.fixture import Fixture 
from models.city import City
from models.team import Team
import statistics

Genome = List[Team]
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
    for date in dates:
        for fixture_date in fixture:
            if date == fixture_date.date:
                for team in genome:
                    if team.id == fixture_date.local:
                        local = team
                    if team.id == fixture_date.visitante:
                        visitante = team
                for index, city_distance in enumerate(distances[visitante.city.name]):
                    if index == local.city.id:
                        visitante.set_total_distance_traveled(visitante.total_distance_traveled+city_distance*2)
    
    distances_travled_by_team = []
    for team in genome:
        distances_travled_by_team.append(team.total_distance_traveled)
    # stdev = statistics.stdev(data=[10000,10213,12320],xbar=distances_avg)
    stdev = statistics.stdev(data=distances_travled_by_team,xbar=distances_avg)
    value = value + stdev
                        
    #TODO #Agregar penalidad por efrentar a Boca o River de manera consecutiva
    for team in genome:
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
selection: selects a subset of the given population
params: 
    population: the population to evaluate
    genome_length: size of the each genom
"""
# def selection(population=Population) -> Population:
#     return choices(
#         # population=population,
#         # weights=
#     )

# def crossover(a: Genome, b:Genome) -> Genome:



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
def run_evolution(fixture, distances, cities, dates,population):
    distances_avg = calculate_distances_average(cities, distances)
    for genome in population:
        value = fitness(genome,distances_avg,distances,cities,dates,fixture)
        print(value)