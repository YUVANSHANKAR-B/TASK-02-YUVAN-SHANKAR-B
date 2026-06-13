import csv
import math
import random
from collections import Counter

FEATURE_NAMES = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]
TARGET_NAMES = ["setosa", "versicolor", "virginica"]

DATA_CSV = """
sepal_length,sepal_width,petal_length,petal_width,target
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
5.4,3.7,1.5,0.2,setosa
4.8,3.4,1.6,0.2,setosa
4.8,3.0,1.4,0.1,setosa
4.3,3.0,1.1,0.1,setosa
5.8,4.0,1.2,0.2,setosa
5.7,4.4,1.5,0.4,setosa
5.4,3.9,1.3,0.4,setosa
5.1,3.5,1.4,0.3,setosa
5.7,3.8,1.7,0.3,setosa
5.1,3.8,1.5,0.3,setosa
5.4,3.4,1.7,0.2,setosa
5.1,3.7,1.5,0.4,setosa
4.6,3.6,1.0,0.2,setosa
5.1,3.3,1.7,0.5,setosa
4.8,3.4,1.9,0.2,setosa
5.0,3.0,1.6,0.2,setosa
5.0,3.4,1.6,0.4,setosa
5.2,3.5,1.5,0.2,setosa
5.2,3.4,1.4,0.2,setosa
4.7,3.2,1.6,0.2,setosa
5.1,3.8,1.9,0.4,setosa
5.7,2.8,4.1,1.3,versicolor
6.3,3.3,4.7,1.6,versicolor
4.9,2.4,3.3,1.0,versicolor
6.6,2.9,4.6,1.3,versicolor
5.2,2.7,3.9,1.4,versicolor
5.0,2.0,3.5,1.0,versicolor
5.9,3.0,4.2,1.5,versicolor
6.0,2.2,4.0,1.0,versicolor
6.1,2.9,4.7,1.4,versicolor
5.6,2.9,3.6,1.3,versicolor
6.7,3.1,4.4,1.4,versicolor
5.6,3.0,4.5,1.5,versicolor
5.8,2.7,4.1,1.0,versicolor
6.2,2.2,4.5,1.5,versicolor
5.6,2.5,3.9,1.1,versicolor
5.9,3.2,4.8,1.8,versicolor
6.1,2.8,4.0,1.3,versicolor
6.3,2.5,4.9,1.5,versicolor
6.1,2.8,4.7,1.2,versicolor
6.4,2.9,4.3,1.3,versicolor
6.6,3.0,4.4,1.4,versicolor
6.8,2.8,4.8,1.4,versicolor
6.7,3.0,5.0,1.7,versicolor
6.0,2.9,4.5,1.5,versicolor
5.7,2.6,3.5,1.0,versicolor
5.5,2.4,3.8,1.1,versicolor
5.5,2.4,3.7,1.0,versicolor
5.8,2.7,3.9,1.2,versicolor
6.0,2.7,5.1,1.6,versicolor
5.4,3.0,4.5,1.5,versicolor
6.0,3.4,4.5,1.6,versicolor
6.7,3.1,4.7,1.5,versicolor
6.3,2.3,4.4,1.3,versicolor
5.6,3.0,4.1,1.3,versicolor
5.5,2.5,4.0,1.3,versicolor
5.5,2.6,4.4,1.2,versicolor
6.1,3.0,4.6,1.4,versicolor
5.8,2.6,4.0,1.2,versicolor
5.0,2.3,3.3,1.0,versicolor
5.6,2.7,4.2,1.3,versicolor
5.7,3.0,4.2,1.2,versicolor
5.7,2.9,4.2,1.3,versicolor
6.2,2.9,4.3,1.3,versicolor
5.1,2.5,3.0,1.1,versicolor
5.7,2.8,4.1,1.3,versicolor
6.3,3.3,6.0,2.5,virginica
5.8,2.7,5.1,1.9,virginica
7.1,3.0,5.9,2.1,virginica
6.3,2.9,5.6,1.8,virginica
6.5,3.0,5.8,2.2,virginica
7.6,3.0,6.6,2.1,virginica
4.9,2.5,4.5,1.7,virginica
7.3,2.9,6.3,1.8,virginica
6.7,2.5,5.8,1.8,virginica
7.2,3.6,6.1,2.5,virginica
6.5,3.2,5.1,2.0,virginica
6.4,2.7,5.3,1.9,virginica
6.8,3.0,5.5,2.1,virginica
5.7,2.5,5.0,2.0,virginica
5.8,2.8,5.1,2.4,virginica
6.4,3.2,5.3,2.3,virginica
6.5,3.0,5.5,1.8,virginica
7.7,3.8,6.7,2.2,virginica
7.7,2.6,6.9,2.3,virginica
6.0,2.2,5.0,1.5,virginica
6.9,3.2,5.7,2.3,virginica
5.6,2.8,4.9,2.0,virginica
7.7,2.8,6.7,2.0,virginica
6.3,2.7,4.9,1.8,virginica
6.7,3.3,5.7,2.1,virginica
7.2,3.2,6.0,1.8,virginica
6.2,2.8,4.8,1.8,virginica
6.1,3.0,4.9,1.8,virginica
6.4,2.8,5.6,2.1,virginica
7.2,3.0,5.8,1.6,virginica
7.4,2.8,6.1,1.9,virginica
7.9,3.8,6.4,2.0,virginica
6.4,2.8,5.6,2.2,virginica
6.3,2.8,5.1,1.5,virginica
6.1,2.6,5.6,1.4,virginica
7.7,3.0,6.1,2.3,virginica
6.3,3.4,5.6,2.4,virginica
6.4,3.1,5.5,1.8,virginica
6.0,3.0,4.8,1.8,virginica
6.9,3.1,5.4,2.1,virginica
6.7,3.1,5.6,2.4,virginica
6.9,3.1,5.1,2.3,virginica
5.8,2.7,5.1,1.9,virginica
6.8,3.2,5.9,2.3,virginica
6.7,3.3,5.7,2.5,virginica
6.7,3.0,5.2,2.3,virginica
6.3,2.5,5.0,1.9,virginica
6.5,3.0,5.2,2.0,virginica
6.2,3.4,5.4,2.3,virginica
5.9,3.0,5.1,1.8,virginica
"""


