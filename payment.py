#!/usr/bin/env python
# File name: payment.py
# Authors: E. Lan, A. van Weerden, B.M. Bruntink 
# This code compares actual routes with standard routes and calculates the payment amount for each driver based on the similarity between the routes. It then generates CSV files containing the payment information and calculates the amount to be deposited back to the bank with a penalty fee if there is remaining payment.
# Date: 30-06-2023

import os
import csv
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
driver_payments = []

# Sort the actual routes based on descending similarity to the standard route
sorted_actual_routes = sorted(actual_routes, key=lambda route: calculate_similarity(route, standard_routes[0]), reverse=True)

payment_counter = 1
csv_directory = 'results'
os.makedirs(csv_directory, exist_ok=True)
csv_filename = f"{csv_directory}/actual_routes{payment_counter}.csv"

with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Actual Route ID', 'Standard Route ID', 'Payment Amount'])

    for actual_route in sorted_actual_routes:
        actual_id = actual_route['id']
        standard_id = route_mapping.get(actual_id)

        if standard_id:
            standard_route = next((route for route in standard_routes if route['id'] == standard_id), None)
            similarity = calculate_similarity(actual_route, standard_route)
            payment = calculate_payment(similarity)

            # Reduce the remaining payment and check if it's sufficient to pay the driver
            if payment <= remaining_payment:
                driver_payments.append((actual_route, standard_route, payment))
                writer.writerow([actual_id, standard_id, payment])
                remaining_payment -= payment
            else:
                break  # Stop further processing if there is not enough payment left

        if remaining_payment <= 0:
            # Close the current file and prepare for the next file
            file.close()

            # Calculate the amount to be deposited back to the bank
            deposit_amount = remaining_payment
            penalty_fee = deposit_amount * 0.05  # Assuming penalty fee is 5% of the deposit amount

            # Print the deposit amount and penalty fee
            print(f"Amount to be deposited back to the bank: {deposit_amount} euros.")
            print(f"Penalty fee: {penalty_fee} euros.")

            payment_counter += 1
            csv_filename = f"{csv_directory}/paymentfile{payment_counter}.csv"

            with open(csv_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Actual Route ID', 'Standard Route ID', 'Payment Amount'])

            remaining_payment = total_payment

# Calculate the amount to be deposited back to the bank
deposit_amount = remaining_payment
penalty_fee = deposit_amount * 0.05  # Assuming penalty fee is 5% of the deposit amount

# Print the deposit amount and penalty fee
print(f"Amount to be deposited back to the bank: {deposit_amount} euros.")
print(f"Penalty fee: {penalty_fee} euros.")

