from city_path import City


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

    @staticmethod
    def collect_results(future_results: list) -> list:
        result_list = []
        for result in future_results:
            for item in result.get():
                result_list.append(item)
        return result_list

    @staticmethod
    def clean_results(result_list: list) -> list:
        best_value = max([item.current_value for item in result_list])
        return [item for item in result_list if item.current_value == best_value]
