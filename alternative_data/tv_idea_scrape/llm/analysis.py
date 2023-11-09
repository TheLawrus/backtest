import openai
import json
from config import JSON_OUTPUT, OPENAI_API_KEY, OPENAI_MODEL

openai.api_key = OPENAI_API_KEY


PROMPT = """
The information provided below reflects a complex set of conditions \
that could potentially impact a broad range of financial \
markets, including stocks. Provide a short breakdown of the kinds \
of stocks that could be influenced by each factor:
{sentiment}
"""

def main():
    with open(f"{JSON_OUTPUT}_step3.json", "r") as f:
        data = json.load(f)
    
    i = 1
    for d in data:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {
                "role": "system",
                "content": "You are a financial analyst."
                },
                {
                "role": "assistant",
                "content": "Understood. I will respond with a dashed list."
                },
                {
                "role": "user",
                "content": PROMPT.format(sentiment=d["excerpt_keywords"])
                }
            ],
            temperature=1.25,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(f"Generated Analysis: {i}")
        d["analysis"] = response["choices"][0]["message"]["content"]
        
        i += 1

    with open(f"{JSON_OUTPUT}_step4.json", "w") as json_file:
        json.dump(data, json_file, default=str)