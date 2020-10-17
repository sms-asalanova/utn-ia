from functools import partial
from problems import fixture
from algorithms import genetic
from utils.analyze import timer

teams = fixture.teams

binaryBits = 2
genome_length = binaryBits * len(teams)
size = 1000


print("")
print("GENETIC ALGORITHM")
print("----------")
print("teams",teams)
print("size",size)
with timer():
	population, generations = genetic.run_evolution(
		populate_func=partial(genetic.generate_population, size=size, genome_length=genome_length),
		fitness_func=partial(fixture.fitness, teams=teams),
		fitness_limit=0.5,
		generation_limit=1000
	)

sack = fixture.from_genome(population[0], binaryBits, teams)
fixture.print_stats(sack)
