import csv
from models.fixture import Fixture 
from models.city import City
from models.team import Team
from algorithms import genetic as ga
import pandas as pd 
from datetime import datetime


def get_fechas(path_to_file):
    fechas = []
    with open(path_to_file, 'r') as csvfile:
        fechas_csv = csv.reader(csvfile, delimiter='\t')
        next(fechas_csv)
        for fecha in fechas_csv:
            fechas.append(fecha[0])
    return fechas

def get_fixture(path_to_file) -> []:
    fixture = []
    with open(path_to_file, 'r') as csvfile:
        f_csv = csv.reader(csvfile, delimiter=',')
        next(f_csv)

        for f in f_csv:
            fix = Fixture(fecha=f[0],local=f[1],visitante=f[2])
            fixture.append(fix)
    return fixture

def get_cities(path_to_file) -> []:
    cities = []
    with open(path_to_file, 'r') as csvfile:
        c_csv = csv.reader(csvfile, delimiter=',')
        next(c_csv)

        for c in c_csv:
            city = City(name=c[0],locality=c[1])
            cities.append(city)
    return cities

    
def get_teams(path_to_file) -> []:
    teams = []
    with open(path_to_file, 'r') as csvfile:
        f_csv = csv.reader(csvfile, delimiter=',')
        next(f_csv)

        for f in f_csv:
            team = Team(name=f[0],size=f[1],binary_id=f[2],last_match="",city=City("",""))
            teams.append(team)
    return teams

def populate_cities_in_teams(cities, teams):
    for c in cities:
        for team in teams:
            if c.name == team.city.name:
                team.city = c

def get_distances(path_to_file) -> []:
    df = pd.read_csv(path_to_file,delimiter=',')
    return df

def calculate_distances_mean(distances,cities):
    mean = 0
    for city in cities:
        for km in distances[city.name]:
            mean = mean + km
    mean = mean/len(cities)/len(cities)
    return mean

if __name__ == "__main__":
    fechas = get_fechas('datasets/24/fechas.csv')
    fixture = get_fixture('datasets/24/localVisitante.csv')
    teams = get_teams('datasets/24/teams.csv')
    cities = get_cities('datasets/cities.csv')    
    populate_cities_in_teams(cities,teams)
  
    distances = get_distances('datasets/distances.csv') 
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Init Time =", current_time)
    population_size = 100000
    print("population_size:",population_size)
    population = ga.generate_population(population_size=population_size,genome_length=len(teams),teams=teams)
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Final Time =", current_time)
    
