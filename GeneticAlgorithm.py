from numpy import random
import numpy as np
from collections import defaultdict
import heapq

from HeuristicFunctions import heuristic_function
from HeuristicComp import HeuristicCompTree as Game


WEIGHT_COUNT = 9


class Individual:
    def __init__(self, weights):
        self.weights = weights
        self.heuristic = heuristic_function(weights)


def individual(weights):
    return Individual(weights)


def random_weights():
    return [random.uniform(-1, 1) for _ in range(WEIGHT_COUNT)]


def population(count):
    return [individual(random_weights()) for _ in range(count)]


def breed_children(parents, num_children):
    children = []
    for _ in range(num_children):
        while True:
            mother, father = random.choice(parents, 2, replace=False)
            child = breed(mother, father)
            if child:
                break
        children.append(child)
    return children


def breed(mother, father):
    if mother == father:
        return

    father_weights = father.weights
    mother_weights = mother.weights
    num_weights = len(father_weights)

    child_weights = [breed_weights(
        mother_weights[i], father_weights[i]) for i in range(num_weights)]

    return individual(child_weights)


def breed_weights(mother_weight, father_weight):
    max_weight = max(mother_weight, father_weight)
    min_weight = min(mother_weight, father_weight)

    new_weight = random.uniform(min_weight * .95, max_weight * 1.05)

    return new_weight


def mutate_population(population):
    mutated_population = []
    for agent in population:
        if mutate > random.uniform(0, 1):
            mutated_agent = mutate_agent(agent)
            mutated_population.append(mutated_agent)
        else:
            mutated_population.append(agent)
    return mutated_population


def mutate_agent(agent):
    weights = agent.weights

    mutated_weights = [mutate_weight(weight) for weight in weights]

    return individual(mutated_weights)


def mutate_weight(weight):
    if weight < 0.5:
        new_weight = (1-weight) + random.uniform(-0.5, 0.1)
    else:
        new_weight = (1-weight) + random.uniform(-0.1, 0.5)

    if new_weight < 0:
        new_weight = 0
    elif new_weight > 1:
        new_weight = 1

    return new_weight


def play_games(population, num_games):
    scores = defaultdict(int)
    for game in range(num_games):
        print("Playing game #{} out of {}".format(game+1, num_games))

        competitors = random.choice(population, 2)
        north_competitor = competitors[0]
        south_competitor = competitors[1]

        game = Game(north_competitor, south_competitor)

        winner_index = game.run_game()
        loser_index = abs(winner_index - 1)

        winner = competitors[winner_index]
        loser = competitors[loser_index]

        scores[winner] += 1
        scores[loser] -= 1

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
    worst_performers = heapq.nsmallest(bottom_scorers_size, scores, key=score)

    random_from_bottom = random.choice(worst_performers, random_select_size)

    parents = best_perfomers + random_from_bottom.tolist()
    random.shuffle(parents)

    num_children = population_size - len(parents)
    children = breed_children(parents, num_children)

    new_population = parents + children
    mutated_population = mutate_population(new_population)

    return mutate_population


if __name__ == "__main__":
    pop_count = 1000
    evolution_cyles = 100
    pop = population(pop_count)
    history = []
    for i in range(evolution_cyles):
        print("Evolution round #{} of {}".format(i+1, evolution_cyles))
        pop = evolve(pop, games_factor=1, retain=0.4,
                     random_select=0.2, mutate=0.01)
        best_weights = [i.weights for i in pop if i]
        print(best_weights)
        history.append(best_weights)
