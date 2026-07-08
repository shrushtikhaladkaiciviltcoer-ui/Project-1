# =============================================================================
#  Project 2: Data Classification Using AI
#  Dataset   : Iris (150 samples, 3 classes, 4 features)
#  Algorithm : K-Nearest Neighbors (KNN)
#  Framework : IPO (Input -> Process -> Output)
# =============================================================================

# ----------------------------- 1. IMPORTS ------------------------------------
# Standard library packages required for the pipeline
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    f1_score,
    accuracy_score,
)

# =============================================================================
# =========================== INPUT STAGE =====================================
# =============================================================================
print("=" * 70)
print("INPUT STAGE  →  Loading the Iris Dataset")
print("=" * 70)

# Load the benchmark Iris dataset from scikit-learn
iris = load_iris()

# Create a pandas DataFrame for easy inspection and manipulation
df = pd.DataFrame(
    data=iris.data,
    columns=iris.feature_names   # ['sepal length (cm)', 'sepal width (cm)',
                                 #  'petal length (cm)', 'petal width (cm)']
)
df["species"] = iris.target      # Add target column (0=Setosa, 1=Versicolor, 2=Virginica)

# Display dataset information
print(f"Dataset Shape        : {df.shape}")           # (150, 5)
print(f"Number of Classes    : {len(iris.target_names)} ({iris.target_names.tolist()})")
print(f"Number of Features   : {len(iris.feature_names)}")
print(f"Samples per Class    : {dict(df['species'].value_counts())}\n")
print("First 5 samples:")
print(df.head())

# Separate features (X) and target labels (y)
X = df.drop("species", axis=1).values   # Feature matrix → shape (150, 4)
y = df["species"].values                # Target vector  → shape (150,)

# =============================================================================
# ========================== PROCESS STAGE ====================================
# =============================================================================
print("\n" + "=" * 70)
print("PROCESS STAGE  →  Scaling, Shuffling, Splitting & Training KNN")
print("=" * 70)

# --- Step 1: Feature Scaling ----------------------------------------------------
# StandardScaler standardizes features to Mean = 0 and Variance = 1.
# This removes scale bias so that features measured in different units
# (e.g. cm) contribute equally to the KNN distance calculations.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Step 2: Train-Test Split with Shuffling ------------------------------------
# Setting shuffle=True (default) eliminates order bias so the model does
# not learn the original sequence of samples.
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.20,        # 80% training, 20% testing
    random_state=42,       # Ensures reproducibility
    shuffle=True,          # Shuffle data before splitting
    stratify=y,            # Preserve class balance in train/test sets
)

print(f"Training samples : {X_train.shape[0]}")
print(f"Testing  samples : {X_test.shape[0]}")

# --- Step 3: Apply K-Nearest Neighbors (KNN) -------------------------------------
# KNN is a supervised learning algorithm that classifies a sample based on
# the majority class among its 'k' closest neighbors in feature space.
k_value = 5
knn_model = KNeighborsClassifier(n_neighbors=k_value, metric="minkowski", p=2)

# Train the model (KNN simply memorizes the training data)
knn_model.fit(X_train, y_train)

# Make predictions on the unseen test set
y_pred = knn_model.predict(X_test)

# =============================================================================
# =========================== OUTPUT STAGE =====================================
# =============================================================================
print("\n" + "=" * 70)
print("OUTPUT STAGE  →  Model Evaluation Metrics")
print("=" * 70)

# --- 1. Accuracy Score ---------------------------------------------------------
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy Score : {accuracy * 100:.2f}%")

# --- 2. Confusion Matrix -------------------------------------------------------
# Rows = actual class, Columns = predicted class
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(
    cm,
    index=[f"Actual_{name}"   for name in iris.target_names],
    columns=[f"Pred_{name}"   for name in iris.target_names],
)
print("\n📊 Confusion Matrix:")
print(cm_df)

# --- 3. F1 Score ---------------------------------------------------------------
# Weighted F1 accounts for class imbalance (safe even though Iris is balanced).
f1_weighted = f1_score(y_test, y_pred, average="weighted")
f1_macro    = f1_score(y_test, y_pred, average="macro")
print(f"\n🎯 F1 Score (Weighted) : {f1_weighted:.4f}")
print(f"🎯 F1 Score (Macro)    : {f1_macro:.4f}")

# --- 4. Full Classification Report --------------------------------------------
print("\n📋 Detailed Classification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# =============================================================================
# ====================== INTERACTIVE PREDICTION DEMO ===========================
# =============================================================================
print("=" * 70)
print("🌐 LIVE PREDICTION  →  Try classifying your own flower!")
print("=" * 70)

# Allow user to input a flower's measurements for real-time classification.
try:
    sl = float(input("Enter Sepal Length (cm) : "))
    sw = float(input("Enter Sepal Width  (cm) : "))
    pl = float(input("Enter Petal Length (cm) : "))
    pw = float(input("Enter Petal Width  (cm) : "))

    # Build a single-sample array and apply the SAME scaler used in training
    sample            = np.array([[sl, sw, pl, pw]])
    sample_scaled     = scaler.transform(sample)
    predicted_class   = knn_model.predict(sample_scaled)[0]
    predicted_proba   = knn_model.predict_proba(sample_scaled)[0]

    print(f"\n🌼 Predicted Species : {iris.target_names[predicted_class]}")
    print("   Class Probabilities:")
    for name, prob in zip(iris.target_names, predicted_proba):
        print(f"     • {name:<12}: {prob * 100:5.2f}%")

except ValueError:
    print("⚠️  Invalid input. Please enter numeric values only.")

print("\n" + "=" * 70)
print("✅ Project 2 Complete — Pipeline executed successfully.")
print("=" * 70)
