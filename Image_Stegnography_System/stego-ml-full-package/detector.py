import joblib
from feature_extractor import extract_features
import os

model = None
model_path = "stego_detector.pkl"

def load_model():
    global model
    if model is None:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
        else:
            raise FileNotFoundError(f"Model file '{model_path}' not found. Run 'python train_model.py' in the package directory to create it.")
    return model

def detect(image_path):
    mdl = load_model()
    f = extract_features(image_path)
    pred = mdl.predict([f])[0]
    return "Stego Image Detected" if pred==1 else "No Hidden Data Found"
