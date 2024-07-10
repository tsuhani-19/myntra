from flask import Flask, request,render_template,jsonify
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# Load your TensorFlow model (probability_model) and define class_names
probability_model = tf.keras.models.load_model('model.keras')  # Update with your model loading code
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Function to preprocess and classify image
def classify_image(image):
    # Example preprocessing (adjust based on your model requirements)
    image = tf.image.resize(image, [28, 28])  # Resize image as per your model input shape
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    predictions = probability_model.predict(image)
    predicted_class = np.argmax(predictions[0])
    class_name = class_names[predicted_class]
    return class_name

# Endpoint to receive image and classify

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)









