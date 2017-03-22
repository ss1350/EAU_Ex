#!/usr/bin/python3

import re
import queue
import sys
import os
import timeit


class Graph:

    def __init__(self):
        self._num_nodes = 0
        self._num_arcs = 0
        # List for storing node objects.
        self._nodes = []
        # List of lists for storing edge objects for each node.
        self._adjacency_lists = []

    def read_graph_from_file(self, file_name):
        """ Read in graph from .graph file.

        Specification of .graph file format:
            First line: number of nodes
            Second line: number of arcs
            3-column lines with node information:
                node_id latitude longitude
            4-column lines with edge information:
                tail_node_id head_node_id distance(m) max_speed(km/h)
        Comment lines (^#) are ignored

        >>> graph = Graph()
        >>> graph.read_graph_from_file('test.graph')
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        """
        c_lines = 0
        with open(file_name, 'rt') as f:
            for line in f:
                cols = line.strip().split(' ')
                # Skip comment lines.
                if re.search('^#', cols[0]):
                    continue
                c_lines += 1
                if c_lines == 1:
                    if self._num_nodes != 0:
                        raise Exception('Graph already read in')
                    self._num_nodes = int(cols[0])
                elif c_lines == 2:
                    self._num_arcs = int(cols[0])
                elif c_lines <= self._num_nodes + 2:  # all node info lines.
                    if not len(cols) == 3:
                        raise Exception('Node info line with != 3 cols')
                    node = Node(int(cols[0]), float(cols[1]), float(cols[2]))
                    # Append node to list.
                    self._nodes.append(node)
                    # Append empty adjacency list for node.
                    self._adjacency_lists.append([])
                else:  # all arc info lines.
                    if not len(cols) == 4:
                        raise Exception('Arc info line with != 4 cols')
                    tail_node_id = int(cols[0])
                    arc = Arc(tail_node_id, int(cols[1]), int(cols[2]),
                              int(cols[3]))
                    # Append arc to tail node's adjacency list.
                    self._adjacency_lists[tail_node_id].append(arc)
        f.closed

    def get_num_nodes(self):
        """Return number of nodes in graph."""
        return self._num_nodes

    def get_num_arcs(self):
        """Return number of arcs in graph."""
        return self._num_arcs

    def compute_reachable_nodes(self, node_id):
        """Mark all nodes reachable from given node.

        Implemented as breadth first search (BFS)
        Returns the number of reachable nodes (incl. start node)

        >>> graph = Graph()
        >>> graph.read_graph_from_file('test2.graph')
        >>> graph.compute_reachable_nodes(0)[0]
        4
        >>> graph.compute_reachable_nodes(4)[0]
        6
        >>> graph.compute_reachable_nodes(6)[0]
        1
        """
        # List of nodes to visit currently.
        current_level = [node_id]
        # Create list of marked nodes, marking reachable nodes with 1.
        marked_nodes = [0] * self._num_nodes
        marked_nodes[node_id] = 1  # Mark start node as reachable.
        num_marked_nodes = 1  # Store number of reachable nodes.
        # While there are still nodes to visit.
        while len(current_level) > 0:
            # Store nodes that are conntected to current_level nodes.
            next_level = []
            # Go through all current_level nodes.
            for curr_node_id in current_level:
                # Go through arcs of current node.
                for arc in self._adjacency_lists[curr_node_id]:
                    # If head_id not marked yet.
                    if not marked_nodes[arc.head_node_id]:
                        marked_nodes[arc.head_node_id] = 1
                        num_marked_nodes += 1
                        # Add head_id to new current level nodes.
                        next_level.append(arc.head_node_id)
            current_level = next_level
        return (num_marked_nodes, marked_nodes)

    def set_arc_costs_to_travel_time(self, max_vehicle_speed):
        """Set arc costs to travel time in whole seconds.

        >>> graph = Graph()
        >>> graph.read_graph_from_file('test.graph')
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        >>> graph.set_arc_costs_to_travel_time(100)
        >>> graph
        [0->1(4), 0->2(8), 1->2(2), 2->3(6), 3->1(5), 4->3(2)]
        """
        for i in range(self._num_nodes):
            for arc in self._adjacency_lists[i]:
                # Compute max possible speed for this arc.
                max_speed = min(arc.max_speed, int(max_vehicle_speed))
                # Compute travel time in whole seconds.
                travel_time_sec = '%.0f' % (arc.distance / (max_speed / 3.6))
                # Set costs to travel time in whole seconds.
                arc.costs = int(travel_time_sec)

    def set_arc_costs_to_distance(self):
        """Set arc costs to distance.

        >>> graph = Graph()
        >>> graph.read_graph_from_file('test.graph')
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        >>> graph.set_arc_costs_to_travel_time(100)
        >>> graph.set_arc_costs_to_distance()
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        """
        for i in range(self._num_nodes):
            for arc in self._adjacency_lists[i]:
                arc.costs = arc.distance

    def compute_lcc(self):
        """Mark all nodes in the largest connected component.

        >>> graph = Graph()
        >>> graph.read_graph_from_file('test.graph')
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        >>> graph.compute_lcc()
        (4, [4, 1, 2, 3])
        >>> graph2 = Graph()
        >>> graph2.read_graph_from_file('test2.graph')
        >>> graph2.compute_lcc()
        (6, [5, 1, 2, 3, 4])
        """
        unvisited_nodes = self._nodes[:]  # copy all nodes
        lcc = (0, None)

        # Visit all nodes which are in no connected component
        while len(unvisited_nodes) > 0:
            node = unvisited_nodes.pop()

            num_marked_nodes, marked_nodes \
                = self.compute_reachable_nodes(node._id)

            # Create a list with all visitied nodes in this lcc
            marked_indices = [node._id]
            for marked_node, marked in enumerate(marked_nodes):
                if marked == 1 and self._nodes[marked_node] in unvisited_nodes:
                    marked_indices.append(marked_node)
                    # Remove from unvisited list
                    # (start node was already removed)
                    unvisited_nodes.remove(self._nodes[marked_node])

            # Did we find a larger component?
            if num_marked_nodes > lcc[0]:
                lcc = num_marked_nodes, marked_indices

        return lcc

    def compute_shortest_paths(self, start_node_id):
        """ Compute the shortest paths for a given start node.

        Compute the shortest paths from the given start node
        using Dijkstra's algorithm.

        >>> graph = Graph()
        >>> graph.read_graph_from_file('test.graph')
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        >>> graph.compute_shortest_paths(1)
        >>> ['%d(%d)' % (node._id, node._distance) for node in graph._nodes]
        ['0(-1)', '1(0)', '2(20)', '3(70)', '4(-1)']
        """
        self._nodes[start_node_id]._distance = 0

        active_nodes = queue.PriorityQueue()
        active_nodes.put(self._nodes[start_node_id])

        while not active_nodes.empty():
            node = active_nodes.get()
            if node._settled:  # Node was already settled
                continue

            node._settled = True  # Settle active node

            # Updated all connected nodes
            for arc in self._adjacency_lists[node._id]:
                new_node = self._nodes[arc.head_node_id]
                new_distance = node._distance + arc.costs

                # Update if new distance is smaller than saved tentative dist.
                if not new_node._settled and \
                        (new_node._distance < 0 or
                         new_distance < new_node._distance):
                    new_node._distance = new_distance
                    new_node._traceback_arc = arc
                    active_nodes.put(new_node)

    def __repr__(self):
        """ Define object's string representation.

        >>> graph = Graph()
        >>> graph.read_graph_from_file('test.graph')
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        """
        obj_str_repr = ''
        for i in range(self._num_nodes):
            for arc in self._adjacency_lists[i]:
                obj_str_repr += repr(arc) + ', '
        if obj_str_repr:
            return '[' + obj_str_repr[:-2] + ']'
        else:
            return '[]'


