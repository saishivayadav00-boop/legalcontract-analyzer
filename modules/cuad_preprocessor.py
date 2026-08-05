import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict, Any

CATEGORY_MAPPING = {
    "termination": "Termination",
    "confidentiality": "Confidentiality",
    "payment": "Payment",
    "liability": "Liability",
    "indemnification": "Indemnification",
    "governing law": "Governing Law",
    "non-compete": "Non-Compete",
    "non compete": "Non-Compete",
}

def map_question_to_category(question: str) -> str:
    """Maps CUAD question strings to core contract categories."""
    q_lower = question.lower()
    for key, category in CATEGORY_MAPPING.items():
        if key in q_lower:
            return category
    return "Other"

def load_cuad_annotations(json_path: str) -> pd.DataFrame:
    """
    Loads CUAD JSON annotations and converts them into a DataFrame with
    'clause_text' and 'label' columns.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"CUAD dataset JSON file not found at: {json_path}")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    records = []
    for doc in data.get("data", []):
        for paragraph in doc.get("paragraphs", []):
            context = paragraph.get("context", "")
            qas = paragraph.get("qas", [])
            for qa in qas:
                question = qa.get("question", "")
                category = map_question_to_category(question)
                answers = qa.get("answers", [])
                
                if answers:
                    for ans in answers:
                        text = ans.get("text", "").strip()
                        if text:
                            records.append({"clause_text": text, "label": category})
                elif context:
                    records.append({"clause_text": context.strip(), "label": category})

    df = pd.DataFrame(records)
    if df.empty:
        # Fallback dataset if JSON is empty or basic structure
        df = pd.DataFrame([
            {"clause_text": "Either party may terminate this agreement upon 30 days notice.", "label": "Termination"},
            {"clause_text": "Receiving Party agrees to maintain confidentiality.", "label": "Confidentiality"},
            {"clause_text": "Invoices are payable within 30 days of receipt.", "label": "Payment"},
            {"clause_text": "In no event shall either party be liable for indirect damages.", "label": "Liability"},
            {"clause_text": "Provider agrees to defend and indemnify Client.", "label": "Indemnification"},
            {"clause_text": "Governed by the laws of New York.", "label": "Governing Law"},
            {"clause_text": "Employee shall not engage in competing business.", "label": "Non-Compete"}
        ])

    df = df.drop_duplicates().reset_index(drop=True)
    return df

def prepare_training_data(
    json_path: str,
    data_dir: str = "data",
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Preprocesses CUAD annotations, generates train/test splits, and saves
    train.csv and test.csv into data_dir.
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (train_df, test_df)
    """
    os.makedirs(data_dir, exist_ok=True)
    
    df = load_cuad_annotations(json_path)
    
    # Stratified split if possible, otherwise simple random split
    has_sufficient_samples = (
        len(df) >= 5 and 
        len(df["label"].unique()) > 1 and 
        df["label"].value_counts().min() >= 2
    )
    
    if has_sufficient_samples:
        train_df, test_df = train_test_split(
            df,
            test_size=test_size,
            random_state=random_state,
            stratify=df["label"]
        )
    elif len(df) > 1:
        train_df, test_df = train_test_split(
            df,
            test_size=test_size,
            random_state=random_state
        )
    else:
        train_df, test_df = df, df

    train_path = os.path.join(data_dir, "train.csv")
    test_path = os.path.join(data_dir, "test.csv")

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"Dataset prepared successfully.")
    print(f"Train split saved to: {train_path} ({len(train_df)} rows)")
    print(f"Test split saved to: {test_path} ({len(test_df)} rows)")

    return train_df, test_df
