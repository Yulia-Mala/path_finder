my_graph = {"London": ["Stockholm", "Constantinople", "Rome", "Moscow", "Marrakesh", "Bermuda", "Reykjavik"],
         "Stockholm": ["London", "Moscow", "Reykjavik"],
         "Moscow": ["Constantinople", "Rome", "London", "Stockholm", "Kabul", "Tunguska"],
         "Constantinople": ["Moscow", "Alexandria", "Rome", "London", "Kabul"],
         "Rome": ["Marrakesh", "Alexandria", "Constantinople", "Moscow", "London"],
         "Marrakesh": ["Rome", "London", "Lagos", "San Juan"],
         "Alexandria": ["Rome", "Constantinople", "Lagos", "Nairobi", "Bombay", "Kabul"],
         "Nairobi": ["Alexandria", "Lagos", "Perth"],
         "Lagos": ["Marrakesh", "Alexandria", "Nairobi", "Rio de Janeiro"],
         "Bermuda": ["London", "Ybor City", "Anchorage", "San Juan", "Bermuda Triangle"],
         "Ybor City": ["Bermuda", "Havana", "San Francisco", "Reykjavik", "San Juan"],
         "Havana": ["Ybor City", "San Francisco", "San Juan", "Quito"],
         "Anchorage": ["Bermuda", "San Francisco", "Reykjavik"],
         "San Francisco": ["Anchorage", "Ybor City", "Tokyo", "Havana"],
         "Tokyo": ["San Francisco", "Shanghai"],
         "Rio de Janeiro": ["Lagos", "Buenos Aires", "San Juan"],
         "Buenos Aires": ["Rio de Janeiro", "Sydney", "Quito"],
         "Shanghai": ["Tokyo", "Kathmandu", "Tunguska", "Hong Kong", "Manokwari"],
         "Kathmandu": ["Shanghai", "Bombay", "Kabul", "Tunguska", "Kuala Lumpur"],
         "Bombay": ["Kathmandu", "Alexandria", "Kabul", "Kuala Lumpur"],
         "Perth": ["Nairobi", "Sydney", "Kuala Lumpur"],
         "Sydney": ["Perth", "Buenos Aires", "Manokwari"],
         "Reykjavik": ["Anchorage", "Ybor City", "Stockholm", "London"],
         "San Juan": ["Havana", "Ybor City", "Bermuda", "Quito", "Rio de Janeiro", "Marrakesh", "Bermuda Triangle"],
         "Quito": ["San Juan", "Havana", "Buenos Aires", "Manokwari", "Bermuda Triangle"],
         "Kabul": ["Constantinople", "Moscow", "Alexandria", "Bombay", "Kathmandu", "Tunguska"],
         "Tunguska": ["Moscow", "Kabul", "Kathmandu", "Shanghai"],
         "Hong Kong": ["Shanghai", "Kuala Lumpur"],
         "Kuala Lumpur": ["Bombay", "Kathmandu", "Hong Kong", "Perth", "Manokwari"],
         "Manokwari": ["Kuala Lumpur", "Shanghai", "Quito", "Sydney"],
         "Bermuda Triangle": ["San Juan", "Quito", "Bermuda"]}

city_values = {'London': 1, 'Stockholm': 1, 'Moscow': 1, 'Constantinople': 3, 'Rome': 1, 'Marrakesh': 3,
          'Alexandria': 3, 'Nairobi': 1, 'Lagos': 1, 'Bermuda': 1, 'Ybor City': 1, 'Havana': 3, 'Anchorage': 3,
          'San Francisco': 1, 'Tokyo': 1, 'Rio de Janeiro': 1, 'Buenos Aires': 3, 'Shanghai': 1, 'Kathmandu': 1,
          'Bombay': 1, 'Perth': 1, 'Sydney': 1, 'Reykjavik': 1, 'San Juan': 1, 'Quito': 1, 'Kabul': 1,
          'Tunguska': 3, 'Hong Kong': 1, 'Kuala Lumpur': 3, 'Manokwari': 1, 'Bermuda Triangle': 3}

city_ident = {'London': 1, 'Stockholm': 2, 'Moscow': 3, 'Constantinople': 4, 'Rome': 5, 'Marrakesh': 6,
              'Alexandria': 7, 'Nairobi': 8, 'Lagos': 9, 'Bermuda': 10, 'Ybor City': 11, 'Havana': 12,
              'Anchorage': 13, 'San Francisco': 14, 'Tokyo': 15, 'Rio de Janeiro': 16, 'Buenos Aires': 17,
              'Shanghai': 18, 'Kathmandu': 19, 'Bombay': 20, 'Perth': 21, 'Sydney': 22, 'Reykjavik': 23,
              'San Juan': 24, 'Quito': 25, 'Kabul': 26, 'Tunguska': 27, 'Hong Kong': 28, 'Kuala Lumpur': 29,
              'Manokwari': 30, 'Bermuda Triangle': 31}


location_access_time = {"Tunguska": 14, "Kabul": 18, "Quito": 18, "San Juan": 18, "Reykjavik": 18}

location_access_expr = {"London": "'Sydney' in [point.city.name for point in self.points] and self.current_time < 22",
                            # "city_ident['Sydney'] + visit_const in path_id and time_now < 22",
                        "Kuala Lumpur": "'Hong Kong' in [point.city.name for point in self.points]",
                            # "city_ident['Hong Kong'] + visit_const in path_id",
                        "Hong Kong": "'Shanghai' in [point.city.name for point in self.points] and \
                                     self.__len__() - [point.city.name for point in self.points].index('Shanghai') > 4",
                        #     "city_ident['Shanghai'] + visit_const in path_id and\
                        # len(path_id) - path_id.index(city_ident['Shanghai'] + visit_const) > 4",
                        "Manokwari": "'Rio de Janeiro' in [point.city.name for point in self.points] and \
                                     'Perth' in [point.city.name for point in self.points] and \
                                      self.current_time < 22",
                        #     "city_ident['Rio de Janeiro'] + visit_const in path_id and \
                        # city_ident['Perth'] + visit_const in path_id and time_now < 22",
                        "Bermuda Triangle": "'Kathmandu' in [point.city.name for point in self.points] and \
                                     'London' in [point.city.name for point in self.points] and\
                                     'Rome' in [point.city.name for point in self.points] and self.current_time < 26"}
                        #     "city_ident['Kathmandu'] + visit_const in path_id and \
                        # city_ident['London'] + visit_const in path_id \
                        # and city_ident['Rome'] + visit_const in path_id and time_now < 26"}
