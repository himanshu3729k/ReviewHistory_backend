import os
from openai import OpenAI

def analyze_review_sentiment(text: str, stars: int):
    """
    Attempts to use OpenAI for sentiment analysis.
    Falls back to a mock response if the API key is missing or invalid.
    """
    if not text:
        return "Neutral", "Neutral"

    api_key = os.environ.get("OPENAI_API_KEY")
    
    # Fallback 1: No API key provided
    if not api_key:
        print("WARNING: OPENAI_API_KEY not found. Using mock LLM response.")
        return _mock_sentiment(stars)

    client = OpenAI(api_key=api_key)
    prompt = f"Analyze the following review which gave {stars} out of 10 stars. Text: '{text}'. Provide the 'tone' (e.g., frustrated, happy, formal) and 'sentiment' (Positive, Negative, Neutral) separated by a comma. Example output: 'Frustrated, Negative'."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.3
        )
        result = response.choices[0].message.content.strip()
        parts = [p.strip() for p in result.split(",")]
        if len(parts) == 2:
            return parts[0], parts[1]
        return "Unknown", "Unknown"
        
    except Exception as e:
        # Fallback 2: The API key was provided but is invalid or the network failed
        print(f"WARNING: OpenAI API call failed ({e}). Using mock LLM response.")
        return _mock_sentiment(stars)

def _mock_sentiment(stars: int):
    """Helper function to generate a realistic mock response."""
    if stars >= 8:
        return "Happy", "Positive"
    elif stars <= 4:
        return "Frustrated", "Negative"
    else:
        return "Objective", "Neutral"