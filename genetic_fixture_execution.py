from functools import partial
from problems import fixture
from algorithms import genetic
from utils.analyze import timer

teams = fixture.teams

weight_limit = 3000
binaryBits = 2
genome_length = binaryBits * len(teams) * (len(teams) - 1)

print("")
print("GENETIC ALGORITHM")
print("----------")

with timer():
	population, generations = genetic.run_evolution(
		populate_func=partial(genetic.generate_population, size=20, genome_length=genome_length),
		fitness_func=partial(fixture.fitness, teams=teams),
		fitness_limit=0.5,
		generation_limit=3000
	)

# print(population[0])
# print(len(population))
sack = fixture.from_genome(population[0], binaryBits, teams)
fixture.print_stats(sack)
