import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

def  generate_financial_advice(financial_goals, transaction_history):
    """
     Generates personalized financial advice using the Gemini LLM.
    
    Args:
        financial_goals (str): The user's stated goals (e.g., "save for a house").
        transaction_history (str): A summary of the user's spending habits.
        
    Returns:
        str: A detailed, personalized portfolio recommendation.
    """
     # The key to getting a good response is a well-crafted prompt.
    # We give the model a persona ("expert financial advisor") and a clear task.

    prompt = f"""
    You are an expert financial advisor. Your goal is to provide personalized and actionable investment advice
    based on a user's financial goals and transaction history. Your advice should be clear, easy to understand
    for a beginner, and include specific portfolio recommendations.

    User's Financial Goals: {financial_goals}
    User's Recent Transaction History: {transaction_history}

    Please provide the following:
    1. A brief analysis of their spending habits in relation to their goals.
    2. A suggested portfolio allocation (e.g., 60% stocks, 30% bonds, 10% cash).
    3. A brief explanation for each asset class recommendation.
    4. A list of 3-5 potential investment opportunities that align with their goals and risk profile.
    """
     # Send the prompt to the Gemini model and get the response
    # The model will generate content based on the prompt we engineered.
    response = model.generate_content(prompt)

    return response.text

# --- Example Usage ---
if __name__ == "__main__":
    # You can change these to test different scenarios
    user_goals = "I want to save for a down payment on a house in 5 years and also start a retirement fund."
    user_transactions = """
    - Starbucks: $5 daily
    - Online shopping: $250 weekly
    - Groceries: $100 weekly
    - Gym membership: $50 monthly
    - Rent: $1500 monthly
    """
    
    advice = generate_financial_advice(user_goals, user_transactions)
    print("--- Personalized Financial Advice Report ---")
    print(advice)