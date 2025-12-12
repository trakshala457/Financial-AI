import os
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS
import gtts
print(gtts.__version__)
# def generate_audio_report(text_report, filename="daily_report.mp3"):
#     """
#     Convert a text into MP3 audio file.

#     Args: 
#         text_Report (str): The text content to be spotken.
#         filename (str): The name of the output MP3 file.
#     """
#     try:
#         tts = gTTS(text=text_report, lang='en')

#         tts.save(filename)
#         print(f"Daily financila report saved to {filename}")

#     except Exception as e:
#         print(f"Error generating audio report: {e}")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def get_latest_finance_news_text(filename="daily_report.mp3"):
    """
    Uses Gemini to create a short finance/market-style brief and returns the text.
    """
    prompt = """
    You are a friendly financial news presenter. Give a concise spoken-style
    market update that sounds like a daily brief for listeners.

    Include:
    - Overall global stock market mood (e.g., mostly positive, mixed, or under pressure)
    - A brief mention of either the tech sector or banking sector
    - A short line about crypto market trend
    - One or two high-level macro themes (inflation, interest rates, or economic growth)

    Constraints:
    - Keep it under 10000 words (so the resulting audio stays under ~3 minutes and above ~ 90seconds).
    - Use simple, conversational English suitable for audio narration.
    - Do NOT mention exact index values, specific dates, or stock tickers.
    """

    try:
        response = model.generate_content(prompt)
        # response.text contains the generated string
        news_text = getattr(response, "text", None) or (response.get("output") if isinstance(response, dict) else str(response))
        tts = gTTS(text=news_text, lang='en')
        tts.save(filename)
        print(f"Daily financila report saved to {filename}")
    except Exception as e:
        news_text = """"Here is a short finance update. Global markets were mixed today as investors "
            "balanced economic data and corporate earnings. Technology stocks showed modest moves, "
            "banks were steady, and crypto remained relatively range-bound. Keep an eye on "
            "inflation and central bank commentary for the week ahead."""
        tts = gTTS(text=news_text, lang='en')
        tts.save(filename)
        print(f"Error occured {e}\n Daily financila report saved to {filename}")

# --- Example Usage ---
if __name__ == "__main__":
    # This is a sample text report, which could be the output from your
    # financial advisor agent.
    # sample_report = """
    # Hello! Here is your daily financial health report. 
    # Based on your spending, you are on track to meet your home savings goal. 
    # We have detected two potential anomalies in your recent transactions: a transfer to a cryptocurrency wallet and an international flight purchase. 
    # Please review these to ensure they are legitimate.
    # """
    get_latest_finance_news_text()
    # generate_audio_report(sample_report)