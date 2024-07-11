from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json

app = Flask(__name__)

# Load TensorFlow model and class names
probability_model = tf.keras.models.load_model('model.keras')
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Load item database
with open('items.json', 'r') as f:
    items_db = json.load(f)

# Function to preprocess and classify image
def classify_image(image):
    image = np.array(image)
    image = tf.image.resize(image, [28, 28])
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    predictions = probability_model.predict(image)
    predicted_class = np.argmax(predictions[0])
    class_name = class_names[predicted_class]
    return class_name

# Function to get matching items
def get_matching_items(class_name, occasion=None, season=None):
    matching_items = []
    for item in items_db:
        if 'match_with' in item and class_name.lower() in item['match_with']:
            if occasion and season:
                if 'occasion' in item and 'season' in item:
                    if item['occasion'] == occasion and item['season'] == season:
                        matching_items.append(item)
            else:
                matching_items.append(item)
    return matching_items

# Endpoint to receive image and classify
@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    occasion = request.form.get('occasion')
    season = request.form.get('season')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename:
        try:
            image = Image.open(io.BytesIO(file.read()))
            image = image.convert('RGB')
            class_name = classify_image(image)
            matching_items = get_matching_items(class_name, occasion, season)
            return jsonify({'class_name': class_name, 'matching_items': matching_items})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
