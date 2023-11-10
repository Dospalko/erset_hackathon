import pandas as pd
import json
from datetime import datetime

# Definovanie ciest k súborom
TRANSACTIONS_FILE_PATH = 'data/transactions.json'
LOAN_DETAILS_FILE_PATH = 'data/loan_details.json'

def load_transactions(file_path=TRANSACTIONS_FILE_PATH):
    with open(file_path, 'r') as file:
        transactions = json.load(file)
    return analyze_expenses(transactions)

def analyze_expenses(transactions):
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    monthly_expenses = df.resample('M').sum()
    return {date.strftime('%Y-%m'): amount for date, amount in monthly_expenses['amount'].items()}

def load_loan_details(file_path=LOAN_DETAILS_FILE_PATH):
    with open(file_path, 'r') as file:
        loan_details = json.load(file)
    return loan_details

def calculate_repayment_plan(monthly_expenses, loan_details):
    loan_amount = loan_details['loan_amount']
    annual_interest_rate = loan_details['annual_interest_rate']
    loan_term_years = loan_details['loan_term_years']

    monthly_rate = annual_interest_rate / 12 / 100
    total_payments = loan_term_years * 12
    basic_monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -total_payments)

    max_expense = max(monthly_expenses.values())
    adjusted_payments = {month: max(0, basic_monthly_payment - (expense / max_expense * basic_monthly_payment * 0.25))
                         for month, expense in monthly_expenses.items()}

    return adjusted_payments
