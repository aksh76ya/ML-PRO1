from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

app = Flask(__name__)

# Define emoji mapping
emoji_map = {
    0: "❤️",  # Love
    1: "🍕",  # Pizza
    2: "🐶",  # Dog
    3: "😊",  # Happy
    4: "🎉",  # Party
}

# Simple pre-trained model (for demonstration purposes)
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=1000, output_dim=16, input_length=10),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')  # 5 classes for 5 emojis
])

# Compile the model (this is just a placeholder; you can train your own model)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Tokenizer for text preprocessing
tokenizer = Tokenizer(num_words=1000)
tokenizer.fit_on_texts(["i love you", "pizza is great", "my dog is cute", "i am happy", "lets party"])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    
    # Preprocess the input text
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=10, padding='post')
    
    # Predict the emoji
    prediction = model.predict(padded_sequence)
    emoji_index = np.argmax(prediction)
    emoji = emoji_map.get(emoji_index, "❓")  # Default to "❓" if emoji not found
    
    return jsonify({'emoji': emoji})

if __name__ == '__main__':
    app.run(debug=True)