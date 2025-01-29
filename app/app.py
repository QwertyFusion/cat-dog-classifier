from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import pickle

app = Flask(__name__, static_folder='static')

# Load Models
try:
    cnn_model = tf.keras.models.load_model('app/models/cnn_model.h5')  # Replace with your CNN model file
    with open("app/models/svm_model.pkl", "rb") as f:
        svm_model = pickle.load(f)
    with open("app/models/rf_model.pkl", "rb") as f:
        rf_model = pickle.load(f)
    with open("app/models/lr_model.pkl", "rb") as f:
        lr_model = pickle.load(f)
    with open("app/models/kmeans_model.pkl", "rb") as f:
        kmeans_model = pickle.load(f)
    vgg_model = tf.keras.applications.VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
except Exception as e:
    print(f"Error loading models: {e}")
    exit()

IMG_HEIGHT = 150
IMG_WIDTH = 150

UPLOAD_FOLDER = 'app/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_cnn(img_array):
    img_array = img_array / 255.0
    prediction = cnn_model.predict(img_array)[0][0]
    return "Dog" if prediction > 0.5 else "Cat"

def predict_other_models(img_array):
    img_array = preprocess_input(img_array)
    features = vgg_model.predict(img_array)
    features = features.reshape(features.shape[0], -1)

    svm_prediction = svm_model.predict(features)[0]
    rf_prediction = rf_model.predict(features)[0]
    lr_prediction = lr_model.predict(features)[0]
    kmeans_prediction = kmeans_model.predict(features)[0]

    svm_label = "Dog" if svm_prediction == 1 else "Cat"
    rf_label = "Dog" if rf_prediction == 1 else "Cat"
    lr_label = "Dog" if lr_prediction == 1 else "Cat"
    kmeans_label = "Dog" if kmeans_prediction == 1 else "Cat" # Adjust if needed

    return svm_label, rf_label, lr_label, kmeans_label

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        img_array = prepare_image(filepath)

        try:
            cnn_prediction = predict_cnn(img_array)
            svm_prediction, rf_prediction, lr_prediction, kmeans_prediction = predict_other_models(img_array)

            predictions = [cnn_prediction, svm_prediction, rf_prediction, lr_prediction, kmeans_prediction]
            final_prediction = max(set(predictions), key=predictions.count)

            return jsonify({
                'cnn': cnn_prediction,
                'svm': svm_prediction,
                'random_forest': rf_prediction,
                'logistic_regression': lr_prediction,
                'kmeans': kmeans_prediction,
                'final_prediction': final_prediction
            })

        except Exception as e:
            return jsonify({'error': str(e)})

    return jsonify({'error': 'Invalid file type'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)