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
         "Buenos Aires": ["Rio de Janeiro"]}

values = {city: value for city, value in zip(graph.keys(), [3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3])}


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


def stop_and_save(value_now, time_limit, time_now, path_now, res_ls):
    if time_now >= time_limit:
        current_value = max(pair[0] for pair in res_ls)
        if value_now > current_value:
            res_ls.clear()
            res_ls.add((value_now, " ".join(path_now)))
        elif value_now == current_value:
            res_ls |= {(value_now, " ".join(path_now))}
        return True
    return False


def rec_transit(in_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now):
    time_now += 1
    path_now.append(f"--> {in_city} - Transit")
    if stop_and_save(value_now, time_limit, time_now, path_now, res_ls):
        return
    travel_options = connections[in_city]
    for i, next_city in enumerate(travel_options):
        rec_transit(next_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now)
        path_now.pop()
        if f"--> {next_city} {city_values[in_city]} Visit" not in path_now:
            rec_visit(next_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now)
            path_now.pop()


def rec_visit(in_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now):
    # додаємо час за подорож
    time_now += 1
    path_now.append(f"--> {in_city} {city_values[in_city]} Visit")
    if stop_and_save(value_now, time_limit, time_now, path_now, res_ls):
        return
    # додаємо час за сценарій
    time_now += 1
    value_now += city_values[in_city]
    travel_options = connections[in_city]
    if stop_and_save(value_now, time_limit, time_now, path_now, res_ls):
        return
    for i, next_city in enumerate(travel_options):
        rec_transit(next_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now)
        path_now.pop()
        if f"--> {next_city} {city_values[in_city]} Visit" not in path_now:
            rec_visit(next_city, connections, city_values, value_now, time_limit, time_now, res_ls, path_now)
            path_now.pop()


path_list = find_path(graph, values, time_limit=14, start="Buenos Aires")
for path in path_list:
    print(path)

print("--- %s seconds ---" % (time.time() - start_time))