def load_dataset():
    rows = list(csv.DictReader(DATA_CSV.strip().splitlines()))
    X = [
        [float(row[name]) for name in FEATURE_NAMES]
        for row in rows
    ]
    y = [row["target"] for row in rows]
    return {
        "name": "Iris sample dataset",
        "feature_names": FEATURE_NAMES,
        "target_names": TARGET_NAMES,
        "data": X,
        "target": y,
    }


def train_test_split(X, y, test_size=0.2, random_state=42):
    random_gen = random.Random(random_state)
    grouped = {}
    for xi, yi in zip(X, y):
        grouped.setdefault(yi, []).append(xi)

    X_train, X_test, y_train, y_test = [], [], [], []
    for label, rows in grouped.items():
        random_gen.shuffle(rows)
        split_at = max(1, int(len(rows) * (1 - test_size)))
        X_train.extend(rows[:split_at])
        y_train.extend([label] * split_at)
        X_test.extend(rows[split_at:])
        y_test.extend([label] * (len(rows) - split_at))

    combined = list(zip(X_train, y_train)) + list(zip(X_test, y_test))
    random_gen.shuffle(combined)
    X_train, y_train = zip(*combined[: len(X_train)])
    X_test, y_test = zip(*combined[len(X_train) :])
    return list(X_train), list(X_test), list(y_train), list(y_test)


def euclidean_distance(point1, point2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))


class NearestCentroidClassifier:
    def fit(self, X, y):
        centroids = {}
        counts = Counter(y)
        sums = {label: [0.0] * len(X[0]) for label in counts}

        for xi, yi in zip(X, y):
            sums[yi] = [s + val for s, val in zip(sums[yi], xi)]

        for label, total in sums.items():
            centroids[label] = [value / counts[label] for value in total]

        self.centroids = centroids

    def predict(self, X):
        predictions = []
        for xi in X:
            best_label = None
            best_distance = float("inf")
            for label, centroid in self.centroids.items():
                distance = euclidean_distance(xi, centroid)
                if distance < best_distance:
                    best_distance = distance
                    best_label = label
            predictions.append(best_label)
        return predictions


def classification_report(y_true, y_pred, target_names):
    labels = target_names
    report_rows = []
    for label in labels:
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == label == yp)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt != label and yp == label)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == label and yp != label)
        support = sum(1 for yt in y_true if yt == label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        report_rows.append((label, precision, recall, f1, support))

    parts = ["label      precision  recall  f1-score  support"]
    for label, precision, recall, f1, support in report_rows:
        parts.append(
            f"{label:9s} {precision:9.2f} {recall:7.2f} {f1:8.2f} {support:8d}"
        )
    accuracy = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true)
    parts.append("\n" + f"accuracy  {accuracy:9.2f}  {'':7s} {'':8s} {len(y_true):8d}")
    return "\n".join(parts)


def main():
    dataset = load_dataset()
    X = dataset["data"]
    y = dataset["target"]

    print("Dataset name:", dataset["name"])
    print("Number of samples:", len(X))
    print("Number of features:", len(FEATURE_NAMES))
    print("Feature names:", FEATURE_NAMES)
    print("Target classes:", TARGET_NAMES)
    print("\nClass distribution:")
    print(Counter(y))
    print("\nFirst 5 rows:")
    for row, label in zip(X[:5], y[:5]):
        print({FEATURE_NAMES[i]: row[i] for i in range(len(FEATURE_NAMES))}, "->", label)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    model = NearestCentroidClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = sum(1 for yt, yp in zip(y_test, y_pred) if yt == yp) / len(y_test)

    print("\nModel: Nearest Centroid")
    print(f"Accuracy on test set: {accuracy:.2f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, TARGET_NAMES))

    print("\nSample predictions:")
    for i in range(min(5, len(y_test))):
        print(
            f"True: {y_test[i]:9s}  Predicted: {y_pred[i]:9s}"
        )


if __name__ == "__main__":
    main()
