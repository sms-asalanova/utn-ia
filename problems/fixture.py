from algorithms.genetic import Genome
from collections import namedtuple
import numpy
import math
import statistics
from scipy.spatial.distance import squareform
import numpy as np

Fixture = namedtuple('Fixture', ['days'])
Day = namedtuple('Day', ['day_number', 'matches'])
Match = namedtuple('Match', ['local_team_number', 'visiting_team_number'])
Team = namedtuple('Team', ['name', 'size', 'binaryId', 'city'])
City = namedtuple('City', ['name', 'location']) #TODO: Definir que es "location",  coordenadas, ubicacion en la matriz de distancia?

# Primer fixture mas chico, 4 equipos
# fixture_1 = [
#     Day(1, [
#         Match(0, 1),
#         Match(2, 3)
#     ]),
#
#     Day(2, [
#         Match(1, 2),
#         Match(3, 0)
#     ]),
#
#     Day(3, [
#         Match(0, 2),
#         Match(1, 3)
#     ])
# ]
#
# teams = [
#     Team('Boca', 'Grande', '00', City('Buenos Aires', '')),
#     Team('River', 'Grande', '01', City('Buenos Aires', '')),
#     Team('Racing', 'Grande', '10', City('Buenos Aires', '')),
#     Team('Talleres', 'Normal', '11', City('Buenos Aires', '')),
# ]
#
# distance_matrix = [[0,11,41,25],
#                    [11,0,1,4],
#                    [41,1,0,30],
#                    [25,4,30,0]]

# 8 Equipos
fixture_1 = [
    Day(1, [
        Match(5, 2),
        Match(1, 6),
        Match(7, 4),
        Match(3, 0)

    ]),

    Day(2, [
        Match(6, 5),
        Match(4, 2),
        Match(0, 1),
        Match(3, 7)
    ]),

    Day(3, [
        Match(5, 4),
        Match(6, 0),
        Match(2, 3),
        Match(1, 7)
    ]),

    Day(4, [
        Match(0, 5),
        Match(3, 4),
        Match(7, 6),
        Match(1, 2)
    ]),

    Day(5, [
        Match(5, 3),
        Match(0, 7),
        Match(4, 1),
        Match(6, 2)
    ]),

    Day(6, [
        Match(7, 5),
        Match(1, 3),
        Match(2, 0),
        Match(6, 4)
    ]),

    Day(7, [
        Match(5, 1),
        Match(7, 2),
        Match(3, 6),
        Match(0, 4)
    ])
]

# 8 Equipos
teams = [
    Team('Boca', 'Grande', '000', City('Buenos Aires', '')),
    Team('River', 'Grande', '001', City('Buenos Aires', '')),
    Team('Racing', 'Grande', '010', City('Buenos Aires', '')),
    Team('Talleres', 'Normal', '011', City('Buenos Aires', '')),
    Team('Ferro', 'Normal', '100', City('Buenos Aires', '')),
    Team('San Lorenzo', 'Normal', '101', City('Buenos Aires', '')),
    Team('Huracan', 'Normal', '110', City('Buenos Aires', '')),
    Team('Velez', 'Normal', '111', City('Buenos Aires', '')),
]

distance_matrix = [ [0  ,5  ,115,300 ,25 ,855,10  ,30],
                    [5  ,0  ,250,11  ,5  ,1  ,15  ,11],
                    [115,250,0  ,41  ,600,58 ,81  ,41],
                    [300,11 ,41 ,0   ,30 ,25 ,2555,25],
                    [25 ,5  ,600,30  ,0  ,58 ,20  ,35],
                    [855,1  ,58 ,25  ,58 ,0  ,50  ,850],
                    [10 ,15 ,81 ,2555,20 ,50 ,0   ,59],
                    [30 ,11 ,41 ,25  ,35 ,850,59  ,0]]



