from random import choices,sample,shuffle
from copy import deepcopy
from typing import List
from models.team import Team


Genome = List[Team]
Population = List[Genome]


"""

fitness: it tells the fitness of a genome
params:
    genome: the given genome to calculate its fitness
"""

def fitness(genome: Genome,distances,fixture) -> int:
    value = 0
    print(distances['Cities'])
    print(fixture)
    #Desvio estandar en ida y vuelta por fecha
    #Agregar penalidad por efrentar a Boca o River de manera consecutiva
    for team in genome:
        if team.last_match in ["Boca Juniors", "River Plate"]:
            value = value - 1 
    #Si juega vs Boca o River o Visitante
    #Si juega de visitante vs Racing,Independiente o San Lorenzo
    print(value)
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