class Node:

    def __init__(self, node_id, latitude, longitude, traceback_arc=None):
        self._id = node_id
        self._latitude = latitude
        self._longitude = longitude
        self._traceback_arc = traceback_arc
        self._settled = False
        self._distance = -1  # Start with negative distance

    def __repr__(self):
        """Define object's string representation."""
        return '%i' % (self._id)

    def __lt__(self, other):
        """Define the less than operator for our priority queue."""
        return self._distance < other._distance


class Arc:

    def __init__(self, tail_id, head_id, distance, max_speed):
        self.tail_node_id = tail_id  # ID of tail node.
        self.head_node_id = head_id  # ID of head node.
        self.distance = distance  # Distance in meter.
        self.max_speed = max_speed  # Maximum speed.
        self.costs = distance  # Set default costs to distance.

    def __repr__(self):
        """Define object's string representation."""
        return '%i->%i(%i)' % (self.tail_node_id, self.head_node_id,
                               self.costs)


def travel_to(graph, end_node, max_speed):
    """Compute distance and travel time of the selected path."""
    node = graph._nodes[end_node]
    time = 0  # Time in 'h'
    distance = 0  # Distance in 'km'

    while True:
        arc = node._traceback_arc
        if arc is None:
            break

        distance += arc.distance / 1000.0

        # v = s / t => t = s / v
        time += arc.distance / 1000.0 / min(arc.max_speed, max_speed)

        # Follow to previous node
        node = graph._nodes[arc.tail_node_id]

    return (distance, time_to_string(time))


