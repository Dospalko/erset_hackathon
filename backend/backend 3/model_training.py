import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Load your dataset (replace 'data.csv' with your dataset file)
data = pd.read_csv('data/user_transactions.csv')

# Define features and target variable
X = data[['loan', 'months', 'income', 'expenses', 'necessary_expenses', 'unnecessary_expenses']]
y = data['loan_payment']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the Random Forest Regressor model
model = RandomForestRegressor(random_state=42)

# Define the hyperparameters and their respective values to search through
param_grid = {
    'n_estimators': [300, 200],  # Number of trees in the forest
    'max_depth': [None, 10, 11],  # Maximum depth of the trees
    'min_samples_split': [2, 0.5, 7],  # Minimum number of samples required to split an internal node
    'min_samples_leaf': [15, 8]  # Minimum number of samples required to be at a leaf node
}

# Create GridSearchCV to find the best hyperparameters
grid_search = GridSearchCV(model, param_grid, scoring='neg_mean_squared_error', cv=5, verbose=1, n_jobs=-1)

# Fit the grid search to the training data
grid_search.fit(X_train, y_train)

# Get the best model and its parameters
best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

# Make predictions on the test set using the best model
y_pred = best_model.predict(X_test)

# Evaluate the best model's performance
mse = mean_squared_error(y_test, y_pred)
# Calculate prediction accuracy in percentage
accuracy = 100 - (mse / np.var(y_test)) * 100

print(f'Best Model Parameters: {best_params}')
print(f'Best Model Prediction Accuracy: {accuracy:.2f}%')

# Save the best model
joblib.dump(best_model, '../model/multiple_trained_model.pkl')
