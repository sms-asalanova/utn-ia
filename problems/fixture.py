from algorithms.genetic import Genome
from collections import namedtuple
import numpy
import math
import statistics

Fixture = namedtuple('Thing', ['name', 'value', 'weight'])

Team = namedtuple('Team', ['name', 'size', 'city'])
City = namedtuple('City', ['name', 'location']) #TODO: Definir que es "location",  coordenadas, ubicacion en la matriz de distancia?


# Primer fixture mas chico, 4 equipos
first_example = [
    Team('Boca', 'Grande', City('Buenos Aires', '')),
    Team('River', 'Grande', City('Buenos Aires', '')),
    Team('Racing', 'Grande', City('Buenos Aires', '')),
    Team('Talleres', 'Normal', City('Buenos Aires', '')),
]

# TODO: Matriz de distancias.

def fitness(genome: Genome, teams: [Team]) -> int:
    # if len(genome) != len(teams):
    #     raise ValueError("genome and teams must be of same length")

    value = 0
    teams_km = []

    # 1 Calcular por cada equipo sus km
    #   Separar genome en fechas
    #   Separar fechas en partidos
    #   Por cada partido que el equipo es visitante(segundo equipo del partido, hacer la sumatoria de kms recorridos)

    days = []

    # Obtengo la cantidad de bits que representan a un equipo en el genome.
    team_binary_length = math.log2(len(teams))
    match_binary_length = team_binary_length * 2
    day_binary_length = (len(teams) - 1) * team_binary_length

    matchNumber = len(teams) / 2
    dayNumber = len(teams) - 1

    #   Separar genome en fechas y las fechas en partidos.
    days = numpy.array_split(numpy.array(genome), dayNumber)


    for i,day in enumerate(days):
        days[i] = numpy.array_split(numpy.array(days[i]), matchNumber)

    for team in teams:
        for day in days:
            for match in day:
                indexA = int(team_binary_length)
                indexB = int((team_binary_length * 2))

                localTeam = ''.join(str(e) for e in list(match[0: indexA]))
                visitingTeam = ''.join(str(e) for e in list(match[indexA: indexB]))

                if visitingTeam == team.name: #El equipo deberia tener un campo que lo relacione con el binario
                    teams_km.append(getDistanceTraveled(localTeam, visitingTeam)) #Funcion que obtiene la distancia de la matriz de distancias

    # 2 Calcular la desviacion estandar
    value = statistics.stdev(teams_km)

    return value

fitness([1,0,1,1,0,1,0,0,1,1,0,1,0,0,1,0,1,1,0,1,0,1,0,0], first_example)


# def getDistanceTraveled(localTeam, visitingTeam) -> int:
# # TODO

# Funciones para imprimir por pantalla los resultados de la ejecucion del algoritmo.

# def from_genome(genome: Genome, things: [Thing]) -> [Thing]:
#     result = []
#     for i, thing in enumerate(things):
#         if genome[i] == 1:
#             result += [thing] #Concatena los objetos como listas.
#
#     return result
#
# def to_string(things: [Thing]):
#     return f"[{', '.join([t.name for t in things])}]"
#
#
# def value(things: [Thing]):
#     return sum([t.value for t in things])
#
#
# def weight(things: [Thing]):
#     return sum([p.weight for p in things])
#
#
# def print_stats(things: [Thing]):
#     print(f"Things: {to_string(things)}")
#     print(f"Value {value(things)}")
#     print(f"Weight: {weight(things)}")