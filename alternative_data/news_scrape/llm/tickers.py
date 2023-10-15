import openai
import json
from config import JSON_OUTPUT, OPENAI_API_KEY, OPENAI_MODEL

openai.api_key = OPENAI_API_KEY

PROMPT = """
The information provided below reflects a complex set of conditions \
that could potentially impact a broad range of financial \
markets, including stocks. It's important to note that market conditions \
are subject to change, and individual stocks can be influenced by a \
variety of factors. However, based {analysis}, provide some sector I \
could broadly look into and some sample tickers for each sector. \
Also provide a few word brief reason for each ticker.

PROVIDE ONLY MAXIMUM {count} TICKERS. NO MORE.

Respond ONLY in JSON format with the keys being the sector, the values, \
being a dict that has the tickers and its reason.

Example:
{{
    "Companies impacted by the Israel-Hamas conflict": {{
        "MDT": "The Medtronic stock may be impacted by the Israel-Hamas conflict due to potential disruptions in its operations or supply chain in the region.",
        "BLMIF": "The Bank Leumi stock may be impacted by the Israel-Hamas conflict due to increased geopolitical risk affecting investor sentiment and the bank's operations."
    }}
}}
"""

def main():
    with open(f"{JSON_OUTPUT}_step4.json", "r") as f:
        data = json.load(f)
        
    for d in data:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {
                "role": "system",
                "content": "You are a financial analyst. Respond in JSON format."
                },
                {
                "role": "assistant",
                "content": "Understood. I will respond in JSON format."
                },
                {
                "role": "user",
                "content": PROMPT.format(analysis=d["analysis"], count=10)
                }
            ],
            temperature=1.25,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(response["choices"][0]["message"]["content"])
        d["tickers"] = json.loads(response["choices"][0]["message"]["content"])

    with open(f"{JSON_OUTPUT}_step5.json", "w") as json_file:
        json.dump(data, json_file, default=str)