# # 16 Equipos
# fixture_1 = [
#     Day(1, [
#         Match(12, 1),
#         Match(10, 0),
#         Match(13, 9),
#         Match(15, 8),
#         Match(2, 6),
#         Match(3, 7),
#         Match(11, 14),
#         Match(4, 5)
#
#     ]),
#
#     Day(2, [
#         Match(0, 12),
#         Match(9, 1),
#         Match(8, 10),
#         Match(6, 13),
#         Match(7, 15),
#         Match(14, 2),
#         Match(5, 3),
#         Match(4, 11)
#     ]),
#
#     Day(3, [
#         Match(12, 9),
#         Match(0, 8),
#         Match(1, 6),
#         Match(10, 7),
#         Match(13, 14),
#         Match(15, 5),
#         Match(2, 4),
#         Match(3, 11)
#     ]),
#
#     Day(4, [
#         Match(8, 12),
#         Match(6, 9),
#         Match(7, 0),
#         Match(14, 1),
#         Match(5, 10),
#         Match(4, 13),
#         Match(11, 15),
#         Match(3, 2)
#     ]),
#
#     Day(5, [
#         Match(12, 6),
#         Match(8, 7),
#         Match(9, 14),
#         Match(0, 5),
#         Match(1, 4),
#         Match(10, 11),
#         Match(13, 3),
#         Match(15, 2)
#     ]),
#
#     Day(6, [
#         Match(7, 12),
#         Match(14, 6),
#         Match(5, 8),
#         Match(4, 9),
#         Match(11, 0),
#         Match(3, 1),
#         Match(2, 10),
#         Match(15, 13)
#     ]),
#
#     Day(7, [
#         Match(12, 14),
#         Match(7, 5),
#         Match(6, 4),
#         Match(8, 11),
#         Match(9, 3),
#         Match(0, 2),
#         Match(1, 15),
#         Match(10, 13)
#     ]),
#
#     Day(8, [
#         Match(5, 12),
#         Match(4, 14),
#         Match(11, 7),
#         Match(3, 6),
#         Match(2, 8),
#         Match(15, 9),
#         Match(13, 0),
#         Match(10, 1)
#     ]),
#
#     Day(9, [
#         Match(12, 4),
#         Match(5, 11),
#         Match(14, 3),
#         Match(7, 2),
#         Match(6, 15),
#         Match(8, 13),
#         Match(9, 10),
#         Match(0, 1)
#     ]),
#
#     Day(10, [
#         Match(11, 12),
#         Match(3, 4),
#         Match(2, 5),
#         Match(15, 14),
#         Match(13, 7),
#         Match(10, 6),
#         Match(1, 8),
#         Match(0, 9)
#     ]),
#
#     Day(11, [
#         Match(12, 3),
#         Match(11, 2),
#         Match(4, 15),
#         Match(5, 13),
#         Match(14, 10),
#         Match(7, 1),
#         Match(6, 0),
#         Match(8, 9)
#     ]),
#
#     Day(12, [
#         Match(2, 12),
#         Match(15, 3),
#         Match(13, 11),
#         Match(10, 4),
#         Match(1, 5),
#         Match(0, 14),
#         Match(9, 7),
#         Match(8, 6)
#     ]),
#
#     Day(13, [
#         Match(12, 15),
#         Match(2, 13),
#         Match(3, 10),
#         Match(11, 1),
#         Match(4, 0),
#         Match(5, 9),
#         Match(14, 8),
#         Match(7, 6)
#     ]),
#
#     Day(14, [
#         Match(13, 12),
#         Match(10, 15),
#         Match(1, 2),
#         Match(0, 3),
#         Match(9, 11),
#         Match(8, 4),
#         Match(6, 5),
#         Match(7, 14)
#     ]),
#
#     Day(15, [
#         Match(12, 10),
#         Match(13, 1),
#         Match(15, 0),
#         Match(2, 9),
#         Match(3, 8),
#         Match(11, 6),
#         Match(4, 7),
#         Match(5, 14)
#     ])
# ]
#
# teams = [
#     Team('Boca', 'Grande', '0000', City('Buenos Aires', '')),
#     Team('River', 'Grande', '0001', City('Buenos Aires', '')),
#     Team('Racing', 'Grande', '0010', City('Buenos Aires', '')),
#     Team('Talleres', 'Normal', '0011', City('Buenos Aires', '')),
#     Team('Ferro', 'Normal', '0100', City('Buenos Aires', '')),
#     Team('San Lorenzo', 'Normal', '0101', City('Buenos Aires', '')),
#     Team('Huracan', 'Normal', '0110', City('Buenos Aires', '')),
#     Team('Velez', 'Normal', '0111', City('Buenos Aires', '')),
#     Team('Rosario Central', 'Normal', '1000', City('Buenos Aires', '')),
#     Team('Newells', 'Normal', '1001', City('Buenos Aires', '')),
#     Team('Union', 'Normal', '1010', City('Buenos Aires', '')),
#     Team('Gimnasia', 'Normal', '1011', City('Buenos Aires', '')),
#     Team('Colon', 'Normal', '1100', City('Buenos Aires', '')),
#     Team('Banfield', 'Normal', '1101', City('Buenos Aires', '')),
#     Team('Godoy Cruz', 'Normal', '1110', City('Buenos Aires', '')),
#     Team('Arsenal', 'Normal', '1111', City('Buenos Aires', '')),
# ]
#
# #TODO: Crear la matriz con datos reales
#
# # Generar matriz random
# N = 16
# distance_matrix = squareform(np.random.randint(3000, size=N*(N-1)//2))

