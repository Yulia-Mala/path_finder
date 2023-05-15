from __future__ import annotations

import time
from multiprocessing import Pool, Manager

from data_handler import RawDataHandler
from path_finder import PathFinder
from raw_data import (city_ident,
                      city_values,
                      my_graph,
                      location_access_time,
                      location_access_expr)


if __name__ == "__main__":
    start_time = time.time()

    data_handler = RawDataHandler(
        city_ids=city_ident,
        graph=my_graph,
        values=city_values,
        access_time=location_access_time,
        access_expr=location_access_expr
    )
    finder = PathFinder(
        cities_instances=data_handler.get_cities_instances(),
        time_limit=27,
        start_city_name="London",
        end_city_name="Tunguska"
    )

    cities = finder.start_city.connections
    path_list = []

    with Manager() as manager:
        lock = manager.Lock()
        value = manager.Value(int, 0)

        with Pool() as pool:
            visit_results = [
                pool.apply_async(finder.visit_wrapper,
                                 args=(city, lock, value))
                for city in cities
            ]
            transit_results = [
                pool.apply_async(finder.transit_wrapper,
                                 args=(city, lock, value))
                for city in cities
            ]
            path_list.extend(data_handler.collect_results(visit_results))
            path_list.extend(data_handler.collect_results(transit_results))
            pool.close()
            pool.join()

    path_list = data_handler.clean_results(path_list)

    for path in path_list:
        print(path)

    print("--- %s seconds ---" % (time.time() - start_time))
