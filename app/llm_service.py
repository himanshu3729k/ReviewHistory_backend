import os
from openai import OpenAI

# It is best practice to load this from an environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-fallback-key"))

def analyze_review_sentiment(text: str, stars: int):
    """Calls OpenAI to determine tone and sentiment."""
    if not text:
        return "Neutral", "Neutral"
        
    prompt = f"Analyze the following review which gave {stars} out of 10 stars. Text: '{text}'. Provide the 'tone' (e.g., frustrated, happy, formal) and 'sentiment' (Positive, Negative, Neutral) separated by a comma. Example output: 'Frustrated, Negative'."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.3
        )
        result = response.choices[0].message.content.strip()
        # Parse the comma-separated result
        parts = [p.strip() for p in result.split(",")]
        if len(parts) == 2:
            return parts[0], parts[1]
        return "Unknown", "Unknown"
    except Exception as e:
        print(f"LLM Error: {e}")
        return "Error", "Error"