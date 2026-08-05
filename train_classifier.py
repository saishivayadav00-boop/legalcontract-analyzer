import os
import sys
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.download_cuad import download_cuad_dataset, CUAD_JSON_PATH
from modules.cuad_preprocessor import prepare_training_data

# Import XGBoost with fallback
try:
    from xgboost import XGBClassifier
    USE_XGBOOST = True
except ImportError:
    from sklearn.ensemble import GradientBoostingClassifier
    USE_XGBOOST = False

def train_clause_classifier():
    data_dir = "data"
    models_dir = "models"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    train_csv = os.path.join(data_dir, "train.csv")
    test_csv = os.path.join(data_dir, "test.csv")

    # Force dataset download and preparation with rich CUAD samples
    json_path = download_cuad_dataset(CUAD_JSON_PATH)
    train_df, test_df = prepare_training_data(json_path, data_dir=data_dir)


    # Clean missing entries
    train_df = train_df.dropna(subset=["clause_text", "label"])
    test_df = test_df.dropna(subset=["clause_text", "label"])

    X_train_text = train_df["clause_text"].astype(str)
    y_train_raw = train_df["label"].astype(str)

    X_test_text = test_df["clause_text"].astype(str)
    y_test_raw = test_df["label"].astype(str)

    # Encode labels
    label_encoder = LabelEncoder()
    all_labels = pd.concat([y_train_raw, y_test_raw]).unique()
    label_encoder.fit(all_labels)

    y_train = label_encoder.transform(y_train_raw)
    y_test = label_encoder.transform(y_test_raw)

    # Build TF-IDF Vectorizer
    print("Building TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words='english'
    )
    X_train_tfidf = vectorizer.fit_transform(X_train_text)
    X_test_tfidf = vectorizer.transform(X_test_text)

    # Train Classifier (XGBoost or GradientBoosting fallback)
    print("Training clause classification model...")
    if USE_XGBOOST:
        print("Using XGBoost Classifier...")
        model = XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42,
            eval_metric="mlogloss"
        )
    else:
        print("XGBoost not available. Using GradientBoostingClassifier fallback...")
        model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )

    model.fit(X_train_tfidf, y_train)

    # Evaluate Model
    y_pred = model.predict(X_test_tfidf)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print("\n" + "="*40)
    print("MODEL EVALUATION RESULTS")
    print("="*40)
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-score:  {f1:.4f}")
    print("="*40 + "\n")

    # Save trained model artifact to models/classifier.pkl
    model_artifact = {
        "model": model,
        "vectorizer": vectorizer,
        "label_encoder": label_encoder,
        "use_xgboost": USE_XGBOOST
    }

    model_path = os.path.join(models_dir, "classifier.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model_artifact, f)

    print(f"Trained model saved successfully to: {model_path}")
    return acc, prec, rec, f1

if __name__ == "__main__":
    train_clause_classifier()
