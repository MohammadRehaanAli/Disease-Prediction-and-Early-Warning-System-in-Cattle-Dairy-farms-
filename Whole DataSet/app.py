from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy prediction logic
def predict_disease(temperature, pulse):
    if temperature > 39 and pulse > 80:
        return "Heat Stress", "Provide cool shade and plenty of water"
    elif temperature > 38 and pulse > 75:
        return "Viral Infection", "Isolate and consult a veterinarian"
    elif temperature > 37 and pulse > 70:
        return "Bacterial Infection", "Antibiotic treatment may be required"
    else:
        return "Healthy", "No specific precautions needed"

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/predict_disease', methods=['POST'])
def predict_disease_route():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.endswith('.csv'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Read the CSV file using pandas
        data = pd.read_csv(file_path)

        # Ensure the CSV has the required columns: 'Cattle ID', 'Temperature', 'Pulse'
        if not {'Cattle ID', 'Temperature', 'Pulse'}.issubset(data.columns):
            return "CSV must contain 'Cattle ID', 'Temperature', and 'Pulse' columns."

        results = []

        # Loop through the dataframe rows and make predictions
        for index, row in data.iterrows():
            cattle_id = row['Cattle ID']
            temperature = row['Temperature']
            pulse = row['Pulse']

            detected_disease, precautions = predict_disease(temperature, pulse)

            results.append({
                'cattle_id': cattle_id,
                'detected_disease': detected_disease,
                'precautions': precautions
            })

        # Render the results on the results.html page
        return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
