from flask import Flask, jsonify
from flask_cors import CORS
from data_analysis import load_transactions, calculate_repayment_plan, load_loan_details

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the AI Bank Project API!"})

@app.route('/analyze', methods=['GET'])
def analyze():
    result = load_transactions()
    return jsonify(result)

@app.route('/calculate', methods=['GET'])
def calculate():
    monthly_expenses = load_transactions()
    loan_details = load_loan_details()
    result = calculate_repayment_plan(monthly_expenses, loan_details)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
