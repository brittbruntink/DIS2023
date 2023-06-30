# DIS2023
Repository for the group assignment of the DIS course at Utrecht University

Payment Calculation Script README

The script payment.py compares actual routes with standard routes and calculates the payment amount for each driver based on the similarity between the routes. It then generates CSV files containing the payment information and calculates the amount to be deposited back to the bank with a penalty fee if there is remaining payment.

Usage:
1. Ensure you have the required input files:
   - actual.json: Contains the actual routes data.
   - standard.json: Contains the standard routes data.
2. Place the input files in the same directory as the script.
3. Run the script by executing the following command in the terminal:
   $ python3 payment.py
4. The script will generate CSV files in the 'results' directory, each containing the payment information for a set of actual routes.
5. The script will also display the amount to be deposited back to the bank and the corresponding penalty fee.

Note:
- Make sure you have Python installed on your system.
- The script uses the difflib library to calculate the similarity ratio between routes.

Authors:
- E. Lan
- A. van Weerden
- B.M. Bruntink

Date: 30-06-2023
