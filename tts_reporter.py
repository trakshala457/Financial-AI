import os
from gtts import gTTS
import gtts
print(gtts.__version__)
def generate_audio_report(text_report, filename="daily_report.mp3"):
    """
    Convert a text into MP3 audio file.

    Args: 
        text_Report (str): The text content to be spotken.
        filename (str): The name of the output MP3 file.
    """
    try:
        tts = gTTS(text=text_report, lang='en')

        tts.save(filename)
        print(f"Daily financila report saved to {filename}")

    except Exception as e:
        print(f"Error generating audio report: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    # This is a sample text report, which could be the output from your
    # financial advisor agent.
    sample_report = """
    Hello! Here is your daily financial health report. 
    Based on your spending, you are on track to meet your home savings goal. 
    We have detected two potential anomalies in your recent transactions: a transfer to a cryptocurrency wallet and an international flight purchase. 
    Please review these to ensure they are legitimate.
    """
    
    generate_audio_report(sample_report)