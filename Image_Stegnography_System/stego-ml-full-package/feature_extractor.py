import cv2
import numpy as np

def extract_features(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256,256))
    hist = cv2.calcHist([img],[0,1,2],None,[8,8,8],[0,256]*3)
    hist = cv2.normalize(hist, hist).flatten()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,100,200)
    edge_density = (edges>0).sum() / edges.size
    noise = gray.std()
    return np.hstack([hist, edge_density, noise])
