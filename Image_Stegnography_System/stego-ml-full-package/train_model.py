import os, joblib
import numpy as np
from feature_extractor import extract_features
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X=[]; y=[]
for img in os.listdir("dataset/clean"):
    X.append(extract_features("dataset/clean/"+img)); y.append(0)
for img in os.listdir("dataset/stego"):
    X.append(extract_features("dataset/stego/"+img)); y.append(1)

X=np.array(X); y=np.array(y)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

model=LogisticRegression(max_iter=1000)
model.fit(X_train,y_train)

pred=model.predict(X_test)
print("Accuracy:",accuracy_score(y_test,pred))

joblib.dump(model,"stego_detector.pkl")
print("Model saved as stego_detector.pkl")
