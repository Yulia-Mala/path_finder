from copy import deepcopy
from multiprocessing import Lock, Value

from city_path import City, Path


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
        self.values_list = sorted([city.value for city in self.cities_instances.values()], reverse=True)

    def _set_location(self, city_name: str) -> City:
        for city in self.cities_instances.values():
            if city.name == city_name:
                return city
        else:
            raise ValueError(f"You've set {city_name} in parameters."
                             "But there is no such a city!")

    def _complete_path(self, path: Path, lock: Lock, value: Value):
        if value.value > self.best_value:
            self.best_value = value.value
            self.result_list.clear()
        if self.best_value > value.value:
            with lock:
                value.value = self.best_value
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
        values = path.values_list[:remaining_time]
        potential_value = path.current_value + sum(values)
        return self.best_value > potential_value

    def _get_from_pool(self, path: Path) -> Path:
        copy_path = self.path_pool.pop()
        copy_path.current_time = path.current_time
        copy_path.start = path.start
        copy_path.current_value = path.current_value
        copy_path.points = path.points.copy()
        copy_path.values_list = path.values_list.copy()
        return copy_path

    def _cyclic_traversal(self, city: City, path: Path, lock: Lock, value: Value):
        for next_city in city.connections:
            if path.is_available_to_visit(next_city=next_city):

                copy_path = (deepcopy(path)
                             if not self.path_pool
                             else self._get_from_pool(path))
                self._recursive_visit(path=copy_path, city=next_city, lock=lock, value=value)

            copy_path = (deepcopy(path)
                         if not self.path_pool
                         else self._get_from_pool(path))
            self._recursive_transit(path=copy_path, city=next_city, lock=lock, value=value)
        self._set_to_pool(path)

    def _set_to_pool(self, path: Path) -> None:
        path.__dict__.clear()
        self.path_pool.append(path)

    def _recursive_visit(self, path: Path, city: City, lock: Lock, value: Value) -> None:
        path.add_point(city=city, visit=True)
        if self.is_bound_to_fail(path=path):
            self._set_to_pool(path)
            return
        if city is self.end_city or path.current_time > self.time_limit - 1:
            # мінус 1, бо якщо у нас лишиться 1 час, то ми  зможемо лише  доїхати але не отримати бали
            self._complete_path(path, lock=lock, value=value)
            return
        self._cyclic_traversal(city=city, path=path, lock=lock, value=value)

    def _recursive_transit(self, path: Path, city: City, lock: Lock, value: Value) -> None:
        path.add_point(city=city, visit=False)
        if self.is_bound_to_fail(path=path):
            self._set_to_pool(path)
            return
        if path.current_time > self.time_limit - 1:
            # мінус 1, бо якщо у нас лишиться 1 час, то ми  зможемо лише  доїхати але не отримати бали
            self._complete_path(path, lock=lock, value=value)
            return
        self._cyclic_traversal(city=city, path=path, lock=lock, value=value)

    def transit_wrapper(self, next_city, lock, value):
        empty_path = Path(start=self.start_city, values=self.values_list)
        self._recursive_transit(path=empty_path, city=next_city, lock=lock, value=value)
        return self.result_list

    def visit_wrapper(self, next_city, lock, value):
        empty_path = Path(start=self.start_city, values=self.values_list)
        if empty_path.is_available_to_visit(next_city=next_city):
            self._recursive_visit(path=empty_path, city=next_city, lock=lock, value=value)
        return self.result_list
