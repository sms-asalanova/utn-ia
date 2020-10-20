class Genome():
    def __init__(self, teams,fitness_value):
        self.teams = teams
        self.fitness_value = fitness_value

    def set_fitness_value(self, fitness_value):
        self.fitness_value = fitness_value