from datetime import datetime
import pandas as pd
import numpy as np
import random
import os
def generate_user_transactions(num_months, start_date, end_date, total_loan_amount, loan_duration_months, max_loan_fluctuation, loan_commission_rate):
    transactions = []
    dates = pd.date_range(start_date, end_date, freq='M')

    total_loan_with_commission = total_loan_amount * (1 + loan_commission_rate)
    base_monthly_loan_payment = total_loan_with_commission / loan_duration_months
    remaining_loan_balance = total_loan_with_commission
    base_expenses = 1800  # Estimated average of necessary expenses

    for transaction_date in dates:
        # Calculate income and base expenses
        monthly_income = 3000
        rent = 1200  # Necessary expense
        groceries = np.random.uniform(150, 350)  # Necessary expense
        necessary_expenses = rent + groceries

        # Unnecessary expenses
        fun = np.random.uniform(100, 400)
        alcohol = np.random.uniform(50, 200)
        netflix = 15
        unnecessary_expenses = fun + alcohol + netflix

        # Special events or seasonal variations
        special_event_expense = 0
        if transaction_date.month == 12:
            special_event_expense += np.random.uniform(300, 500)
        if random.random() < 0.1:
            special_event_expense += np.random.uniform(200, 400)
        unnecessary_expenses += special_event_expense
        # Total monthly expenses

        total_expenses = necessary_expenses + unnecessary_expenses
        expense_difference = total_expenses - base_expenses

        if expense_difference > expense_increase_threshold:
            necessary_expense_impact = necessary_expenses / total_expenses
            adjustment_factor = loan_reduction_rate * necessary_expense_impact + loan_reduction_rate * 0.5 * (
                        1 - necessary_expense_impact)
            adjusted_loan_payment = base_monthly_loan_payment * (1 - adjustment_factor)
        else:
            adjusted_loan_payment = base_monthly_loan_payment

        adjusted_loan_payment = min(adjusted_loan_payment, remaining_loan_balance)
        remaining_loan_balance -= adjusted_loan_payment

        transactions.append({
            'loan': total_loan_with_commission,
          #  'date': transaction_date.strftime('%Y-%m-%d'),
            'income': round(monthly_income, 2),
            'expenses': round(total_expenses, 2),
            'necessary_expenses': round(necessary_expenses, 2),
            'unnecessary_expenses': round(unnecessary_expenses, 2),
            'loan_payment': round(adjusted_loan_payment, 2)
        })

    return transactions


# Parameters for the dataset generation
num_months = 100
start_date = datetime(2022, 1, 1)
end_date = datetime(2029, 12, 31)
total_loan_amount = 30000
loan_duration_months = 100
expense_increase_threshold = 200  # Expense increase threshold for loan payment adjustment
loan_reduction_rate = 0.2  # Loan reduction rate when expense increase threshold is exceeded
loan_commission_rate = 0.05
max_loan_fluctuation = 0.2  # Max fluctuation of loan payment amount
# Generate the dataset
user_transactions_df = pd.DataFrame(generate_user_transactions(num_months, start_date, end_date, total_loan_amount, loan_duration_months, max_loan_fluctuation, loan_commission_rate))
total_loan_payments = user_transactions_df['loan_payment'].sum()
print(f"Total amount paid towards the loan: {total_loan_payments}")

# Save the dataframe to CSV
output_path = os.path.join('data', 'user_transactions.csv')
user_transactions_df.to_csv(output_path, index=False)