import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib  # для збереження моделі

# 1. Завантаження датасету
df = pd.read_csv(r"C:\Users\zenas\Desktop\Me\Applied ML Methods on an ECU in MicroPython (ESP32)\esp32\touch_dataset_example.csv")

# 2. Вхідні та цільові дані
X = df.drop("label", axis=1)
y = df["label"]

# 3. Розбиття на train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Навчання моделі
clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# 5. Оцінка
y_pred = clf.predict(X_test)
print("Classification report:\n", classification_report(y_test, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

# 6. Збереження моделі
joblib.dump(clf, "touch_model.joblib")
print("✅Model saved as touch_model.joblib")
