import random as rand

from nomad.util import *

def background():
    def generate(plains, edge_coords):
        return dict((xy, [plains.floor_entity()]) for xy in edge_coords)
    return generate


def random(*entities):
    def generate(plains, edge_coords):
        new_ents = {}
        for xy in edge_coords:
            new_ents[xy] = [plains.floor_entity(), rand.choice(entities)()]
        return new_ents
    return generate


def chance(prob2ent):
    probs = sorted(prob2ent.keys(), key=lambda x: x + rand.random())
    def generate(plains, edge_coords):
        new_ents = {}
        for xy in edge_coords:
            new_ents[xy] = [plains.floor_entity()]
            roll = rand.random()
            for prob in probs:
                if roll * 100 <= prob:
                    entity = prob2ent[prob]
                    new_ents[xy].append(entity())
                    break
        return new_ents
    return generate
