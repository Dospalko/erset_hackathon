import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

# Nastavenie parametrov pre generovanie datasetu
num_customers = 100  # Počet zákazníkov
transactions_per_customer = 50  # Počet transakcií na zákazníka
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 1, 1)

# Generovanie dátumov transakcií
dates = pd.date_range(start_date, end_date, freq='D')

# Funkcia pre generovanie realistických transakcií
def generate_realistic_transactions():
    transactions = []
    for _ in range(num_customers):
        income_stability = np.random.choice(['stable', 'variable', 'unstable'], p=[0.7, 0.2, 0.1])
        life_event = np.random.choice(['none', 'marriage', 'childbirth', 'retirement'], p=[0.9, 0.05, 0.03, 0.02])
        for _ in range(transactions_per_customer):
            category = np.random.choice(['groceries', 'utilities', 'dining', 'shopping', 'transport'])
            amount = np.random.normal(category_mean_amounts[category], 20)  # +/- 20 okolo priemeru
            transaction_date = pd.Timestamp(np.random.choice(dates))  # Konverzia na Pandas Timestamp
            transactions.append({
                'date': transaction_date.strftime('%Y-%m-%d'),
                'amount': max(1, round(amount, 2)),  # Minimálna suma 1 a zaokrúhlenie
                'category': category,
                'payment_type': np.random.choice(['cash', 'credit_card', 'debit_card', 'online']),
                'income_stability': income_stability,
                'life_event': life_event if transaction_date.month == 5 else 'none'  # Pridelenie životnej udalosti v máji
            })
    return transactions




# Priemerné sumy pre jednotlivé kategórie
category_mean_amounts = {
    'groceries': 50,  # Priemerná suma za nákup potravín
    'utilities': 100,  # Priemerná suma za služby
    'dining': 30,  # Priemerná suma za stravovanie
    'shopping': 80,  # Priemerná suma za nákupy
    'transport': 20   # Priemerná suma za dopravu
}

# Generovanie datasetu
transactions_df = pd.DataFrame(generate_realistic_transactions())

# Uloženie do JSON súboru
output_path = 'data/transactions.json'  # Prispôsobte cestu podľa potreby
transactions_df.to_json(output_path, orient='records', date_format='iso')

print("Realistic dataset generated and saved to:", output_path)
