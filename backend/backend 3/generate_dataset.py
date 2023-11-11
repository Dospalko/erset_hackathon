from datetime import datetime
import pandas as pd
import numpy as np
import random
import os
def generate_user_transactions(num_months, total_loan_amount, loan_commission_rate):
    transactions = []
    #dates = pd.date_range(start_date, end_date, freq='M')
    remaining_months = num_months
    total_loan_with_commission = total_loan_amount * (1 + loan_commission_rate)
    base_monthly_loan_payment = total_loan_with_commission / num_months
    remaining_loan_balance = total_loan_with_commission
    monthly_income = np.random.uniform(1000, 10000)
    while(monthly_income*0.35 < base_monthly_loan_payment):
        monthly_income = np.random.uniform(1000, 10000)
    base_expenses = 0.65 * monthly_income  # Estimated average of necessary expenses
    rent = 0.55 * base_expenses  # Necessary expense
    while(remaining_months>0 and remaining_loan_balance>0):
        # Calculate income and base expenses
        groceries = np.random.uniform(0.12*base_expenses, 0.2*base_expenses)  # Necessary expense
        necessary_expenses = rent + groceries

        # Unnecessary expenses
        fun = np.random.uniform(0.06*base_expenses, 0.125*base_expenses)
        alcohol = np.random.uniform(0.042*base_expenses, 0.084*base_expenses)
        if random.random() < 0.3:
            netflix = 8
            unnecessary_expenses = fun + alcohol + netflix
        else:
            unnecessary_expenses = fun + alcohol 

        # Special events or seasonal variations
        special_event_expense = 0
        if random.random() < 0.1:
            special_event_expense += np.random.uniform(100, 400)
        unnecessary_expenses += special_event_expense
        # Total monthly expenses

        total_expenses = necessary_expenses + unnecessary_expenses
        expense_difference = total_expenses - base_expenses

        if expense_difference > 0:
            adjusted_loan_payment = base_monthly_loan_payment / (total_expenses/base_expenses)
            if(adjusted_loan_payment < base_monthly_loan_payment *(1- loan_reduction_rate)):
                adjusted_loan_payment = base_monthly_loan_payment *(1- loan_reduction_rate)
        else:
            adjusted_loan_payment = base_monthly_loan_payment / (total_expenses/base_expenses)
            if(adjusted_loan_payment > base_monthly_loan_payment *(1+ loan_reduction_rate)):
                adjusted_loan_payment = base_monthly_loan_payment *(1+ loan_reduction_rate)


        adjusted_loan_payment = min(adjusted_loan_payment, remaining_loan_balance)
        if(adjusted_loan_payment< (remaining_loan_balance/remaining_months) ):
            adjusted_loan_payment = remaining_loan_balance/remaining_months

        remaining_loan_balance -= adjusted_loan_payment
        remaining_months -=1
        transactions.append({
            'loan': total_loan_with_commission,
            'months': num_months,
          #  'date': transaction_date.strftime('%Y-%m-%d'),
            'income': round(monthly_income, 2),
            'expenses': round(total_expenses, 2),
            'necessary_expenses': round(necessary_expenses, 2),
            'unnecessary_expenses': round(unnecessary_expenses, 2),
            'loan_payment': round(adjusted_loan_payment, 2)
        })

    return transactions


# Parameters for the dataset generation
expense_increase_threshold = 200  # Expense increase threshold for loan payment adjustment
loan_reduction_rate = 0.2  # Loan reduction rate when expense increase threshold is exceeded
loan_commission_rate = 0.05

# Initialize a list to store DataFrames
transactions_list = []

for _ in range(50):
    # Randomly select the number of months and loan amount
    num_months = random.choice([12, 24, 36, 48, 60])
    total_loan_amount = random.randint(15, 400) * 100  # Random amount between 1500 and 40000, rounded to hundreds

    # Generate transactions for this iteration
    user_transactions_df = pd.DataFrame(generate_user_transactions(num_months, total_loan_amount, loan_commission_rate))

    # Append the new DataFrame to the list
    transactions_list.append(user_transactions_df)

# Combine all DataFrames in the list into one DataFrame
all_transactions_df = pd.concat(transactions_list, ignore_index=True)

# Save the combined dataframe to CSV
output_path = os.path.join('data', 'user_transactions.csv')
all_transactions_df.to_csv(output_path, index=False)

print("Dataset generation complete. Data saved to 'user_transactions.csv'")# Parameters for the dataset generation
expense_increase_threshold = 200  # Expense increase threshold for loan payment adjustment
loan_reduction_rate = 0.2  # Loan reduction rate when expense increase threshold is exceeded
loan_commission_rate = 0.05

# Initialize a list to store DataFrames
transactions_list = []

for _ in range(200):
    # Randomly select the number of months and loan amount
    num_months = random.choice([12, 24, 36, 48, 60])
    total_loan_amount = random.randint(15, 400) * 100  # Random amount between 1500 and 40000, rounded to hundreds

    # Generate transactions for this iteration
    user_transactions_df = pd.DataFrame(generate_user_transactions(num_months, total_loan_amount, loan_commission_rate))

    # Append the new DataFrame to the list
    transactions_list.append(user_transactions_df)

# Combine all DataFrames in the list into one DataFrame
all_transactions_df = pd.concat(transactions_list, ignore_index=True)

# Save the combined dataframe to CSV
output_path = os.path.join('data', 'user_transactions.csv')
all_transactions_df.to_csv(output_path, index=False)

print("Dataset generation complete. Data saved to 'user_transactions.csv'")
