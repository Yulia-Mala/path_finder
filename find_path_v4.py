import time
from random import choice
start_time = time.time()

graph = {"London": ["Stockholm", "Constantinople", "Rome", "Moscow", "Marrakesh", "Bermuda", "Reykjavik"],
         "Stockholm": ["London", "Moscow", "Reykjavik"],
         "Moscow": ["Constantinople", "Rome", "London", "Stockholm", "Kabul", "Tunguska"],
         "Constantinople": ["Moscow", "Alexandria", "Rome", "London", "Kabul"],
         "Rome": ["Marrakesh", "Alexandria", "Constantinople", "Moscow", "London"],
         "Marrakesh": ["Rome", "London", "Lagos", "Sun Juan"],
         "Alexandria": ["Rome", "Constantinople", "Lagos", "Nairobi", "Bombay", "Kabul"],
         "Nairobi": ["Alexandria", "Lagos", "Perth"],
         "Lagos": ["Marrakesh", "Alexandria", "Nairobi", "Rio de Janeiro"],
         "Bermuda": ["London", "Ybor City", "Anchorage", "Sun Juan"],
         "Ybor City": ["Bermuda", "Havana", "San Francisco", "Reykjavik", "Sun Juan"],
         "Havana": ["Ybor City", "San Francisco", "Sun Juan", "Quito"],
         "Anchorage": ["Bermuda", "San Francisco", "Reykjavik"],
         "San Francisco": ["Anchorage", "Ybor City", "Tokyo", "Havana"],
         "Tokyo": ["San Francisco", "Shanghai"],
         "Rio de Janeiro": ["Lagos", "Buenos Aires", "Sun Juan"],
         "Buenos Aires": ["Rio de Janeiro", "Sydney", "Quito"],
         "Shanghai": ["Tokyo", "Kathmandu", "Tunguska", "Hong Kong"],
         "Kathmandu": ["Shanghai", "Bombay", "Kabul", "Tunguska"],
         "Bombay": ["Kathmandu", "Alexandria", "Kabul"],
         "Perth": ["Nairobi", "Sydney"],
         "Sydney": ["Perth", "Buenos Aires"],
         "Reykjavik": ["Anchorage", "Ybor City", "Stockholm", "London"],
         "Sun Juan": ["Havana", "Ybor City", "Bermuda", "Quito", "Rio de Janeiro", "Marrakesh"],
         "Quito": ["Sun Juan", "Havana", "Buenos Aires"],
         "Kabul": ["Constantinople", "Moscow", "Alexandria", "Bombay", "Kathmandu", "Tunguska"],
         "Tunguska": ["Moscow", "Kabul", "Kathmandu", "Shanghai"],
         "Hong Kong": ["Shanghai"]}

values = {'London': 5, 'Stockholm': 1, 'Moscow': 1, 'Constantinople': 5,
          'Rome': 1, 'Marrakesh': 5, 'Alexandria': 5, 'Nairobi': 1, 'Lagos': 1,
          'Bermuda': 1, 'Ybor City': 1, 'Havana': 5, 'Anchorage': 5, 'San Francisco': 1,
          'Tokyo': 1, 'Rio de Janeiro': 1, 'Buenos Aires': 5, 'Shanghai': 1,
          'Kathmandu': 1, 'Bombay': 1, 'Perth': 1, 'Sydney': 1, 'Reykjavik': 1,
          'Sun Juan': 1, 'Quito': 1, 'Kabul': 1, 'Tunguska': 5, 'Hong Kong': 1}

city_ident = {city: i for city, i in zip(graph.keys(), range(1, len(graph)+1))}
id_value_dict = {ident: value for ident, value in zip(city_ident.values(), values.values())}
location_access = {"Tunguska": 15, "Kabul": 20, "Quito": 20, "San Juan": 20, "Reykjavik": 20, "Hong Kong": 24}


