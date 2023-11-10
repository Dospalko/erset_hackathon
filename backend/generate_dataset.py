import pandas as pd
import numpy as np
import json
from datetime import datetime

def generate_realistic_transactions(num_customers, transactions_per_month, category_mean_amounts, start_date, end_date):
    transactions = []
    dates = pd.date_range(start_date, end_date, freq='D')  # Daily transactions

    for customer_id in range(num_customers):
        customer_profile = generate_customer_profile(customer_id)
        life_events = generate_life_events(customer_id, dates)

        for transaction_date in dates:
            if np.random.rand() < 0.5:  # Randomly decide whether to generate a transaction for a given day
                category = np.random.choice(list(category_mean_amounts.keys()))
                amount = max(1, np.random.normal(category_mean_amounts[category], 20))
                life_event = life_events.get(transaction_date, 'none')

                transactions.append({
                    'customer_id': customer_id,
                    'date': transaction_date.strftime('%Y-%m-%d'),
                    'amount': round(amount, 2),
                    'category': category,
                    'payment_type': np.random.choice(['cash', 'credit_card', 'debit_card', 'online']),
                    'life_event': life_event,
                    **customer_profile
                })

    return transactions

def generate_customer_profile(customer_id):
    # Profiles for different customer types
    student = {'education_level': 'bachelor', 'age': np.random.randint(18, 25), 'occupation': 'student', 'region': 'urban', 'income_stability': 'variable', 'savings': np.random.uniform(0, 500)}
    working_professional = {'education_level': 'master', 'age': np.random.randint(25, 50), 'occupation': 'employed', 'region': 'suburban', 'income_stability': 'stable', 'savings': np.random.uniform(5000, 20000)}
    unemployed = {'education_level': 'high_school', 'age': np.random.randint(18, 60), 'occupation': 'unemployed', 'region': 'urban', 'income_stability': 'unstable', 'savings': np.random.uniform(0, 1000)}
    senior = {'education_level': 'high_school', 'age': np.random.randint(60, 80), 'occupation': 'retired', 'region': 'rural', 'income_stability': 'stable', 'savings': np.random.uniform(2000, 15000)}
    non_working_student = {'education_level': 'bachelor', 'age': np.random.randint(18, 25), 'occupation': 'student', 'region': 'urban', 'income_stability': 'variable', 'savings': np.random.uniform(0, 500)}

    profiles = [student, working_professional, unemployed, senior, non_working_student]
    return profiles[customer_id % len(profiles)]
def generate_life_events(customer_id, dates):
    life_events = {}
    # Randomly assign life events based on customer_id to avoid repetition
    if customer_id % 5 == 0:
        # Marriage in a random month
        marriage_date = np.random.choice(dates[dates.month == np.random.randint(1, 13)])
        life_events[marriage_date] = 'marriage'
    elif customer_id % 5 == 1:
        # Childbirth in a random month
        childbirth_date = np.random.choice(dates[dates.month == np.random.randint(1, 13)])
        life_events[childbirth_date] = 'childbirth'
    # ... Other life events logic for retirement, purchasing a house, etc.
    # Ensure not to assign multiple major events in the same year

    return life_events


# Nastavenie parametrov a generovanie datasetu
num_customers = 5
transactions_per_month = 30  # Average transactions per month
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 1, 1)
category_mean_amounts = {'groceries': 50, 'utilities': 100, 'dining': 30, 'shopping': 80, 'transport': 20}

transactions_df = pd.DataFrame(generate_realistic_transactions(num_customers, transactions_per_month, category_mean_amounts, start_date, end_date))
output_path = 'data/realistic_transactions.json'
transactions_df.to_json(output_path, orient='records', date_format='iso')
print("Realistic dataset generated and saved to:", output_path)
