import requests
from bs4 import BeautifulSoup
import random
import json
import time
from config import JSON_OUTPUT


def extract_text(url):
    # List of User-Agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537',
        # Add more user agents here
    ]

    # Loop through URLs
    headers = {'User-Agent': random.choice(user_agents)}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Assuming news links are in <a> tags with a specific class (this is just an example; the actual structure may be different)
        body = soup.select("div.caas-body")[0]
        text = body.select("p")
        
        res = ""
        for t in text:
            res += f" {t.text}"
            
        return res

def main():
    with open(f"{JSON_OUTPUT}_step1.json", "r") as f:
        data = json.load(f)
        
    i = 0
    for url in data:
        textdata = extract_text(url["link"])
        url["text"] = textdata
        i+=1
        print(f"scraped: {i}")
        time.sleep(3)
            
    with open(f"{JSON_OUTPUT}_step2.json", "w") as json_file:
            json.dump(data, json_file, default=str)
            
if __name__ == "__main__":
    main()