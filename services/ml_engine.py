import os
import random
import pickle
import datetime
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from concurrent.futures import ThreadPoolExecutor
from sklearn.linear_model import LinearRegression
from utils.db import get_connection, release_connection

MODEL_PATH = "demand_model.pkl"


def generate_synthetic_training_data(num_samples=500):
    data = []

    for _ in range(num_samples):
        day_of_week = random.randint(0, 6)
        hour_of_day = random.randint(8, 20)
        resource_type_code = random.randint(0, 3)
        department_code = random.randint(0, 5)
        past_usage_frequency = random.randint(0, 50)

        base_demand = past_usage_frequency * 0.5

        if hour_of_day in [10, 11, 14, 15]:
            base_demand += 10

        if day_of_week in [5, 6]:
            base_demand -= 8

        noise = random.uniform(-3, 3)
        demand_score = max(0, base_demand + noise)

        data.append([day_of_week, hour_of_day, resource_type_code, department_code, past_usage_frequency, demand_score])

    return data


def train_demand_model():
    training_data = generate_synthetic_training_data(500)

    features = []
    labels = []

    for row in training_data:
        features.append(row[0:5])
        labels.append(row[5])

    features_array = np.array(features)
    labels_array = np.array(labels)

    model = LinearRegression()
    model.fit(features_array, labels_array)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return model


def load_model():
    if not os.path.exists(MODEL_PATH):
        return train_demand_model()

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    return model


def predict_demand(day_of_week, hour_of_day, resource_type_code, department_code, past_usage_frequency):
    model = load_model()

    input_features = np.array([[day_of_week, hour_of_day, resource_type_code, department_code, past_usage_frequency]])
    prediction = model.predict(input_features)

    return float(prediction[0])


CLUSTER_MODEL_PATH = "cluster_model.pkl"


def _fetch_resource_utilization_features():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.id, COUNT(b.id) as booking_count,
               COALESCE(SUM(EXTRACT(EPOCH FROM (b.end_time - b.start_time)) / 3600), 0) as total_hours
        FROM resources r
        LEFT JOIN bookings b ON r.id = b.resource_id AND b.status = 'approved'
        GROUP BY r.id
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    release_connection(conn)
    return rows


def train_cluster_model():
    rows = _fetch_resource_utilization_features()

    if len(rows) < 3:
        return None

    resource_ids = []
    features = []

    for row in rows:
        resource_ids.append(row[0])
        features.append([row[1], float(row[2])])

    features_array = np.array(features)

    num_components = min(2, features_array.shape[1])
    pca = PCA(n_components=num_components)
    reduced_features = pca.fit_transform(features_array)

    num_clusters = min(3, len(rows))
    kmeans = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
    cluster_labels = kmeans.fit_predict(reduced_features)

    with open(CLUSTER_MODEL_PATH, "wb") as f:
        pickle.dump({"pca": pca, "kmeans": kmeans}, f)

    results = []
    for i in range(len(resource_ids)):
        results.append({
            "resource_id": resource_ids[i],
            "booking_count": features[i][0],
            "total_hours": features[i][1],
            "cluster": int(cluster_labels[i])
        })

    return results


def get_clusters():
    return train_cluster_model()


def predict_demand_batch(resource_requests):
    def predict_one(req):
        demand = predict_demand(
            req["day_of_week"],
            req["hour_of_day"],
            req["resource_type_code"],
            req["department_code"],
            req["past_usage_frequency"]
        )
        return {
            "resource_id": req["resource_id"],
            "predicted_demand": demand
        }

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(predict_one, resource_requests))

    return results
