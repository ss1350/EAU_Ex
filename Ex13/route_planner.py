import graph
from math import floor


def secToTime(seconds):
    """
    umrechnen in Zeitstring
    """
    minutes = floor(seconds / 60)
    seconds = seconds % 60
    hours = floor(minutes / 60)
    minutes = minutes % 60
    s = str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"
    return s


def mapBBCode(graph, path, dest_node_id, color, label):
    """erstellt mapBB code für dest. Node id
    """
    configstring = "(" + color + "|" + label + ")"
    completestring = ""
    while (True):
        a = path.pop()
        nid = a[1]
        n = graph.getNode(nid)
        completestring += str(n.getLatitude()) + "," + str(n.getLongitude())
        if len(path) == 0:
            completestring = completestring + configstring
            break
        else:
            completestring = completestring + " "
    return completestring


if __name__ == "__main__":
    """calculates on the Graph bawue_bayern.graph
    1. the shortest path
    2. the fastest traveling time by car (max. speed 130 km/h)
    3. the fastest traveling time by tuned moped (max. speed 100 km/h)
    between the Faculty of Engineering (node ID 5508637) and the
    central railway station of Nürnberg (node ID 4435496)

    output from compute_shortest_path:
    output[][] (cost, nodeid)
    """
    g = graph.Graph()
    print("reading data")
    g.read_graph_from_file("bawue_bayern.graph")
    # g.read_graph_from_file("test.graph")
    print("Data successfully read")
    # shortest path (default)
    g.set_arc_costs_to_distance
    graph_shortest_path = g.compute_shortest_paths(5508637)
    shortest_path = g.getPath(4435496)
    # graph_shortest_path = g.compute_shortest_paths(4)
    # shortest_path = g.getPath(1)
    overall_cost = 0
    while(True):
        if len(shortest_path) == 0:
            break
        a = shortest_path.pop()
        if a is None:
            break
        overall_cost += a.costs
    print("Shortest Path regarding distance: ", overall_cost)

    # fastest traveling time by car
    g.set_arc_costs_to_travel_time(130)
    graph_time_car = g.compute_shortest_paths(5508637)
    # graph_time_car = g.compute_shortest_paths(4)
    # find furthest away
    sortiert = sorted(graph_time_car, key=lambda a: a[0])
    print("Groesste travel Time für Auto: Node " +
          str(sortiert[len(sortiert) - 1][1]) +
          " mit Zeit = " + secToTime(sortiert[len(sortiert) - 1][0]))

    for i in range(len(graph_time_car)):
        if graph_time_car[i][1] == 5508637:
            # if graph_time_car[i][1] == 1:
            print("Weg zu Node Id " + str(graph_time_car[i][1]) +
                  " benoetigte Zeit mit Auto: " +
                  secToTime(graph_time_car[i][0]))

    # fastest traveling time by moped
    g.set_arc_costs_to_travel_time(100)
    graph_time_moped = g.compute_shortest_paths(5508637)
    # graph_time_moped = g.compute_shortest_paths(4)
    # find furthest away
    sortiert1 = sorted(graph_time_moped, key=lambda a: a[0])
    print("Groesste travel Time für Moped: Node " +
          str(sortiert1[len(sortiert1) - 1][1]) +
          " mit Zeit = " + secToTime((sortiert1[len(sortiert1) - 1][0])))

    for i in range(len(graph_time_moped)):
        if graph_time_moped[i][1] == 5508637:
            # if graph_time_moped[i][1] == 1:
            print("Weg zu Node Id " + str(graph_time_moped[i][1]) +
                  " benoetigte Zeit mit Moped: " +
                  secToTime(graph_time_moped[i][0]))
    # mapBB ausgeben
    print("[map]" + mapBBCode(
            g, graph_time_car, sortiert[len(sortiert) - 1][1], "blue", "car") +
          ";" + "\n" +
          mapBBCode(
            g, graph_time_moped, sortiert1[len(sortiert1) - 1][1], "red",
            "moped") + "[\map]")
