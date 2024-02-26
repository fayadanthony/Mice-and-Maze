# Given: A set of laboratory mice is being trained to escape a maze. The maze is made up of cells, and each cell
# is connected to some other cells. However, there are obstacles in the passage between cells and therefore
# there is a time penalty to overcome the passage Also, some passages allow mice to go one-way, but not
# the other way round.
# Suppose that all mice are now trained and, when placed in an arbitrary cell in the maze, take a
# path that leads them to the exit cell in minimum time.
# We are going to conduct the following experiment: a mouse is placed in each cell of the maze and
# a count-down timer is started. When the timer stops we count the number of mice out of the maze.
# Write a program that, given a description of the maze and the time limit, predicts the number of
# mice that will exit the maze. Assume that there are no bottlenecks is the maze, i.e. that all cells have
# room for an arbitrary number of mice.

import numpy as np
import networkx as nx

def main():
    cases = int(input())
    nbMice = []
    
    for i in range(cases):
        nbCells = int(input())
        exitCell = int(input())
        countdown = int(input())
        nbConnections = int(input())
        connections = np.empty((nbConnections, 3))
        
        for j in range(nbConnections):
            a = input()
            for k in range(3):
                connections[j, k] = int(a.split(' ')[k])
        
        nbMice.append(Dijkstra(nbCells, exitCell, countdown, connections))
       
        G = nx.DiGraph()
        for j in range(nbConnections):
            G.add_edge(connections[j,0], connections[j,1], weight = connections[j,2])
        for j in range(1,nbCells+1,1):
            G.add_node(j, label=str(j))
        labels = nx.get_edge_attributes(G,'weight')
        pos=nx.spring_layout(G)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        nx.draw(G, pos,with_labels=True)
        
        print(nbMice[i])


def Dijkstra(nbCells, exitCell, countdown, connections):
    nbMice = 0

    for i in range(1, nbCells+1, 1):
        if i == exitCell:
            nbMice += 1
            continue
        
        N = {i: 0}

        for j in range(1, nbCells+1, 1):
            if j != i:
                N.update({j: CalculateCost(i, j, connections)})
                
        while ValsNotinN(nbCells, N):
            V={}

            for val in ValsNotinN(nbCells, N):
                V.update({val:N.get(val)})
                
            w = V.keys()[V.values().index(min(np.array(V.values())))]

            for j in range(nbCells):
                if CalculateCost(i, j, connections) != np.inf:
                    N.update({j: min(N.get(j), N.get(w) + CalculateCost(w, j, connections))})

        if (N.get(exitCell) <= countdown):
            nbMice += 1

    return nbMice


def CalculateCost(a, b, connections):
    for i in range(connections.shape[0]):
        if connections[i, 0] == a and connections[i, 1] == b:
            return connections[i, 2]
    return np.inf


def ValsNotinN(nbCells, N):
    V = []
    for i in range(1,nbCells+1,1):
        if i not in N.keys():
            V.append(i)
    return V


main()