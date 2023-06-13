# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 12:52:03 2023

@author: britt
"""
import json
from difflib import SequenceMatcher


# Function to calculate similarity ratio between two routes
def calculate_similarity(route1, route2):
    cities1 = [stop['from'] for stop in route1['route']]
    cities2 = [stop['from'] for stop in route2['route']]
    city_similarity = SequenceMatcher(None, cities1, cities2).ratio()

    merchandise1 = {item for stop in route1['route'] for item in stop['merchandise'].items()}
    merchandise2 = {item for stop in route2['route'] for item in stop['merchandise'].items()}
    merchandise_similarity = SequenceMatcher(None, list(merchandise1), list(merchandise2)).ratio()

    return (city_similarity + merchandise_similarity) / 2


# Read actual routes from actual.json
with open('actual.json', 'r') as file:
    actual_routes = json.load(file)

# Read standard routes from standard.json
with open('standard.json', 'r') as file:
    standard_routes = json.load(file)

# Create a dictionary to store the standard route for each actual route
route_mapping = {}

# Iterate over each actual route and find the most similar standard route
for actual_route in actual_routes:
    max_similarity = 0
    standard_route_match = None

    for standard_route in standard_routes:
        similarity = calculate_similarity(actual_route, standard_route)
        if similarity > max_similarity:
            max_similarity = similarity
            standard_route_match = standard_route

    if standard_route_match is not None:
        route_mapping[actual_route['id']] = standard_route_match['id']

    


# Function to calculate payment based on similarity
def calculate_payment(similarity):
    # Define the compensation range and the corresponding payment range
    payment = 1000 * similarity

    return payment


# Calculate the total payment available for the drivers
total_payment = 500000
remaining_payment = total_payment

# Calculate the payment for each driver
driver_payments = {}

for actual_id, standard_id in route_mapping.items():
    actual_route = next((route for route in actual_routes if route['id'] == actual_id), None)
    standard_route = next((route for route in standard_routes if route['id'] == standard_id), None)

    if actual_route and standard_route:
        similarity = calculate_similarity(actual_route, standard_route)
        payment = calculate_payment(similarity)

        # Reduce the remaining payment and check if it's sufficient to pay the driver
        if payment <= remaining_payment:
            driver_payments[actual_id] = payment, standard_id
            remaining_payment -= payment

# # Print the driver payments
for item in driver_payments:
    print("Driver for Actual Route", item, "which was most similar to Standard Route", driver_payments[item][1], "receives", driver_payments[item][0], "euros.")


# Calculate the amount to be deposited back to the bank
deposit_amount = remaining_payment

# Print the deposit amount and penalty fee
print(f"Amount to be deposited back to the bank: {deposit_amount} euros.")

