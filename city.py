from __future__ import annotations

import time
from copy import deepcopy

from raw_data import (city_ident,
                      city_values,
                      my_graph,
                      location_access_time,
                      location_access_expr)

class City:
    def __init__(self,
                 name: str,
                 value: int,
                 ident: int,
                 connections_ids: list[int],
                 access_expr: str,
                 access_time: int):
        self.name = name
        self.value = value
        self.ident = ident
        self.connections_ids = connections_ids
        self.connections = None
        self.access_time = access_time
        self.access_expr = access_expr

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.ident == other.ident


    @classmethod
    def set_connections(cls, cities_dict: dict) -> None:
        for ident, city in cities_dict.items():
            city.connections = [nearby for ident, nearby in cities_dict.items()
                                if ident in city.connections_ids]


class PathPoint:
    def __init__(self, city: City, visit: bool):
        self.city = city
        self.visit = visit
        self.value = city.value if visit else 0


class Path:
    def __init__(self, start: City):
        self.current_time = 1
        self.start = start
        self.current_value = self.start.value
        self.points = []

    def __str__(self):
        result = ""
        for point in self.points:
            result += f"--> {point.city.name} {point.value} {'Visit' if point.visit else 'Transit'}"
        return result

    def __repr__(self):
        result = ""
        for point in self.points:
            result += f"--> {point.city.name} {point.value} {'Visit' if point.visit else 'Transit'}"
        return result

    def __len__(self):
        return len(self.points)

    def get_visited(self):
        return [point.city for point in self.points if point.visit]

    def is_available_to_visit(self, next_city: City) -> bool:
        """перевіряє чи доступна локація для візиту
        (задані умови + чи ще не відвідували її)"""
        not_visited = next_city not in self.get_visited()
        time_match = next_city.access_time <= self.current_time
        expressions_match = True
        if next_city.access_expr:
            expressions_match = eval(next_city.access_expr)
        return all([not_visited, time_match, expressions_match])

    def add_point(self, city: City, visit: bool) -> None:
        self.points.append(PathPoint(city=city, visit=visit))
        if visit:
            self.current_time += 2
            self.current_value += city.value
        else:
            self.current_time += 1


class RawDataHandler:
    def __init__(self,
                 city_ids: dict,
                 graph: dict,
                 values: dict,
                 access_time: dict,
                 access_expr: dict):
        self.city_ids = city_ids
        self.graph = graph
        self.values = values
        self.access_time = access_time
        self.access_expr = access_expr

    def get_cities_instances(self) -> dict:
        cities_dict = {}
        for city_name, city_id in self.city_ids.items():
            connections_names = self.graph[city_name]
            connections_ids = [self.city_ids[city] for city in connections_names]

            time_condition = (self.access_time[city_name]
                              if city_name in self.access_time else 0)
            other_condition = (self.access_expr[city_name]
                               if city_name in self.access_expr else None)
            city = City(
                name=city_name,
                value=self.values[city_name],
                ident=city_id,
                connections_ids=connections_ids,
                access_time=time_condition,
                access_expr=other_condition
            )
            cities_dict[city_id] = city

        City.set_connections(cities_dict=cities_dict)

        return cities_dict


class PathFinder:
    def __init__(self,
                 cities_instances: dict,
                 time_limit: int,
                 start_city_name: str,
                 end_city_name: str):
        self.time_limit = time_limit
        self.cities_instances = cities_instances
        self.start_city = self._set_location(start_city_name)
        self.end_city = self._set_location(end_city_name)
        self.result_list = []
        self.best_value = 0
        self.best_city_value = max(city.value for city in self.cities_instances.values())
        self.path_pool = []

    def _set_location(self, city_name: str) -> City:
        for city in self.cities_instances.values():
            if city.name == city_name:
                return city
        else:
            raise ValueError(f"You've set {city_name} in parameters."
                             "But there is no such a city!")

    def _complete_path(self, path: Path):
        if path.current_value > self.best_value:
            self.best_value = path.current_value
            self.result_list.clear()
            self.result_list.append(path)
        elif path.current_value == self.best_value:
            self.result_list.append(path)
        else:
            self._set_to_pool(path)

    def is_bound_to_fail(self, path: Path) -> bool:
        remaining_time = (self.time_limit - path.current_time) // 2
        potential_value = path.current_value + self.best_city_value * remaining_time
        return self.best_value > potential_value

    def _get_from_pool(self, path: Path) -> Path:
        copy_path = self.path_pool.pop()
        copy_path.current_time = path.current_time
        copy_path.start = path.start
        copy_path.current_value = path.current_value
        copy_path.points = path.points.copy()
        return copy_path

    def _cyclic_traversal(self, city: City, path: Path):
        for next_city in city.connections:
            if path.is_available_to_visit(next_city=next_city):

                copy_path = (deepcopy(path)
                             if not self.path_pool
                             else self._get_from_pool(path))
                self._recursive_visit(path=copy_path, city=next_city)

            copy_path = (deepcopy(path)
                         if not self.path_pool
                         else self._get_from_pool(path))
            self._recursive_transit(path=copy_path, city=next_city)
        self._set_to_pool(path)

    def _set_to_pool(self, path: Path) -> None:
        path.__dict__.clear()
        self.path_pool.append(path)

    def _recursive_visit(self, path: Path, city: City) -> None:
        path.add_point(city=city, visit=True)
        if self.is_bound_to_fail(path=path):
            self._set_to_pool(path)
            return
        if city is self.end_city or path.current_time > self.time_limit - 1:
            #мінус 1, бо якщо у нас лишиться 1 час, то ми  зможемо лише  доїхати але не отримати бали
            self._complete_path(path)
            return
        self._cyclic_traversal(city=city, path=path)

    def _recursive_transit(self, path: Path, city: City) -> None:
        path.add_point(city=city, visit=False)
        if self.is_bound_to_fail(path=path):
            self._set_to_pool(path)
            return
        if path.current_time > self.time_limit - 1:
            # мінус 1, бо якщо у нас лишиться 1 час, то ми  зможемо лише  доїхати але не отримати бали
            self._complete_path(path)
            return
        self._cyclic_traversal(city=city, path=path)

    def find_best_path(self):

            empty_path = Path(start=self.start_city)

            for next_city in self.start_city.connections:
                if empty_path.is_available_to_visit(next_city=next_city):
                    copy_path = deepcopy(empty_path)
                    self._recursive_visit(path=copy_path, city=next_city)
                copy_path = deepcopy(empty_path)
                self._recursive_transit(path=copy_path, city=next_city)

            return self.result_list



data_handler = RawDataHandler(city_ids=city_ident,
                              graph=my_graph,
                              values=city_values,
                              access_time=location_access_time,
                              access_expr= location_access_expr)

cities_list = data_handler.get_cities_instances()

path_finder = PathFinder(
    cities_instances=cities_list,
    time_limit=11,
    start_city_name="London",
    end_city_name="Tunguska"
)
start_time = time.time()

for rez in path_finder.find_best_path():
    print(rez.current_value, rez)

print("--- %s seconds ---" % (time.time() - start_time))
