from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Simulating models for predictions
def random_prediction():
    return random.uniform(0.7, 0.99)  # Generate a random confidence between 70% and 99%

models = ["CNN", "SVM", "Logistic Regression", "Random Forest"]

@app.route('/')
def home():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image uploads and make predictions."""
    file = request.files.get('file')
    sub_option = request.form.get('sub_option')

    if not file or not sub_option:
        return jsonify({"error": "Image and sub-option are required."}), 400

    # Simulating model predictions
    results = {}
    for model in models:
        confidence = random_prediction()
        prediction = "Cat" if confidence > 0.75 else "Dog"
        results[model] = {"prediction": prediction, "confidence": f"{confidence*100:.2f}%"}

    # Calculating overview and averages
    overview = {}
    total_confidence = 0
    for model, data in results.items():
        total_confidence += float(data['confidence'].strip('%'))
        overview[model] = f"{data['prediction']} ({data['confidence']})"
    
    average_confidence = total_confidence / len(models)

    return render_template(
        'results.html', 
        results=results, 
        overview=overview, 
        average_confidence=f"{average_confidence:.2f}%"
    )

if __name__ == '__main__':
    app.run(debug=True)
