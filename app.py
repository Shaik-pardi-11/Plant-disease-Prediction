from flask import Flask, render_template, request, send_from_directory
import json
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('models/plant_disease_model.h5')

# Define the labels for predictions
label = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
         'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
         'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
         'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
         'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
         'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 
         'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
         'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
         'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 
         'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 
         'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
         'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
         'Tomato___healthy']

# Load plant disease descriptions
with open('plant_disease.json', 'r') as file:
    plant_disease = json.load(file)

@app.route('/uploadimages/<path:filename>')
def uploaded_images(filename):
    return send_from_directory('uploadimages', filename)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_label = None
    description = None
    filename = None
    if request.method == 'POST':
        img_file = request.files['plant-image']
        img_path = os.path.join('uploadimages', img_file.filename)
        img_file.save(img_path)
        # Make prediction
        predicted_idx, confidence = model_predict(img_path)
        prediction_label = label[predicted_idx]
        description = plant_disease.get(prediction_label, "No description available.")
        filename = img_file.filename
        return render_template('result.html', prediction_label=prediction_label, description=description, confidence=confidence, filename=filename)
    return render_template('home.html')

# Feature extraction function
def extract_features(image):
    image = tf.keras.utils.load_img(image, target_size=(160,160))
    feature = tf.keras.utils.img_to_array(image)
    feature = feature / 255.0
    feature = np.expand_dims(feature, axis=0)
    return feature

# Model prediction function
def model_predict(image):
    img = extract_features(image)
    prediction = model.predict(img)
    predicted_idx = np.argmax(prediction)
    confidence = float(np.max(prediction))
    return predicted_idx, confidence
