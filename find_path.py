graph = {"London": ["Stockholm", "Constantinople", "Rome", "Moscow", "Marrakesh"],
         "Stockholm": ["London", "Moscow"],
         "Moscow": ["Constantinople", "Rome", "London", "Stockholm"],
         "Constantinople": ["Moscow", "Alexandria", "Rome", "London"],
         "Rome": ["Marrakesh", "Alexandria", "Constantinople", "Moscow", "London"],
         "Marrakesh": ["Rome", "London", "Lagos"],
         "Alexandria": ["Rome", "Constantinople", "Lagos", "Nairobi"],
         "Nairobi": ["Alexandria", "Lagos"],
         "Lagos": ["Marrakesh", "Alexandria", "Nairobi"]}

values = {city: value for city, value in zip(graph.keys(), [3, 1, 1, 3, 1, 3, 3, 1, 1])}
founded_path = {0: "No path"}


def check_stop(passed_time, earned_value, visited, time_limit):
    if passed_time >= time_limit:
        max_value = max(founded_path.keys())
        if earned_value > max_value:
            founded_path[earned_value] = " - ".join(visited)
            del founded_path[max_value]
        elif earned_value == max_value:
            founded_path[earned_value] += (" or " + " - ".join(visited))
        return True


def find_path(passed_time=0, earned_value=0, visited=None, time_limit=11):
    global founded_path
    if check_stop(passed_time, earned_value, visited, time_limit):
        return
    if visited is None:
        visited = ["London"]
    current_city = visited[-1]
    passed_time += 1        #додаємо час за сценарій
    earned_value += values[current_city]        #додаємо цінність за сценарій
    unvisited = sorted(list(set(graph[current_city]) - set(visited)))
    if not unvisited:
        return
    if check_stop(passed_time, earned_value, visited, time_limit):
        return
    for city in unvisited:
        visited.append(city)
        passed_time += 1        #додаємо час за подорож
        find_path(passed_time, earned_value, visited)
        visited.pop()
        passed_time -= 1


find_path()
total_value = sum([key for key in founded_path])
print(total_value)
pathes = founded_path[total_value].split(" or ")
for path in pathes:
    print(path)