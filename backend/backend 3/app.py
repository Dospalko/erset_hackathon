from flask import Flask, jsonify

import pandas as pd
from data_analysis import load_transactions, calculate_repayment_plan, load_loan_details

app = Flask(__name__)

import joblib

# Load your trained model
model = joblib.load('/model/multiple_trained_model.pkl')


# Function to input data from the terminal
def input_data():
    loan = float(input("Enter the loan amount: "))
    months = float(input("Enter number of months: "))
    income = float(input("Enter the monthly income: "))
    expenses = float(input("Enter the total monthly expenses: "))
    necessary_expenses = float(input("Enter the necessary monthly expenses: "))
    unnecessary_expenses = float(input("Enter the unnecessary monthly expenses: "))

    # Return the input data as a dictionary
    return {
        'loan': loan,
        'months': months,
        'income': income,
        'expenses': expenses,
        'necessary_expenses': necessary_expenses,
        'unnecessary_expenses': unnecessary_expenses
    }

# Function to predict loan payment
def predict_loan_payment(input_data):
    input_data = pd.DataFrame(input_data, index=[0])
    prediction = model.predict(input_data)
    return prediction[0]

# Main function to get input and make predictions
def main():
    print("Loan Payment Prediction")
    data = input_data()
    loan_payment = predict_loan_payment(data)
    print(f"Predicted Loan Payment: {loan_payment:.2f}")

if __name__ == "__main__":
    main()
