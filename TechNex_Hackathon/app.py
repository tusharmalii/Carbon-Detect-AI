import os
import base64
import io
import time
import webbrowser
from threading import Timer

# --- MANDATORY: COMPATIBILITY SETTINGS ---
os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from tensorflow.keras.layers import DepthwiseConv2D

app = Flask(__name__)
app.secret_key = "ecosorter_final_v2026"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecosorter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- AI VERSION PATCH ---
class PatchedDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, **kwargs):
        if 'groups' in kwargs:
            kwargs.pop('groups')
        super().__init__(**kwargs)

# --- DATABASE SCHEMA ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    carbon_saved = db.Column(db.Float, default=0.0)

# --- AI ENGINE LOADING ---
model = None
labels = []
try:
    model = tf.keras.models.load_model(
        "keras_model.h5", 
        compile=False,
        custom_objects={'DepthwiseConv2D': PatchedDepthwiseConv2D}
    )
    with open("labels.txt", "r") as f:
        labels = [line.strip().split(" ")[1] for line in f.readlines()]
    print("\n✅ SYSTEM: AI CORE INITIALIZED")
except Exception as e:
    print(f"\n❌ AI LOAD ERROR: {e}")

# --- API ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/auth', methods=['POST'])
def auth():
    try:
        data = request.get_json()
        u, p = data.get('username'), data.get('password')
        
        user = User.query.filter_by(username=u).first()
        if not user:
            # Auto-Signup
            user = User(username=u, password=p)
            db.session.add(user)
            db.session.commit()
            
        if user.password == p:
            session['user_id'] = user.id
            return jsonify({
                "success": True, 
                "username": user.username, 
                "saved": round(user.carbon_saved, 2)
            })
        return jsonify({"success": False, "message": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'user_id' not in session or model is None:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    image_data = base64.b64decode(data['image'].split(',')[1])
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    
    img_array = np.asarray(image).astype(np.float32) / 127.5 - 1
    input_tensor = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    input_tensor[0] = img_array

    prediction = model.predict(input_tensor, verbose=0)
    idx = np.argmax(prediction)
    name = labels[idx]
    conf = float(prediction[0][idx])

    savings = {"Recyclable": 0.5, "Biodegradable": 0.2, "Hazardous": 1.5}.get(name, 0.0)
    user = User.query.get(session['user_id'])
    user.carbon_saved += savings
    db.session.commit()

    return jsonify({
        "category": name,
        "confidence": round(conf * 100, 2),
        "total_carbon": round(user.carbon_saved, 2),
        "timestamp": time.strftime("%H:%M:%S")
    })

# --- AUTO-LAUNCH ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(host='0.0.0.0', port=5000, debug=False)