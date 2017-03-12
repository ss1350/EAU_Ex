#!/usr/bin/python3

import re
import heapq


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
        >>> graph.read_graph_from_file("test.graph")
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        """
        c_lines = 0
        with open(file_name) as f:
            for line in f:  # einzelne Linien einlesen
                cols = line.strip().split(" ")  # nach spalten aufteilen
                # Skip comment lines.
                if re.search("^#", cols[0]):    # Kommentare ignorieren
                    continue
                c_lines += 1    # Linien mitzählen (wenn nicht Kommentarlinie)
                if c_lines == 1:    # 1. Linie = Anzahl der Nodes
                    if self._num_nodes != 0:
                        raise Exception("Graph already read in")
                    self._num_nodes = int(cols[0])
                    # Wert für Anzahl der Linien übernehmen
                elif c_lines == 2:  # 2. Linie = Anzahl der Kanten (arcs)
                    self._num_arcs = int(cols[0])
                elif c_lines <= self._num_nodes + 2:  # all node info lines.
                    # (+2 wegen Anzahlinformation)
                    if not len(cols) == 3:
                        # Fehler: Node Unvollständig angegeben
                        raise Exception("Node info line with != 3 cols")
                    node = Node(int(cols[0]), float(cols[1]), float(cols[2]))
                    # Append node to list.
                    self._nodes.append(node)
                    # Append empty adjacency list for node.
                    self._adjacency_lists.append([])
                else:  # all arc info lines. (Kanten)
                    if not len(cols) == 4:
                        raise Exception("Arc info line with != 4 cols")
                    tail_node_id = int(cols[0])
                    # Warum tail node id zwischenspeichern?
                    arc = Arc(tail_node_id, int(cols[1]), int(cols[2]),
                              int(cols[3]))
                    # Append arc to tail node's adjacency list.
                    self._adjacency_lists[tail_node_id].append(arc)
                    # Fügt Kante zur Verbindungsliste[Knoten] zu
        f.closed

    def getNode(self, node_id):
        """
        returns node with given node_id
        """
        for i in range(len(self._nodes)):
            if self._nodes[i]._id == node_id:
                return self._nodes[i]
        return None

    def get_num_nodes(self):
        """Return number of nodes in graph."""
        return self._num_nodes

    def get_num_arcs(self):
        """Return number of arcs in graph."""
        return self._num_arcs

    def compute_reachable_nodes(self, node_id):
        """Mark all nodes reachable from given node.
        Given Node = start node, ends when next level = 0
        (no fresh unmarked nodes)

        Implemented as breadth first search (BFS)
        Returns the number of reachable nodes (incl. start node)

        >>> graph = Graph()
        >>> graph.read_graph_from_file("test2.graph")
        >>> graph.compute_reachable_nodes(0)
        4
        >>> graph.compute_reachable_nodes(4)
        6
        >>> graph.compute_reachable_nodes(6)
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
        output = (marked_nodes, num_marked_nodes)
        return output

    def set_arc_costs_to_travel_time(self, max_vehicle_speed):
        """Set arc costs to travel time in whole seconds.
        Suchkriterium: Zeit

        >>> graph = Graph()
        >>> graph.read_graph_from_file("test.graph")
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
                travel_time_sec = "%.0f" % (arc.distance / (max_speed / 3.6))
                # Set costs to travel time in whole seconds.
                arc.costs = int(travel_time_sec)

    def set_arc_costs_to_distance(self):
        """Set arc costs to distance.
        Suchkriterium: Entfernung

        >>> graph = Graph()
        >>> graph.read_graph_from_file("test.graph")
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

    def compute_lcc(self, marked_nodes):
        """Mark all nodes in the largest connected component.
        Find the highest count of marked nodes

        calculates all connected components and
        marks the nodes in the largest connected component

        use compute_reachable_nodes to find largest connected component
        then mark it's nodes
        """
        max_count = 0
        max_nodes = []
        for n in self._nodes:
            if (n._id in max_nodes):
                continue
            t_nodes_marked, t_num_marked = self.compute_reachable_nodes(n._id)
            if t_num_marked > max_count:
                max_count = t_num_marked
                max_nodes = t_nodes_marked
        for i in range(0, len(max_nodes)):
            if max_nodes[i] == 1:
                marked_nodes.append(self._nodes[i]._id)

    def compute_shortest_paths(self, start_node_id):
        """Compute the shortest paths for a given start node.

        Compute the shortest paths from the given start node
        using Dijkstra's algorithm.

        calculate the cost of all shortest paths from a given node
        to all reachable nodes.
        start at start node, look at arcs, store costs and
        traceback arc
        -> uses a priority queue to store node id and dist
        key = dist, value = node

        returns list [][]: node id, distance
        """
        output = []
        heap = []
        currentnodes = []
        currentnodes.append(start_node_id)
        # lastcost = 0
        heapq.heappush(heap, (0, start_node_id))
        # settled = [start_node_id]
        settled = []
        # repeat until no nodes unsettled
        while(len(currentnodes) > 0):
            nextnodes = []
            # for every node in the current step
            for n in currentnodes:
                # get the arcs leaving from current node
                # (they have current node as tail)
                # make a copy to pop
                t_arclst = self._adjacency_lists[n][:]
                while len(t_arclst) > 0:
                    # extract a single arc
                    t_arc = t_arclst.pop()
                    t_h_node = self.getNode(t_arc.head_node_id)
                    # continue with next arc when head is already settled
                    if t_arc.head_node_id in settled:
                        continue
                    # save the traceback arc for the head node
                    t_h_node.setTracebackArc(t_arc)
                    # calculate costs until current node with traceback arcs
                    lastcost = 0
                    while (t_h_node.getTracebackArc() is not None):
                        lastcost += t_h_node.getTracebackArc().costs
                        t_h_node = self.getNode(
                                        t_h_node._traceback_arc.tail_node_id)
                    # push head node with its cost into heap
                    heapq.heappush(heap, (lastcost, t_arc.head_node_id))
                    # check node in next step
                    nextnodes.append(t_arc.head_node_id)
                # set nodes for next cycle
                # pop the node with the shortest path, set it as settled,
                # save the cost value of the node, append node to output
                if len(heap) > 0:
                    t_element = heapq.heappop(heap)
                    if t_element[1] in settled:
                        continue
                    settled.append(t_element[1])
                    output.append(t_element)
            currentnodes = nextnodes
        return(output)

    def getPath(self, nodeid):
        """returns the arcs and costs to get to a destination
        start at destination, save traceback arcs (false order!)
        """
        t_node = self.getNode(nodeid)
        output = []
        while (t_node.getTracebackArc() is not None):
            output.append(t_node.getTracebackArc())
            t_node = self.getNode(t_node._traceback_arc.tail_node_id)
        return output

    def __repr__(self):
        """ Define object's string representation.

        >>> graph = Graph()
        >>> graph.read_graph_from_file("test.graph")
        >>> graph
        [0->1(30), 0->2(70), 1->2(20), 2->3(50), 3->1(40), 4->3(20)]
        """
        obj_str_repr = ""
        for i in range(self._num_nodes):
            for arc in self._adjacency_lists[i]:
                obj_str_repr += repr(arc) + ", "
        if obj_str_repr:
            return "[" + obj_str_repr[:-2] + "]"
        else:
            return "[]"


