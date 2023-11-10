import pandas as pd
import json
from datetime import datetime

# Definovanie ciest k súborom
TRANSACTIONS_FILE_PATH = 'data/realistic_transactions.json'
LOAN_DETAILS_FILE_PATH = 'data/loan_details.json'

def load_transactions(file_path=TRANSACTIONS_FILE_PATH):
    with open(file_path, 'r') as file:
        transactions = json.load(file)
    return analyze_expenses(transactions)


def analyze_expenses(transactions):
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Group by customer_id and calculate monthly expenses
    monthly_expenses = df[df['amount'] < 0].groupby('customer_id').resample('M').sum()

    # Convert Timestamps to strings and handle the tuples
    monthly_expenses_dict = {}
    for (customer_id, date), expenses in monthly_expenses.iterrows():
        month_str = date.strftime('%Y-%m')
        if customer_id not in monthly_expenses_dict:
            monthly_expenses_dict[customer_id] = {}
        monthly_expenses_dict[customer_id][month_str] = -expenses['amount']

    return monthly_expenses_dict


def load_loan_details(file_path=LOAN_DETAILS_FILE_PATH):
    with open(file_path, 'r') as file:
        loan_details = json.load(file)
    # Convert list of dicts to dict with customer_id as key
    loan_details_dict = {item['customer_id']: item for item in loan_details}
    return loan_details_dict


def calculate_repayment_plan(monthly_expenses, loan_details_dict):
    repayment_plans = {}
    for customer_id, expenses in monthly_expenses.items():
        if customer_id in loan_details_dict:
            loan_details = loan_details_dict[customer_id]
            loan_amount = loan_details['loan_amount']
            annual_interest_rate = loan_details['annual_interest_rate']
            loan_term_years = loan_details['loan_term_years']

            monthly_rate = annual_interest_rate / 12 / 100
            total_payments = loan_term_years * 12
            basic_monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -total_payments)

            # Calculate the max_expense for the customer
            max_expense = max(expenses.values(), default=0)

            for month, expense in expenses.items():
                # Ensure expense is a number, not a sequence
                if isinstance(expense, (int, float)):
                    # Adjust the payment based on the expense
                    adjusted_payment = max(0, basic_monthly_payment - (expense / max_expense * basic_monthly_payment * 0.25))
                    if customer_id not in repayment_plans:
                        repayment_plans[customer_id] = {}
                    repayment_plans[customer_id][month] = adjusted_payment
                else:
                    print(f"Invalid expense data for customer {customer_id}, month {month}")

    return repayment_plans


