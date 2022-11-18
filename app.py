import math
import random

global n
global n_drivers


def calc_total_distance(drivers_route, object_f):
    distance = 0
    for d in drivers_route:
        distance += object_f(d)
    return distance


def generate_city(n):
    demand = [0]
    city_map = [(random.randint(1, 5000), random.randint(1, 5000))]  # bázis
    for i in range(1, n + 1):
        loc_x = random.randint(1, 5000)
        loc_y = random.randint(1, 5000)
        city_map.append((loc_x, loc_y))
        demand.append(random.randint(1, 5))
    return city_map, demand


def calc_city_distances(base, cities):
    cdist = []
    for city in cities:
        cdist.append(distance(base, city))
    return cdist


def distance(c1, c2):
    return abs((c1[0] - c2[0])) + abs((c1[1] - c2[1]))


def transform_tsp(tsp):
    tsp_dict = {}
    for i in range(len(tsp)):
        for j in range(len(tsp)):
            tsp_dict[(i, j)] = distance(tsp[i], tsp[j])
    return tsp_dict


def object_function(distances_dict, s):
    dist = 0
    prev = s[0]
    for i in s:
        dist += distances_dict[(prev, i)]
        prev = i
    dist += distances_dict[(s[-1], s[0])]
    return dist


def get_initial_route(cities, n, capacity, visited, demand):
    solution = [0]  # inicializalja a bazissal
    cdist = calc_city_distances(cities[0], cities)
    for _ in range(n):
        closest_index = math.inf
        distance = math.inf
        for j in range(len(cdist)):
            if cdist[j] < distance and cdist[j] != 0 and j not in visited and demand[j] <= capacity:
                closest_index = j
                distance = cdist[j]
        if closest_index == math.inf:
            if capacity != 0 and len(visited) != len(cities):
                capacity += 1
            else:
                solution.append(0)  # utolso lepeskent hozzateszi a bazis utat
                return solution
        else:
            solution.append(closest_index)
            visited.append(closest_index)
            capacity -= demand[closest_index]
            cdist = calc_city_distances(cities[closest_index], cities)
    return None


def search(route, object_f, demand, tabulist, tabulength):
    am = list()  # alternativ (nem jobb, de legkozelebb best-hez allo megoldas) csere adatait tarolo lista
    n_of_alternates = 0
    counter = 0
    retries = 3
    route_base = list(route)
    best_dist = calc_total_distance(route, object_f)
    while True:
        e = random.randint(0, len(route_base) - 1)
        q = random.randint(0, len(route_base) - 1)
        if e == q:
            continue
        s1_base = list(route_base[e])
        s2_base = list(route_base[q])
        a = random.randint(1, len(s1_base) - 2)
        b = random.randint(1, len(s2_base) - 2)
        if demand[s1_base[a]] != demand[s2_base[b]]:
            continue
        s1_base[a], s2_base[b] = s2_base[b], s1_base[a]
        route_base[e] = s1_base
        route_base[q] = s2_base
        swapped_dist = calc_total_distance(route_base, object_f)
        if best_dist > swapped_dist and s1_base not in tabulist and s2_base not in tabulist:
            print("Found better solution")
            counter = 0
            n_of_alternates = 0
            retries = 5
            tabulist.insert(0, route_base[e])
            tabulist.insert(0, route_base[q])
            if len(tabulist) > tabulength:
                tabulist.pop(len(tabulist) - 1)
                tabulist.pop(len(tabulist) - 1)
            route = list(route_base)
            best_dist = swapped_dist
            print("new:", best_dist)
            if len(am) != 0:
                am.pop(0)
        else:
            if len(am) == 0 and s1_base not in tabulist and s2_base not in tabulist:
                am.append([a, b, e, q, swapped_dist])
            elif len(am) != 0 and am[0][4] > swapped_dist and s1_base not in tabulist \
                    and s2_base not in tabulist:
                am.insert(0, [a, b, e, q, swapped_dist])
                am.pop(1)
            s1_tried = s1_base
            s2_tried = s2_base
            s1_base[a], s2_base[b] = s2_base[b], s1_base[a]
            route_base[e] = s1_base
            route_base[q] = s2_base
            counter += 1
            if counter == 50000:
                n_of_alternates += 1
                if n_of_alternates == 3:
                    print("too many base swaps, going back to best")
                    route_base = list(route)
                    #best_dist = calc_total_distance(route, object_f)
                    #print(best_dist)
                    #swapped_dist = calc_total_distance(route_base, object_f)
                    #print(swapped_dist)
                    print("original:", best_dist)
                    n_of_alternates = 0
                    counter = 0
                    retries -= 1
                    if retries == 0:
                        return route
                else:
                    print("using alternate route because I cant find a better route")
                    route_base[am[0][2]][am[0][0]], route_base[am[0][3]][am[0][1]] = \
                        route_base[am[0][3]][am[0][1]], route_base[am[0][2]][am[0][0]]
                    am.pop(0)
                    swapped_dist = calc_total_distance(route_base, object_f)
                    tabulist.insert(0, s1_tried)
                    tabulist.insert(0, s2_tried)
                    if len(tabulist) > tabulength:
                        tabulist.pop(len(tabulist) - 1)
                        tabulist.pop(len(tabulist) - 1)
                    counter = 0
                    print("new base:", swapped_dist)



def summarize(n_drivers, route, object_f):
    distance = 0
    for r in range(n_drivers):
        distance += object_f(route[r])
    for b in range(n_drivers):
        print("route for driver", b, ":", route[b])
        print("distance for driver", b, ":", object_f(route[b]), "m")
    print("total distance:", distance, "m")


def main():
    n = 500
    n_drivers = 10
    tabulength = 10
    random.seed(35142)
    object_f = lambda sched: object_function(tsp_dict, sched)
    tabulist = []
    visited = [0]
    driver_capacities = []
    route = []
    city_map, demand = generate_city(n)
    demandsum = sum(demand)
    tsp_dict = transform_tsp(city_map)
    for b in range(n_drivers):
        if demandsum % n_drivers != 0:
            if b == 0:
                driver_capacities.append(math.floor(demandsum / n_drivers) + demandsum % n_drivers)
                route.append(get_initial_route(city_map, n, driver_capacities[b], visited, demand))
            else:
                driver_capacities.append(math.floor(demandsum / n_drivers))
                route.append(get_initial_route(city_map, n, driver_capacities[b], visited, demand))
        else:
            driver_capacities.append(math.floor(demandsum / n_drivers))
            route.append(get_initial_route(city_map, n, driver_capacities[b], visited, demand))
    summarize(n_drivers, route, object_f)
    route = search(route, object_f, demand, tabulist, tabulength)
    summarize(n_drivers, route, object_f)


main()