class Node:

    def __init__(self, node_id, latitude, longitude):
        self._id = node_id
        self._latitude = latitude
        self._longitude = longitude
        self._traceback_arc = None

    def __repr__(self):
        """ Define object's string representation."""
        return "%i" % (self._id)

    def setTracebackArc(self, traceback_arc):
        """ Set traceback arc to find way back
        stores the edge that was used to calculate the lowest costs
        for this particular node
        """
        self._traceback_arc = traceback_arc

    def getTracebackArc(self):
        """ return the traceback arc
        """
        return self._traceback_arc

    def getLatitude(self):
        return self._latitude

    def getLongitude(self):
        return self._longitude


class Arc:

    def __init__(self, tail_id, head_id, distance, max_speed):
        self.tail_node_id = tail_id  # ID of tail node.
        self.head_node_id = head_id  # ID of head node.
        self.distance = distance  # Distance in meter.
        self.max_speed = max_speed  # Maximum speed.
        self.costs = distance  # Set default costs to distance.

    def __repr__(self):
        """ Define object's string representation."""
        return "%i->%i(%i)" % (self.tail_node_id, self.head_node_id,
                               self.costs)

# if __name__ == "__main__":
#     g = Graph()
#     g.read_graph_from_file("test2.graph")
#     # print(g.getNode(2))
#     markedNodes = []
#     g.compute_lcc(markedNodes)
#     # print(markedNodes)
#     print(g.compute_shortest_paths(2))
