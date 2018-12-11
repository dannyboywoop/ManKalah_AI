import numpy as np
import heapq
from progressbar import progressbar
from numpy import random
from collections import defaultdict

from HeuristicFunctions import heuristic_function
from HeuristicComp import HeuristicCompTree as Game


WEIGHT_COUNT = 10


def random_weights():
    return np.array([random.uniform(0, 1) for _ in range(WEIGHT_COUNT)])


def population(population_size):
    return np.array([random_weights() for _ in range(population_size)])


def breed_children(parents, num_children):
    children = []
    for _ in range(num_children):
        while True:
            choices = np.random.choice(len(parents), 2)
            mother, father = parents[choices]
            child = breed_individuals(mother, father)
            if child is not None:
                break
        children.append(child)
    return np.array(children)


def breed_individuals(mother, father):
    if np.array_equal(mother, father):
        return

    return np.array(
        [breed_weights(mother[i], father[i]) for i in range(WEIGHT_COUNT)]
    )


def breed_weights(mother_weight, father_weight):
    max_weight = max(mother_weight, father_weight)
    min_weight = min(mother_weight, father_weight)

    new_weight = random.uniform(min_weight * .95, max_weight * 1.05)

    return new_weight


def mutate_population(population, mutation_rate):
    mutated_population = []
    for individual in population:
        if mutation_rate > random.uniform(0, 1):
            mutated_individual = mutate_individual(individual)
            mutated_population.append(mutated_individual)
        else:
            mutated_population.append(individual)
    return np.array(mutated_population)


def mutate_individual(individual):
    return np.array(
        [mutate_weight(weight) for weight in individual]
    )


def mutate_weight(weight):
    new_weight = weight + random.normal(scale=0.333)

    if new_weight < 0:
        new_weight = 0
    elif new_weight > 1:
        new_weight = 1

    return new_weight


def array_to_key(array):
    return ','.join(str(x) for x in array)


def play_games(population, num_games):
    scores = defaultdict(int)
    for game in progressbar(range(num_games)):
        choices = np.random.choice(len(population), 2)
        competitors = population[choices]

        winner_index = Game(competitors[0], competitors[1]).run_game()
        loser_index = (winner_index + 1) % 2

        winner = competitors[winner_index]
        loser = competitors[loser_index]

        scores[winner.tostring()] += 1
        scores[loser.tostring()] -= 1

    return scores


def evolve(population, games_factor=2, retain=.2, random_select=.1, mutate=.1):
    population_size = len(population)
    num_games = population_size * games_factor

    scores = play_games(population, num_games)

    top_scorers_size = int(retain * population_size)
    bottom_scorers_size = population_size - top_scorers_size
    random_select_size = int(population_size * random_select)

    score = scores.get
    best_perfomers = heapq.nlargest(top_scorers_size, scores, key=score)
    best_perfomers = np.array([np.fromstring(x) for x in best_perfomers])

    record_best_performers(best_perfomers)

    worst_performers = heapq.nsmallest(bottom_scorers_size, scores, key=score)
    worst_performers = np.array([np.fromstring(x) for x in worst_performers])

    random_choices_from_bottom = np.random.choice(
        bottom_scorers_size, random_select_size)
    random_from_bottom = worst_performers[random_choices_from_bottom]

    parents = np.concatenate((best_perfomers, random_from_bottom), axis=0)
    random.shuffle(parents)

    num_children = population_size - len(parents)
    children = breed_children(parents, num_children)

    new_population = np.concatenate((parents, children), axis=0)
    mutated_population = mutate_population(new_population, mutate)

    return mutated_population


def record_best_performers(best_perfomers):
    with open("best-performers.txt", "a+") as f:
        f.write(str(best_perfomers) + "\n\n")


if __name__ == "__main__":
    pop_count = 5
    evolution_cyles = 2000
    population = population(pop_count)
    for i in range(evolution_cyles):
        print("Evolution number {}".format(i+1))
        population = evolve(
            population,
            games_factor=1,
            retain=0.4,
            random_select=0.2,
            mutate=0.01
        )
