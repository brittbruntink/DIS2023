# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:48:20 2023

@author: britt
"""

import json
import random


def main():
    cities = ['Utrecht', 'Amsterdam', 'The Hague', 'Almere', 'Arnhem',
          'Rotterdam', 'Tilburg', 'Groningen', 'Breda', 'Nijmegen']

    merchandise = ['milk', 'honey', 'butter', 'tomatoes', 'pens', 'bread',
                   'cheese', 'coffee', 'tea', 'chocolate']
    
    
    # Generate random actual routes based on standard routes with variations
    def generate_actual_routes_from_standard(standard_routes, num_actual_routes):
        actual_routes = []
        num_standard_routes = len(standard_routes)
        num_standard_routes_in_actual = max(1, int(num_standard_routes * 0.1))
    
        # # Include 10% of the standard routes in actual routes
        # for i in range(num_standard_routes_in_actual):
        #     standard_route = standard_routes[i].copy()
        #     standard_route['id'] = i + 1
        #     actual_routes.append(standard_route)
    
        # Generate additional actual routes
        num_additional_routes = num_actual_routes - num_standard_routes_in_actual
        for i in range(num_additional_routes):
            route = []
    
            # Select a random standard route as a starting point
            standard_route = random.choice(standard_routes)
    
            # Retrieve information from the standard route
            from_city = standard_route['route'][0]['from']
            to_city = standard_route['route'][-1]['to']
            merchandise_dict = standard_route['route'][0]['merchandise'].copy()
    
            # Add or omit cities
            num_extra_cities = random.randint(0, 1)
            for _ in range(num_extra_cities):
                extra_city = random.choice(cities)
                while extra_city == from_city:
                    extra_city = random.choice(cities)
    
                # Add an item for the extra city
                extra_item = random.choice(merchandise)
                quantity = random.randint(1, 10)
                merchandise_dict[extra_item] = quantity
    
                route.append({'from': from_city, 'to': extra_city, 'merchandise': merchandise_dict})
                from_city = extra_city
    
            # Add the final trip to the destination city
            route.append({'from': from_city, 'to': to_city, 'merchandise': merchandise_dict})
    
            # Add the route to the actual routes list
            actual_route = {'id': i + num_standard_routes_in_actual + 1, 'route': route}
            actual_routes.append(actual_route)
    
        return actual_routes
    
    
    # Generate random standard routes
    def generate_standard_routes(num_routes):
        standard_routes = []
        for i in range(num_routes):
            route = []
            num_trips = random.randint(1, 5)
            from_city = random.choice(cities)
            for j in range(num_trips):
                to_city = random.choice(cities)
                while from_city == to_city:
                    to_city = random.choice(cities)
                merchandise_dict = {}
                num_merchandise = random.randint(1, len(merchandise))
                for _ in range(num_merchandise):
                    item = random.choice(merchandise)
                    quantity = random.randint(1, 10)
                    merchandise_dict[item] = quantity
                route.append({'from': from_city, 'to': to_city, 'merchandise': merchandise_dict})
                from_city = to_city
            standard_route = {'id': i + 1, 'route': route}
            standard_routes.append(standard_route)
    
        return standard_routes
    
    
    # Generate random standard routes
    num_standard_routes = 100  # Specify the desired quantity of standard routes
    standard_routes = generate_standard_routes(num_standard_routes)
    
    # Save standard routes to JSON file
    with open('standard.json', 'w') as file:
        json.dump(standard_routes, file, indent=4)
    
    
    # Generate actual routes JSON file based on standard routes
    num_actual_routes = 1000  # Specify the desired quantity of actual routes
    actual_routes = generate_actual_routes_from_standard(standard_routes, num_actual_routes)
    

    # Save actual routes to JSON file
    with open('actual.json', 'w') as file:
        json.dump(actual_routes, file, indent=4)
    
    

main()