# Recorro el gen y por cada equipo, busco los partidos donde fue visitante y calculo los kms recorridos.
# Cuando tengo en una lista los kms recorridos por todos los equipos, calculo la desviacion estandar del gen.
def fitness(genome: Genome, teams: [Team]) -> int:
    teams_km = []
    binary_teams = numpy.array_split(numpy.array(genome), len(teams))

    # Penalizo con una desviacion enorme a un gen que tenga equipos repetidos.
    if(len(binary_teams) != len(set(tuple(row) for row in binary_teams))):
        return 9999

    for i, team in enumerate(binary_teams):
        team_km = 0

        for day in fixture_1:
            for match in day.matches:
                team_string_number = ''.join(str(e) for e in list(team))
                visitingTeam = ''.join(str(e) for e in list(binary_teams[match.local_team_number]))
                if (match.visiting_team_number == i):
                    team_km += getDistanceTraveled(visitingTeam, team_string_number)
        teams_km.append(team_km)
    # 2 Calcular la desviacion estandar
    value = statistics.stdev(teams_km)

    return value

# Funcion que obtiene la distancia de la matriz de distancias
def getDistanceTraveled(localTeam, visitingTeam) -> int:
    local_team_index = int(localTeam, 2)
    visiting_team_index = int(visitingTeam, 2)

    distance_km = distance_matrix[local_team_index][visiting_team_index]

    return distance_km


# TODO: Adaptar para que muestre el fixture
# Funciones para imprimir por pantalla los resultados de la ejecucion del algoritmo.

def from_genome(genome: Genome, team_length: int, things: [Team]) -> [Team]:
    result = []
    teams_binary = numpy.array_split(numpy.array(genome), (len(genome) / team_length))
    for i, binary in enumerate(teams_binary):
        result += list(filter(lambda x: x.binaryId == ''.join(str(e) for e in list(binary)), things))

    return result

def to_string(things: [Team]):
    return f"[{', '.join([t.name for t in things])}]"


def value(things: [Team]):
    return sum([t.value for t in things])


def weight(things: [Team]):
    return sum([p.weight for p in things])


def print_stats(things: [Team]):
    print(f"Equipos: {to_string(things)}")
    # print(f"Value {value(things)}")
    # print(f"Weight: {weight(things)}")
