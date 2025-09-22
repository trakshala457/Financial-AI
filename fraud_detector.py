import os
from dotenv import load_dotenv
import google.generativeai as genai
from sklearn.ensemble import IsolationForest
import numpy as np

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

def get_transaction_embeddings(transactions):
    """
    Converts a list of transaction descriptions into a list of numerical embeddings.
    Args:
        transactions (list of str): A list of transaction descriptions.

    Returns:
        list of list of float: A list of embedding vectors.
    """

    # We use a dedicated embedding model for this task.
    # The 'models/embedding-001' is a powerful, general-purpose model.
    # The 'TASK_TYPE_UNSPECIFIED' is good for general similarity searches.
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=transactions,
            task_type="TASK_TYPE_UNSPECIFIED"
        )
         # Extract the embeddings from the response and return them as a NumPy array.
        # NumPy is a standard library for numerical operations in Python.
        return np.array(response['embedding'])
    except Exception as e:
        print(f"Error getting embeddings: {e}")
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
# if __name__ == "__main__":
#     # This is a mock list of transactions.
#     # Notice the last two transactions are "unusual" compared to the rest.
#     mock_transactions = [
#         "groceries at local market",
#         "coffee at starbucks",
#         "gas station purchase",
#         "dinner at a restaurant",
#         "online clothes shopping",
#         "subscription to streaming service",
#         "groceries at local market",
#         "transfer to cryptocurrency wallet", # Anomaly 1
#         "international flight ticket purchase" # Anomaly 2
#     ]
    
#     print("Step 1: Getting embeddings for transactions...")
#     transaction_embeddings = get_transaction_embeddings(mock_transactions)
    
#     if transaction_embeddings is not None:
#         print("Step 2: Detecting anomalies using Isolation Forest...")
#         anomalies = detect_anomalies(transaction_embeddings)
        
#         if anomalies:
#             print("\n--- Suspicious Transactions Detected! ---")
#             for index in anomalies:
#                 print(f"Index {index}: '{mock_transactions[index]}' has been flagged.")
#             print("\nAction: Alert the user and request verification.")
#         else:
#             print("\nNo suspicious transactions detected.")