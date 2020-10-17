from random import choices
from typing import List
from models.team import Team


Genome = List[Team]
Population = List[Genome]


"""

fitness: it tells the fitness of a genome
params:
    genome: the given genome to calculate its fitness
"""

def fitness(genome: Genome,distances) -> int:
    value = 0
    #Desvio estandar en ida y vuelta
    #Agregar penalidad por efrentar a Boca o River de manera consecutiva
    #Si juega vs Boca o River o Visitante
    for team in genome:
        if team.last_match in ["Boca Juniors", "River Plate"]:
            value = value - 1 
    #Si juega de visitante vs Racing,Independiente o San Lorenzo
   
    return value


"""
generate_genome: generates a genome with a given length
params: 
    length: size of the genome. 
"""
def generate_genome(length:int,teams) -> Genome:
    return choices(teams, k=length)


"""
generate_population: generates a population of genomes
params: 
    size: size of the population
    genome_length: size of the each genome
"""
def generate_population(size:int, genome_length:int,teams: [Team]) -> Population:
    return [generate_genome(genome_length,[team for team in teams]) for _ in range(size)]

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
