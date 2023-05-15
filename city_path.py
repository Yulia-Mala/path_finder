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
    def __init__(self, start: City, values: list):
        self.current_time = 1
        self.start = start
        self.current_value = self.start.value
        self.points = []
        self.values_list = values

    def __str__(self):
        result = ""
        for point in self.points:
            result += f"--> {point.city.name} {point.value} {'Visit' if point.visit else 'Transit'}"
        return f"{self.current_value} {result}"

    def __repr__(self):
        result = ""
        for point in self.points:
            result += f"--> {point.city.name} {point.value} {'Visit' if point.visit else 'Transit'}"
        return f"{self.current_value} {result}"

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
            self.values_list.remove(city.value)
        else:
            self.current_time += 1
