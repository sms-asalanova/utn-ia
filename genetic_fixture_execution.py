from functools import partial
from problems import fixture
from algorithms import genetic
from utils.analyze import timer

teams = fixture.teams

binaryBits = 3
genome_length = binaryBits * len(teams)

print("")
print("GENETIC ALGORITHM")
print("----------")

with timer():
	population, generations = genetic.run_evolution(
		populate_func=partial(genetic.generate_population, size=100, genome_length=genome_length),
		fitness_func=partial(fixture.fitness, teams=teams),
		fitness_limit=0.5,
		generation_limit=100
	)

sack = fixture.from_genome(population[0], binaryBits, teams)
fixture.print_stats(sack)
