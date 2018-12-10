from numpy import random
from collections import defaultdict
import heapq

from HeuristicFunctions import heuristic_function
from HeuristicComp import HeuristicCompTree as Game


WEIGHT_COUNT = 7


class Individual:
    def __init__(self, weights):
        self.weights = weights
        self.heuristic = heuristic_function(weights)


def individual(weights):
    return Individual(weights)


def random_weights():
    return [random.uniform(0, 1) for _ in range(WEIGHT_COUNT)]


def population(count):
    return [individual(random_weights()) for _ in range(count)]


def breed(mother, father):
    if mother == father:
        print('Cannot breed with itself: Error: Mother == Father')
        return

    father_weights = father.weights
    mother_weights = mother.weights

    child_weights = []
    for index in range(len(father_weights)):
        father_weight = father_weights[index]
        mother_weight = mother_weights[index]
        new_child_weight = breed_specific_weight(father_weight, mother_weight)
        child_weights.append(new_child_weight)

    return individual(child_weights)


def breed_specific_weight(mother, father):
    if father > mother:
        child_weight = random.uniform(mother * .95, father * 1.05)
    else:
        child_weight = random.uniform(father * .95, mother * 1.05)

    if child_weight < 0:
        child_weight = 0
    elif child_weight > 1:
        child_weight = 1

    return child_weight


def mutate_agent(agent):
    weights = agent.weights

    new_weights = []
    for weight in weights:
        mutated_weight = mutate_specific_weight(weight)
        new_weights.append(mutated_weight)

    return individual(new_weights)


def mutate_specific_weight(weight):
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
        scores[loser] -= -1

    return scores


def evolve(pop, games_factor=2, retain=0.2, random_select=0.05, mutate=0.01):
    num_games = len(pop) * games_factor
    scores = play_games(pop, num_games)

    top_performers_size = int(retain * len(pop))
    bottom_performers_size = len(pop) - top_performers_size
    rand_select_size = int(len(pop) * random_select)

    key = scores.get
    best_perfomers = heapq.nlargest(top_performers_size, scores, key=key)
    worst_performers = heapq.nsmallest(bottom_performers_size, scores, key=key)

    random_from_worst = random.choice(worst_performers, rand_select_size)

    parents = best_perfomers + random_from_worst.tolist()
    random.shuffle(parents)

    # Create children
    num_children = len(pop) - len(parents)

    children = []
    for i in range(num_children):
        while True:
            current_parents = random.choice(parents, 2, replace=False)
            father = current_parents[0]
            mother = current_parents[1]
            child = breed(mother, father)
            if child:
                break
        children.append(child)

    new_pop = parents + children

    mutated_pop = []
    # Randomly mutate some of the new population
    for agent in new_pop:
        if mutate > random.uniform(0, 1):
            mutated_agent = mutate_agent(agent)
            mutated_pop.append(mutated_agent)
        else:
            mutated_pop.append(agent)
    return mutated_pop


if __name__ == "__main__":
    pop_count = 5
    evolution_cyles = 2
    pop = population(pop_count)
    history = []
    for i in range(evolution_cyles):
        print("Evolution round #{} of {}".format(i+1, evolution_cyles))
        pop = evolve(pop, games_factor=1, retain=0.4,
                     random_select=0.2, mutate=0.01)
        best_weights = [i.weights for i in pop if i]
        print(best_weights)
        history.append(best_weights)

    print('Evolution Results:')
    [x for x in history]
