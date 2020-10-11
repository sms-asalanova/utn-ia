from functools import partial
from problems import fixture
from algorithms import genetic
from utils.analyze import timer

teams = fixture.teams

weight_limit = 3000

print("")
print("GENETIC ALGORITHM")
print("----------")

with timer():
	population, generations = genetic.run_evolution(
		populate_func=partial(genetic.generate_population, size=10, genome_length=len(things)),
		fitness_func=partial(knapsack.fitness, things=things, weight_limit=weight_limit),
		fitness_limit=result[0],
		generation_limit=100
	)

sack = fixture.from_genome(population[0], teams)
fixture.print_stats(sack)
