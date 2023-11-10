import pandas as pd
import numpy as np
from datetime import datetime

def generate_realistic_transactions(num_customers, transactions_per_month, category_mean_amounts, start_date, end_date, min_balance_for_loan):
    transactions = []
    dates = pd.date_range(start_date, end_date, freq='M')  # Monthly transactions

    for customer_id in range(num_customers):
        customer_profile = generate_customer_profile(customer_id)
        income_data = generate_monthly_income(customer_profile, dates)

        for transaction_date in dates:
            balance = 0  # Starting balance for the month

            # Record income as a positive transaction
            monthly_income = income_data[transaction_date]
            balance += monthly_income
            transactions.append({
                'customer_id': customer_id,
                'date': transaction_date.strftime('%Y-%m-%d'),
                'amount': round(monthly_income, 2),
                'category': 'income',
                'payment_type': 'income',
                'balance': round(balance, 2)
            })

            # Random gift money (twice per month)
            for _ in range(2):
                gift_amount = np.random.uniform(5, 20)  # Gift amount up to 20 euros
                balance += gift_amount
                transactions.append({
                    'customer_id': customer_id,
                    'date': transaction_date.strftime('%Y-%m-%d'),
                    'amount': round(gift_amount, 2),
                    'category': 'gift',
                    'payment_type': 'gift',
                    'balance': round(balance, 2)
                })

            # Generate expense transactions as negative amounts
            for _ in range(transactions_per_month):
                if balance > min_balance_for_loan:  # Ensure enough balance for loan payment
                    category = np.random.choice(list(category_mean_amounts.keys()))
                    min_amount = category_min_amounts[category]  # Set minimum amount for realism
                    max_amount = min(balance - min_balance_for_loan, category_mean_amounts[category])
                    amount = np.random.uniform(min_amount, max_amount)
                    balance -= amount
                    transactions.append({
                        'customer_id': customer_id,
                        'date': transaction_date.strftime('%Y-%m-%d'),
                        'amount': -round(amount, 2),
                        'category': category,
                        'payment_type': np.random.choice(['cash', 'credit_card', 'debit_card', 'online']),
                        'balance': round(balance, 2)
                    })

    return transactions

def generate_monthly_income(profile, dates):
    income = {}
    base_income = profile.get('income', 1000)
    for date in dates:
        if profile['occupation'] in ['student', 'self-employed']:
            fluctuation = np.random.uniform(-0.3, 0.3)
            income[date] = max(0, base_income + base_income * fluctuation)
        else:
            income[date] = base_income
    return income

def generate_customer_profile(customer_id):
    profiles = [
        {'education_level': 'bachelor', 'age': np.random.randint(18, 25), 'occupation': 'student', 'region': 'urban', 'income_stability': 'variable', 'savings': np.random.uniform(0, 500), 'income': 500},
        {'education_level': 'master', 'age': np.random.randint(25, 50), 'occupation': 'employed', 'region': 'suburban', 'income_stability': 'stable', 'savings': np.random.uniform(5000, 20000), 'income': 3000},
        {'education_level': 'high_school', 'age': np.random.randint(18, 60), 'occupation': 'unemployed', 'region': 'urban', 'income_stability': 'unstable', 'savings': np.random.uniform(0, 1000), 'income': 1000},
        {'education_level': 'high_school', 'age': np.random.randint(60, 80), 'occupation': 'retired', 'region': 'rural', 'income_stability': 'stable', 'savings': np.random.uniform(2000, 15000), 'income': 2000},
        {'education_level': 'bachelor', 'age': np.random.randint(18, 25), 'occupation': 'student', 'region': 'urban', 'income_stability': 'variable', 'savings': np.random.uniform(0, 500), 'income': 500}
    ]
    return profiles[customer_id % len(profiles)]



# Parameters and dataset generation
num_customers = 5
transactions_per_month = 15
min_balance_for_loan = 500  # Minimum balance required for loan payment
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 1, 1)
category_mean_amounts = {'groceries': 100, 'utilities': 150, 'dining': 50, 'shopping': 200, 'transport': 80}
category_min_amounts = {'groceries': 30, 'utilities': 50, 'dining': 10, 'shopping': 20, 'transport': 5}  # Minimum expenses

transactions_df = pd.DataFrame(generate_realistic_transactions(num_customers, transactions_per_month, category_mean_amounts, start_date, end_date, min_balance_for_loan))
output_path = 'data/realistic_transactions.json'
transactions_df.to_json(output_path, orient='records', date_format='iso')
print("Modified dataset with managed expenses and gifts generated and saved to:", output_path)
