from algorithms.genetic import Genome
from collections import namedtuple
import numpy
import math
import statistics

Fixture = namedtuple('Thing', ['name', 'value', 'weight'])

Team = namedtuple('Team', ['name', 'size', 'binaryId', 'city'])
City = namedtuple('City', ['name', 'location']) #TODO: Definir que es "location",  coordenadas, ubicacion en la matriz de distancia?


# Primer fixture mas chico, 4 equipos
teams = [
    Team('Boca', 'Grande', '00', City('Buenos Aires', '')),
    Team('River', 'Grande', '01', City('Buenos Aires', '')),
    Team('Racing', 'Grande', '10', City('Buenos Aires', '')),
    Team('Talleres', 'Normal', '11', City('Buenos Aires', '')),
]

#TODO: Crear la matriz con datos reales
distance_matrix = [[0,11,41,25],
                   [11,0,1,4],
                   [41,1,0,30],
                   [25,4,30,0]]

# TODO: Matriz de distancias.

def fitness(genome: Genome, teams: [Team]) -> int:
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
        penalty = 0
        team_km = 0
        teams_played = []
        repeated_team = False

        for day in days:
            games_played = 0
            for match in day:
                indexA = int(team_binary_length)
                indexB = int((team_binary_length * 2))

                localTeam = ''.join(str(e) for e in list(match[0: indexA]))
                visitingTeam = ''.join(str(e) for e in list(match[indexA: indexB]))

                if localTeam == team.binaryId:
                    games_played += 1
                    teams_played.append(visitingTeam)
                    if len(list(filter(lambda x: x == visitingTeam, teams_played))) > 1:
                        repeated_team = True

                if visitingTeam == team.binaryId:
                    games_played += 1
                    teams_played.append(localTeam)
                    if len(list(filter(lambda x: x == localTeam, teams_played))) > 1:
                        repeated_team = True

                if visitingTeam == team.binaryId: #El equipo deberia tener un campo que lo relacione con el binario
                    team_km += getDistanceTraveled(localTeam, visitingTeam)

            if games_played != 1:
                return 999
        if repeated_team:
            return 999

        teams_km.append(team_km) #Funcion que obtiene la distancia de la matriz de distancias

    # 2 Calcular la desviacion estandar
    value = statistics.stdev(teams_km) + penalty

    return value



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
    print(f"Things: {to_string(things)}")
    # print(f"Value {value(things)}")
    # print(f"Weight: {weight(things)}")
