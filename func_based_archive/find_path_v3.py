import time
start_time = time.time()


graph = {"London": ["Stockholm", "Constantinople", "Rome", "Moscow", "Marrakesh", "Bermuda"],
         "Stockholm": ["London", "Moscow"],
         "Moscow": ["Constantinople", "Rome", "London", "Stockholm"],
         "Constantinople": ["Moscow", "Alexandria", "Rome", "London"],
         "Rome": ["Marrakesh", "Alexandria", "Constantinople", "Moscow", "London"],
         "Marrakesh": ["Rome", "London", "Lagos"],
         "Alexandria": ["Rome", "Constantinople", "Lagos", "Nairobi"],
         "Nairobi": ["Alexandria", "Lagos"],
         "Lagos": ["Marrakesh", "Alexandria", "Nairobi", "Rio de Janeiro"],
         "Bermuda": ["London", "Ybor City", "Anchorage"],
         "Ybor City": ["Bermuda", "Havana", "San Francisco"],
         "Havana": ["Ybor City", "San Francisco"],
         "Anchorage": ["Bermuda", "San Francisco"],
         "San Francisco": ["Anchorage", "Ybor City", "Tokyo", "Havana"],
         "Tokyo": ["San Francisco"],
         "Rio de Janeiro": ["Lagos", "Buenos Aires"],
         "Buenos Aires": ["Rio de Janeiro"],}


# values = {city: value for city, value in zip(graph.keys(), [3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3])}

values = {'London': 3, 'Stockholm': 1, 'Moscow': 1, 'Constantinople': 3,
          'Rome': 1, 'Marrakesh': 3, 'Alexandria': 3, 'Nairobi': 1, 'Lagos': 1,
          'Bermuda': 1, 'Ybor City': 3, 'Havana': 3, 'Anchorage': 1, 'San Francisco': 1,
          'Tokyo': 1, 'Rio de Janeiro': 1, 'Buenos Aires': 3}


def find_path(connections,  city_values, start="London", time_limit=5):
    value_now, time_now = city_values[start], 1
    res_ls = {(0, "No path")}
    travel_options = connections[start]
    for next_city in travel_options:
        rec_transit(next_city, connections, city_values, value_now,
                    time_limit, time_now, res_ls, path_now=[f"--> {start} {city_values[start]} Visit"])
        rec_visit(next_city, connections, city_values, value_now,
                  time_limit, time_now, res_ls, path_now=[f"--> {start} {city_values[start]} Visit"])
    return res_ls


def stop_and_save(value_now, path_now, res_set):
    current_value = max(pair[0] for pair in res_set)
    if value_now > current_value:
        res_set.clear()
        res_set.add((value_now, " ".join(path_now)))
    elif value_now == current_value:
        res_set |= {(value_now, " ".join(path_now))}


def is_bound_to_fail(city_values, value_now, time_limit, time_now, res_ls):
    max_num_of_futur_scen = (time_limit - time_now) // 2
    max_city_value = max(city_values.values())
    current_max_path_value = max(pair[0] for pair in res_ls)
    if max_city_value * max_num_of_futur_scen + value_now < current_max_path_value:
        return True
    return False


def rec_transit(in_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now):
    time_now += 1
    path_now.append(f"--> {in_city} - Transit")
    if time_now >= time_limit:
        stop_and_save(value_now, path_now, res_ls)
        return
    if is_bound_to_fail(city_values, value_now, time_limit, time_now, res_ls):
        return
    travel_options = connections[in_city]
    for next_city in travel_options:
        rec_transit(next_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now)
        path_now.pop()
        if f"--> {next_city} {city_values[next_city]} Visit" not in path_now:
            rec_visit(next_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now)
            path_now.pop()


def rec_visit(in_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now):
    # додаємо час за подорож
    time_now += 1
    path_now.append(f"--> {in_city} {city_values[in_city]} Visit")
    if time_now >= time_limit:
        stop_and_save(value_now, path_now, res_ls)
        return
    time_now += 1
    value_now += city_values[in_city]
    travel_options = connections[in_city]
    if is_bound_to_fail(city_values, value_now, time_limit, time_now, res_ls):
        return
    if time_now >= time_limit:
        stop_and_save(value_now, path_now, res_ls)
        return
    for next_city in travel_options:
        rec_transit(next_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now)
        path_now.pop()
        if f"--> {next_city} {city_values[next_city]} Visit" not in path_now:
            rec_visit(next_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now)
            path_now.pop()


path_list = find_path(graph, values, time_limit=14, start="Rome")
for path in path_list:
    print(path)

print("--- %s seconds ---" % (time.time() - start_time))

