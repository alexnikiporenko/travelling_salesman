# importing libraries
import math
import random
from matplotlib import pyplot as plt

# class to store maps
class Map:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.distance_matrix = self.populate_distance_matrix(coordinates)

    def plot(self):
        x, y = zip(*self.coordinates)
        plt.scatter(x, y, c="r")
        plt.suptitle(f"{len(self.coordinates)}-node map")
        plt.show()

    # distance between individual nodes is calculated using Pythagoras theorem
    def calculate_hypotenuse(self, coordinates, a, b):
        x1, y1 = coordinates[a]
        x2, y2 = coordinates[b]
        return math.sqrt( abs(x1-x2)**2 + abs(y1-y2) )

    # distance matrix is used to store distances between individual nodes
    def populate_distance_matrix(self, coordinates):
        l = len(coordinates)
        dist_matrix = [[0 for j in range(l)] for i in range(l)]
        for i in range(l):
            for j in range(i, l):
                dist_matrix[i][j] = self.calculate_hypotenuse(coordinates, i, j)
                dist_matrix[j][i] = dist_matrix[i][j]
        return dist_matrix

    def __repr__(self):
        return f"{len(self.coordinates)}-node map"

# class to store routes
class Route:
    def __init__(self, map, path):
        self.map = map
        self.path = path
        self.distance = calculate_distance(map, path)
        # fitness used in Genetic Algorithm
        self.fitness = 0

    def update_path(self, new_path):
        self.path = new_path
        self.distance = calculate_distance(self.map, self.path)

    def plot(self):
        r = [self.map.coordinates[self.path[-1]]]
        for n in self.path:
            r.append(self.map.coordinates[n])
        x, y = zip(*r)
        plt.scatter(x, y, c="r")
        plt.plot(x, y)
        plt.suptitle(f"Distance = {self.distance}")
        plt.show()

    def __repr__(self):
        return f"{len(self.path)}-node route, distance = {self.distance}"

# a function for calculating a distance of a path
def calculate_distance(map, path):
    l = len(path)
    total = 0
    for i in range(l):
        total += map.distance_matrix[path[i]][path[(i+1)%l]]
    return total

# function generating a random initial path
def create_initial_random(map):
    indices = list(range(len(map.coordinates)))
    random.seed(1)
    random.shuffle(indices)
    return indices

# function generating the initial path using greedy algorithm
# always choosing the closest unvisited node
def create_initial_greedy(map, start=None):
    if start is None:
        path = [random.randrange(len(map.coordinates))]
    else:
        path = [start]
    while len(path) < len(map.coordinates):
        current = path[-1]
        indices = [ind for ind in range(len(map.coordinates)) if ind not in path]
        smallest = float("inf")
        next = -1
        for ind in indices:
            if map.distance_matrix[current][ind] < smallest:
                smallest = map.distance_matrix[current][ind]
                next = ind
        path.append(next)
    return path
    
# function that swaps two random nodes
def node_swapper(path):
    p = list(path)
    index1 = random.randrange(0, len(p))
    index2 = index1
    while index2 == index1:
        index2 = random.randrange(0, len(p))
    temp = p[index2]
    p[index2] = p[index1]
    p[index1] = temp
    return p

# importing a map of 24 nodes
with open("24node.csv") as input:
    map24_coordinates = [tuple([float(n) for n in line.split(",")]) for line in input.read().splitlines()]

map24 = Map(map24_coordinates)

# two initial routes: random and greedy
map24_random = Route(map24, create_initial_random(map24))

# importing a random map of 150 nodes
with open("150node_random.csv") as input:
    map150_coordinates = [tuple([float(n) for n in line.split(",")]) for line in input.read().splitlines()]
    
map150 = Map(map150_coordinates)

# two initial routes: random and greedy
map150_random = Route(map150, create_initial_random(map150))
map150_greedy = Route(map150, create_initial_greedy(map150, start=88))

# # use this code to create more maps
# import random
# import csv

# map1000_coordinates = []

# for i in range(1000):
#     a = round(random.uniform(0, 10), 3)
#     b = round(random.uniform(0, 10), 3)
#     map1000_coordinates.append((a, b))

# with open('1000node_random.csv', 'w', newline='') as out:
#     writer = csv.writer(out)
#     for coord in map1000_coordinates:
#         writer.writerow((coord[0], coord[1]))

# importing a random map of 150 nodes
with open("1000node_random.csv") as input:
    map1000_coordinates = [tuple([float(n) for n in line.split(",")]) for line in input.read().splitlines()]
    
map1000 = Map(map1000_coordinates)

map1000_greedy = Route(map1000, create_initial_greedy(map1000, start=600))