def find_path(connections,  city_values, city_id, id_value, open_time, start="London", time_limit=5, visit_const=100):
    value_now, time_now = city_values[start], 1
    res_set = {(0, "No path")}
    travel_options = connections[start]
    path_id = [city_id[start] + visit_const]
    for next_city in travel_options:
        if open_time.get(next_city, time_now) <= time_now:
            rec_visit(next_city, connections, city_values, value_now, time_limit, time_now,
                      res_set, city_id, path_id, visit_const, id_value, open_time)
            path_id.pop()
        rec_transit(next_city, connections, city_values, value_now, time_limit, time_now,
                    res_set, city_id, path_id, visit_const, id_value, open_time)
        path_id.pop()
    return res_set


def stop_and_save(value_now, path_id, res_set, city_id, city_values, visit_const):
    current_value = choice(tuple(res_set))[0]
    if value_now >= current_value:
        path_now = ""
        id_city = {i: city for city, i in city_id.items()}
        for ident in path_id:
            if ident > visit_const:
                path_now += f"--> {id_city[ident-visit_const]} {city_values[id_city[ident-visit_const]]} Visit"
            else:
                path_now += f"--> {id_city[ident]} - Transit"
        if value_now > current_value:
            res_set.clear()
            res_set.add((value_now, path_now))
        elif value_now == current_value:
            res_set |= {(value_now, path_now)}


def is_bound_to_fail(value_now, time_limit, time_now, res_set, path_id, visit_const, id_value):
    max_num_of_futur_scen = (time_limit - time_now) // 2
    visited_id = [ident - visit_const for ident in path_id if ident > visit_const]
    not_visited_values = [id_value[ident] for ident in id_value.keys() if ident not in visited_id]
    max_future_value = sorted(not_visited_values, reverse=True)[:max_num_of_futur_scen]
    current_max_path_value = choice(tuple(res_set))[0]
    if sum(max_future_value) + value_now < current_max_path_value:
        return True
    return False


def rec_transit(in_city, connections, city_values, value_now, time_limit, time_now, res_set,
                city_id, path_id, visit_const, id_value, open_time):
    time_now += 1
    path_id.append(city_id[in_city])
    if time_now >= time_limit:
        stop_and_save(value_now, path_id, res_set, city_id, city_values, visit_const)
        return
    if is_bound_to_fail(value_now, time_limit, time_now, res_set, path_id, visit_const, id_value):
        return
    travel_options = connections[in_city]
    for next_city in travel_options:
        if city_id[next_city] + visit_const not in path_id and \
                open_time.get(next_city, time_now) <= time_now and time_limit - time_now > 1:
            rec_visit(next_city, connections, city_values, value_now, time_limit, time_now,
                      res_set, city_id, path_id, visit_const, id_value, open_time)
            path_id.pop()
        rec_transit(next_city, connections, city_values, value_now, time_limit, time_now,
                    res_set, city_id, path_id, visit_const, id_value, open_time)
        path_id.pop()


def rec_visit(in_city, connections, city_values, value_now, time_limit, time_now, res_set,
              city_id, path_id, visit_const, id_value, open_time):
    time_now += 2
    path_id.append(city_id[in_city] + visit_const)
    value_now += city_values[in_city]
    travel_options = connections[in_city]
    if is_bound_to_fail(value_now, time_limit, time_now, res_set, path_id, visit_const, id_value):
        return
    if time_now >= time_limit:
        stop_and_save(value_now, path_id, res_set, city_id, city_values, visit_const)
        return
    for next_city in travel_options:
        if city_id[next_city] + visit_const not in path_id and \
                open_time.get(next_city, time_now) <= time_now and time_limit - time_now > 1:
            rec_visit(next_city, connections, city_values, value_now, time_limit, time_now, res_set,
                      city_id, path_id, visit_const, id_value, open_time)
            path_id.pop()
        rec_transit(next_city, connections, city_values, value_now, time_limit, time_now, res_set,
                    city_id, path_id, visit_const, id_value, open_time)
        path_id.pop()


path_list = find_path(graph, values, city_id=city_ident,  id_value=id_value_dict,
                      time_limit=23, start="London", open_time=location_access)
for path in path_list:
    print(path)

print("--- %s seconds ---" % (time.time() - start_time))
