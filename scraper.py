# -*- coding: utf-8 -*-

import requests
from lxml import html
import networkx as nx
import argparse
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c',
    '--task',
    choices=['distance', 'leaf'],
    required=True,
    help='choose task {distance} in order to calculate the distance '
         'between two species; choose task {leaf} in order to build '
         'a tree of life (you may specify a certain distance up to 6'
         ') to the top for one species')
parser.add_argument(
    '-f',
    '--leaf_from',
    type=str,
    required=True,
    help='a "leaf_from" species (corresponding to ending of '
         'the Wikipedia link)')
parser.add_argument(
    '-t',
    '--leaf_to',
    type=str,
    help='a "leaf_to" species (corresponding to ending of '
         'the Wikipedia link), required if the task is "distance"')
parser.add_argument(
    '-l',
    '--level',
    type=int,
    choices=[1, 2, 3, 4, 5, 6],
    help='certain distance up in a tree of life of the species (default: 6)')
parser.add_argument(
    '-d',
    '--draw',
    action='store_true',
    help='draw the graph')
args = parser.parse_args()

TAXONOMIC_RANKS = [
    'Species:', 'Genus:', 'Family:', 'Order:', 'Class:', 'Phylum:',
    'Division:', 'Kingdom:'
]
WIKI_URL = 'http://en.wikipedia.org/wiki/'

evo_graph = nx.Graph()


def to_tree(species, level=None):
    """

    :param species: (corresponding to ending of the Wikipedia link) for which
                    a tree of life should be extended.
    :type species: str
    :param level: certain distance up in a tree of life of the species
                  (level є [1; 6])
    :type level: int
    :return: scientific name of the species
    """
    species_url = WIKI_URL + species
    species_page = requests.get(species_url)
    species_dom = html.fromstring(species_page.text)
    evo_graph.add_node(
        species_dom.xpath('//span[@class="species"]')[0][0][0].text)
    ranks = [
        species_dom.xpath('//span[@class="species"]')[0][0][0].text,
    ]
    if not level:
        level = 6
    i = 0
    while i < level and i < 10:
        try:
            ranks.append(
                species_dom.xpath('//td[text()="{}"]/following-sibling::td[1]'
                                  '//a'.format(TAXONOMIC_RANKS[i]))[0].text)
            evo_graph.add_node(ranks[-1])
            evo_graph.add_edge(ranks[-1], ranks[-2])
        except IndexError:
            level += 1
        i += 1
    return species_dom.xpath('//span[@class="species"]')[0][0][0].text


def find_distance(sp1, sp2, level=None):
    """

    :param sp1: species (corresponding to ending of the Wikipedia link)
    :type sp1: str
    :param sp2: species (corresponding to ending of the Wikipedia link)
    :type sp2: str
    :param level: certain distance up in a tree of life of the species
                  (level є [1; 6])
    :type level: int
    :return:
    """
    node_sp1 = to_tree(species=sp1, level=level)
    node_sp2 = to_tree(species=sp2, level=level)
    try:
        distance = nx.algorithms.shortest_paths.generic. \
                       shortest_path_length(evo_graph, node_sp1, node_sp2) // 2
        print('# Result ##########################'
              '\n{0} has a species name {1}.'
              '\n{2} has a species name {3}.'
              '\nThe distance between {1} and {3} is {4}.'
              '\n###################################'.format(sp1.capitalize(),
                                                             node_sp1.lower(),
                                                             sp2.capitalize(),
                                                             node_sp2.lower(),
                                                             distance))
        return distance
    except nx.exception.NetworkXNoPath:
        print("No path between {0} and {1}. "
              "Try to run again without setting flag -l (--level)".format(sp1,
                                                                          sp2))


if __name__ == '__main__':
    try:
        if args.task == 'distance':
            if not args.leaf_to:
                logging.info('PLease, enter leaf_to using flag -t')
            else:
                find_distance(args.leaf_from, args.leaf_to, args.level)
        if args.task == 'leaf':
            to_tree(args.leaf_from, args.level)
        if args.draw:
            import matplotlib.pyplot as plt
            plt.subplot(121)
            nx.draw(evo_graph, with_labels=True)
            plt.show()
    except IndexError:
        print('Please, make sure the species name(-s) match(-es) the ending '
              'of their Wikipedia page URL.')
