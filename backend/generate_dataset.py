import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

# Nastavenie počtu generovaných transakcií
num_transactions = 500

# Generovanie datasetu
np.random.seed(0)  # Pre reprodukovateľnosť výsledkov
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 1, 1)

dates = pd.date_range(start_date, end_date, freq='D')
data = {
    'date': np.random.choice(dates, num_transactions),
    'amount': np.random.uniform(5, 200, num_transactions),
    'category': np.random.choice(['groceries', 'utilities', 'dining', 'shopping', 'transport'], num_transactions),
    'payment_type': np.random.choice(['cash', 'credit_card', 'debit_card', 'online'], num_transactions)
}

transactions_df = pd.DataFrame(data)
# Konverzia dátumu na reťazec pre JSON serializáciu
transactions_df['date'] = transactions_df['date'].dt.strftime('%Y-%m-%d')

# Uloženie do JSON súboru
output_path = 'data/transactions.json'  # Prispôsobte cestu podľa potreby
transactions_df.to_json(output_path, orient='records', date_format='iso')

output_path
