from flask import Flask, jsonify, request
import pandas as pd
import joblib
from flask_cors import CORS  # Make sure you've installed flask-cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your trained model
model = joblib.load('model/multiple_trained_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from POST request
    data = request.get_json(force=True)

    # Validate and extract input data
    loan = data.get("loan", 10000)
    months = data.get("months", 12)
    income = data.get("income", 3000)
    expenses = data.get("expenses", 0)
    necessary_expenses = data.get("necessary_expenses", 0)
    unnecessary_expenses = data.get("unnecessary_expenses", 0)

    # Create DataFrame from the input data
    input_df = pd.DataFrame({
        'loan': [loan],
        'months': [months],
        'income': [income],
        'expenses': [expenses],
        'necessary_expenses': [necessary_expenses],
        'unnecessary_expenses': [unnecessary_expenses]
    })

    # Make prediction
    prediction = model.predict(input_df)

    # Return prediction as JSON
    return jsonify({'predicted_loan_payment': float(prediction[0])})

# If you still want the command line feature, you can keep this
def input_data():
    print("Enter loan details for prediction:")
    loan = float(input("Enter the loan amount: "))
    months = float(input("Enter number of months: "))
    income = float(input("Enter the monthly income: "))
    expenses = float(input("Enter the total monthly expenses: "))
    necessary_expenses = float(input("Enter the necessary monthly expenses: "))
    unnecessary_expenses = float(input("Enter the unnecessary monthly expenses: "))
    return {
        'loan': loan,
        'months': months,
        'income': income,
        'expenses': expenses,
        'necessary_expenses': necessary_expenses,
        'unnecessary_expenses': unnecessary_expenses
    }

def predict_loan_payment(input_data):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    return prediction[0]

# Command line interaction is an additional feature
def command_line_feature():
    user_data = input_data()
    loan_payment = predict_loan_payment(user_data)
    print(f"Predicted Loan Payment: {loan_payment:.2f}")
@app.route('/data', methods=['GET'])
def get_data():
    df = pd.read_csv('data/user_transactions.csv')
    # Convert the DataFrame to a JSON format. You might need to adjust this depending on your CSV structure.
    data = df.to_dict(orient='records')
    return jsonify(data)
# Main function to start Flask server
if __name__ == "__main__":
    # Uncomment the next line if you want to enable command line feature
    # command_line_feature()
    app.run(debug=True)  # Start the Flask server
