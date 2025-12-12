import os
from dotenv import load_dotenv
import google.generativeai as genai
from sklearn.ensemble import IsolationForest
import numpy as np
from sentence_transformers import SentenceTransformer

_sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_transaction_embeddings(transactions):
    """
    Local fallback: use sentence-transformers to create embeddings
    transactions: list[str]
    returns: numpy.ndarray shape (n, dim)
    """
    try:
        embeddings = _sbert_model.encode(transactions, show_progress_bar=False)
        return np.array(embeddings)
    except Exception as e:
        print("Local embedding error:", e)
        return None

def detect_anomalies(embeddings):
    """
    Uses Isolation Forest to detect anomalous embeddings.

    Args:
        embeddings (numpy.ndarray) : A 2D array of transaction embeddings.

    Returns:
        list of int: The indices of the transactions flagged as anomalies.
    """
    # Isolation Forest is an unsupervised algorithm, meaning it doesn't need
    # pre-labeled data (like "fraud" or "not fraud"). It finds outliers automatically.

     # We set 'contamination' to a small value (e.g., 0.01 or 1%). This is the
    # expected proportion of outliers in the data. You can tune this value.
    # contamination : It tells the model what fraction of your dataset you expect to be “anomalies” (fraud / outliers).
    model = IsolationForest(contamination=0.01)

    # The fit_predict method trains the model and makes predictions at the same time.
    # It returns 1 for inliers (normal transactions) and -1 for outliers (anomalies).
    predictions = model.fit_predict(embeddings)

    anomaly_indices = np.where(predictions == -1)[0]

    return anomaly_indices.tolist()
    # tolist(): that converts a NumPy array into a standard Python list.



# # --- Example Usage ---
if __name__ == "__main__":
    # This is a mock list of transactions.
    # Notice the last two transactions are "unusual" compared to the rest.
    mock_transactions = [
        "groceries at local market",
        "coffee at starbucks",
        "gas station purchase",
        "dinner at a restaurant",
        "online clothes shopping",
        "subscription to streaming service",
        "groceries at local market",
        "transfer to cryptocurrency wallet", # Anomaly 1
        "international flight ticket purchase" # Anomaly 2
    ]
    
    print("Step 1: Getting embeddings for transactions...")
    transaction_embeddings = get_transaction_embeddings(mock_transactions)
    
    if transaction_embeddings is not None:
        print("Step 2: Detecting anomalies using Isolation Forest...")
        anomalies = detect_anomalies(transaction_embeddings)
        
        if anomalies:
            print("\n--- Suspicious Transactions Detected! ---")
            for index in anomalies:
                print(f"Index {index}: '{mock_transactions[index]}' has been flagged.")
            print("\nAction: Alert the user and request verification.")
        else:
            print("\nNo suspicious transactions detected.")