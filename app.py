import math
import random


def get_total_distance(route, object_f):
    sum = 0
    for a in range(len(route)):
        sum += object_f(route[a])
    return sum


def generate_city(cities, demand):
    loc_x = random.randint(1, 5000)
    loc_y = random.randint(1, 5000)
    cities.append((loc_x, loc_y))
    demand.append(random.randint(1, 5))


def get_city_distances(base, cities):
    cdist = []
    for j in range(len(cities)):
        cdist.append(distance(base, cities[j]))
    return cdist


def distance(c1, c2):
    return abs((c1[0] - c2[0])) + abs((c1[1] - c2[1]))


def transform_tsp(tsp):
    tsp_dict = {}
    for i in range(len(tsp)):
        for j in range(len(tsp)):
            tsp_dict[(i, j)] = distance(tsp[i], tsp[j])
    return tsp_dict


def object_function(dict, s):
    dist = 0
    prev = s[0]
    for i in s:
        dist += dict[(prev, i)]
        prev = i
    dist += dict[(s[-1], s[0])]
    return dist


def get_initial_route(cities, n, capacity, visited, demand):
    solution = [0]
    cdist = get_city_distances(cities[0], cities)
    for i in range(n):
        closestindex = 9999
        distance = 2000000
        for j in range(len(cdist)):
            if cdist[j] < distance and cdist[j] != 0 and j not in visited and demand[j] <= capacity:
                closestindex = j
                distance = cdist[j]
        if closestindex == 9999:
            solution.append(0)
            return solution
        else:
            solution.append(closestindex)
            visited.append(closestindex)
            capacity -= demand[closestindex]
            cdist = get_city_distances(cities[closestindex], cities)


def search(route, object_f, iterations, demand, tabulist, tabulength):
    am = list()
    layers = 0
    counter = 0
    route_base = list(route)
    fa = get_total_distance(route, object_f)
    for _ in range(1000):
        e = random.randint(0, len(route) - 1)
        q = random.randint(0, len(route) - 1)
        if e != q:
            s1_base = list(route_base[e])
            s2_base = list(route_base[q])
            for _ in range(iterations):
                a = random.randint(1, len(s1_base) - 2)
                b = random.randint(1, len(s2_base) - 2)
                if demand[s1_base[a]] != demand[s2_base[b]]:
                    continue
                s1_base[a], s2_base[b] = s2_base[b], s1_base[a]
                route_base[e] = s1_base
                route_base[q] = s2_base
                fa_neighbor = get_total_distance(route_base, object_f)
                if (fa - fa_neighbor) > 0 and s1_base not in tabulist and s2_base not in tabulist:
                    print("Found better solution")
                    counter = 0
                    layers = 0
                    tabulist.insert(0, route_base[e])
                    tabulist.insert(0, route_base[q])
                    if len(tabulist) > tabulength:
                        tabulist.pop(len(tabulist) - 1)
                        tabulist.pop(len(tabulist) - 1)
                    route = list(route_base)
                    fa = get_total_distance(route, object_f)
                    print("new:", fa)
                    if len(am) != 0:
                        am.pop(0)
                else:
                    counter += 1
                    s1_base[a], s2_base[b] = s2_base[b], s1_base[a]
                    if len(am) == 0:
                        am.append([a, b, e, q, fa_neighbor])
                    elif am[0][4] > fa_neighbor:
                        am.insert(0, [a, b, e, q, fa_neighbor])
                        am.pop(1)
                    if counter == 50000:
                        print("using alternate route because I cant find a better route")
                        layers += 1
                        route_base[am[0][2]][am[0][0]], route_base[am[0][3]][am[0][1]] =\
                            route_base[am[0][3]][am[0][1]], route_base[am[0][2]][am[0][0]]
                        counter = 0
                        fa_neighbor = get_total_distance(route_base, object_f)
                        print("new base:", fa_neighbor)
                        am.pop(0)
                        if layers == 3:
                            print("too many layers, going back to best")
                            route_base = list(route)
                            fa = get_total_distance(route_base, object_f)
                            print("original:", fa)
                            layers = 0
    return route


def summarize(drivers, route, object_f):
    summ = 0
    for r in range(drivers):
        summ += object_f(route[r])
    for b in range(drivers):
        print("route for driver", b, ":", route[b])
        print("distance for driver", b, ":", object_f(route[b]), "m")
    print("total distance:", summ, "m")


def main():
    random.seed(35142)
    object_f = lambda sched: object_function(tsp_dict, sched)
    n = 100
    tabulist = []
    tabulength = 6
    cities = [(random.randint(1, 5000), random.randint(1, 5000))]  # bázis
    demand = [0]
    visited = [0]
    drivers = 6
    driver_capacities = []
    route = []
    for i in range(1, n + 1):
        generate_city(cities, demand)
    demandsum = sum(demand)
    tsp_dict = transform_tsp(cities)
    for b in range(drivers):
        if demandsum % drivers != 0:
            if b == 0:
                driver_capacities.append(math.floor(demandsum / drivers) + demandsum % drivers)
                route.append(get_initial_route(cities, n, driver_capacities[b], visited, demand))
            else:
                driver_capacities.append(math.floor(demandsum / drivers))
                route.append(get_initial_route(cities, n, driver_capacities[b], visited, demand))
        else:
            driver_capacities.append(math.floor(demandsum / drivers))
            route.append(get_initial_route(cities, n, driver_capacities[b], visited, demand))
    summarize(drivers, route, object_f)
    route = search(route, object_f, 5000, demand, tabulist, tabulength)
    summarize(drivers, route, object_f)

main()
