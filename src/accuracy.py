import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

metrics_path = 'data/metrics_simulation_data_100u_200d.csv'

df = pd.read_csv(metrics_path)

def categorize(value):
    if 0 <= value < 0.2:
        return 1
    elif 0.2 <= value < 0.4:
        return 2
    elif 0.4 <= value <= 1:
        return 3
    else:
        return None

# Apply the function to the 'a' column to create a new categorical column
df['Results'] = df['Engagement Score'].apply(categorize)

# Save the updated DataFrame back to a CSV file
df.to_csv('data/metrics_simulation_data_100u_200d_r.csv', index=False)

df = pd.read_csv('data/metrics_simulation_data_100u_200d_r.csv')

y_true = df['Engagement Level']
y_pred = df['Results']

conf_matrix = confusion_matrix(y_true, y_pred)

accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(y_true, y_pred, average=None)

recall = recall_score(y_true, y_pred, average=None)

f1 = f1_score(y_true, y_pred, average=None)

print(f'{conf_matrix=}, {accuracy=}, {precision=}, {recall=}, {f1=}')
