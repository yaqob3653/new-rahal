import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler
import joblib
import os

# 1. Generate Synthetic Data
n_samples = 2000
np.random.seed(42)

# Features: [age, weight, acc_val, pref_family, pref_thrill, pref_food]
age = np.random.randint(10, 70, n_samples)
weight = np.random.randint(40, 120, n_samples)
acc_val = np.random.randint(0, 4, n_samples) # 0: Alone, 1: Friends, 2: Family, 3: Kids
pref_family = np.random.rand(n_samples)
pref_thrill = np.random.rand(n_samples)
pref_food = np.random.rand(n_samples)

X = np.column_stack((age, weight, acc_val, pref_family, pref_thrill, pref_food))

# Target Logic (Cluster 0, 1, 2)
y = []
for i in range(n_samples):
    if pref_thrill[i] > 0.6:
        y.append(1.0) # Thrill
    elif pref_family[i] > 0.6 or acc_val[i] >= 2:
        y.append(2.0) # Family
    else:
        y.append(0.0) # General

y = np.array(y)

# 2. Scale Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Build Deep Learning Model (Sequential)
# Dense 64, 32, 1
model = Sequential([
    Dense(64, activation='relu', input_shape=(6,)),
    Dense(32, activation='relu'),
    Dense(1, activation='linear') 
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 4. Train Model
print("Training Deep Learning Model...")
model.fit(X_scaled, y, epochs=50, batch_size=32, verbose=1)

# 5. Save Model & Scaler
model_dir = os.path.join("Rahhal_Flask", "models")
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

model_path = os.path.join(model_dir, "recommendation_model.h5")
scaler_path = os.path.join(model_dir, "scaler.pkl")

model.save(model_path)
joblib.dump(scaler, scaler_path)

print(f"✅ Model saved to {model_path}")
print(f"✅ Scaler saved to {scaler_path}")