def generate_mapbb(graph, end_node, file_name, name, color, is_first, is_last):
    """Generate a MapBB file for the selected path."""
    if is_first:  # Delete if the file already exists
        try:
            os.remove(file_name)
        except FileNotFoundError as e:
            pass

    # Open with options 'append'(a) and 'text'(t)
    with open(file_name, 'at') as f:
        if is_first:
            f.write('[map]')

        node = graph._nodes[end_node]
        while True:
            arc = node._traceback_arc
            if arc is None:
                break

            f.write('%.4f,%.4f' % (node._latitude, node._longitude))

            # Follow to previous node
            node = graph._nodes[arc.tail_node_id]
            if node._traceback_arc is not None:
                f.write(' ')

        f.write('(%s|%s)%s' % (color, name, '; ' if not is_last else ''))

        if is_last:
            f.write('[/map]')


def time_to_string(time):
    """Convert time in hours to string format."""
    hours = int(time)
    minutes = int((time - hours) * 60)
    return '%d hour(s) %d minute(s)' % (hours, minutes)


def reset_graph(graph):
    """Resets the graph and it's fields."""
    for node in graph._nodes:
        node._traceback_arc = None
        node._settled = False
        node._distance = -1


def get_furthest_node(graph):
    """Return the id of the furthest node."""
    max_dist = (-1, None)

    for node in graph._nodes:
        if node._distance > max_dist[0]:
            max_dist = (node._distance, node._id)

    return max_dist[1]


if __name__ == '__main__':
    def helper_fnc(graph, max_speed, result):
        """Calculate shortest path and do a trace back."""
        graph.compute_shortest_paths(5508637)
        result[0], result[1] = travel_to(graph, 4435496, max_speed)

    graph = Graph()
    print('Loading map')

    # We explicitly don't use the timeit method since we want the garbage
    # collector to stay activated
    start_time = timeit.default_timer()
    graph.read_graph_from_file('bawue_bayern.graph')

    print('Loaded map in %.2f s' % (timeit.default_timer() - start_time))
    print()  # Create new line
    graph.set_arc_costs_to_distance()

    # --------------- Distance ------------------------------------------------

    res = [None, None, None]
    res[2] = timeit.timeit(stmt=lambda: helper_fnc(graph, sys.maxsize, res),
                           number=1)
    print('Shortest path:')
    print('Distance %d km, Time %s, Computation time %.2f s'
          % (res[0], res[1], res[2]))
    generate_mapbb(graph, 4435496, 'nuremberg.map', 'distance', 'blue',
                   True, False)

    max_dist = get_furthest_node(graph)
    print('Longest path:')
    print('Distance %d km, Time %s' % travel_to(graph, max_dist, sys.maxsize))
    generate_mapbb(graph, max_dist, 'furthest.map', 'distance', 'blue',
                   True, False)

    print()  # Create new line

    reset_graph(graph)
    graph.set_arc_costs_to_travel_time(130)

    # --------------- Time 130 km/h -------------------------------------------

    res = [None, None, None]
    res[2] = timeit.timeit(stmt=lambda: helper_fnc(graph, 130, res),
                           number=1)
    print('Fastest path with 130 km/h:')
    print('Distance %d km, Time %s, Computation time %.2f s'
          % (res[0], res[1], res[2]))
    generate_mapbb(graph, 4435496, 'nuremberg.map', '130 km/h', 'red',
                   False, False)

    max_dist = get_furthest_node(graph)
    print('Slowest path with 130 km/h:')
    print('Distance %d km, Time %s' % travel_to(graph, max_dist, 130))
    generate_mapbb(graph, max_dist, 'furthest.map', '130 km/h', 'red',
                   False, False)

    print()  # Create new line

    reset_graph(graph)
    graph.set_arc_costs_to_travel_time(100)

    # --------------- Time 100 km/h -------------------------------------------

    res = [None, None, None]
    res[2] = timeit.timeit(stmt=lambda: helper_fnc(graph, 100, res),
                           number=1)
    print('Fastest path with 100 km/h:')
    print('Distance %d km, Time %s, Computation time %.2f s'
          % (res[0], res[1], res[2]))
    generate_mapbb(graph, 4435496, 'nuremberg.map', '100 km/h', 'green',
                   False, True)

    max_dist = get_furthest_node(graph)
    print('Slowest path with 100 km/h:')
    print('Distance %d, Time %s' % travel_to(graph, max_dist, 100))
    generate_mapbb(graph, max_dist, 'furthest.map', '100 km/h', 'green',
                   False, True)
