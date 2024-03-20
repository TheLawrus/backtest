import openai
import json
import os
from dotenv import load_dotenv

load_dotenv() 


file_path = "redditor.json"

with open(file_path, "r") as f:
    redditor_data = json.load(f)

print(len(redditor_data))

config_prompt="""
You are an expert stock market psychologist specializing in the analysis of Reddit data, your mission is to delve into the collective psyche of online investors, decode their cognitive biases, and distill actionable insights for navigating financial markets. 
 Through a keen understanding of the intricate interplay between investor psychology and market dynamics, your goal is to empower traders with information that transcends the noise, enabling them to make more informed and rational investment decisions.
 In a world influenced by cognitive traps, you strive to elevate consciousness, promote critical thinking, and foster a community of investors attuned to both the art and science of trading.
  You are provided with a Reddit discussion, through which you aim to uncover hidden patterns, identify prevailing behavioral biases,
    and provide explicit stock tickers paired with sentiments in a format such as [["Ticker1", "Sentiment regarding that ticker"], ["Ticker2", "Sentiment regarding that ticker"], ...].
    """



def llm_parser(comments):
  system_prompt=config_prompt
  user_prompt=f"""
                You are now the Reddit expert stock market psychologist. All messages must be in the following format:
                User: {comments}
                Stock Market Psychologist: [output]
    """
  openai.api_key = os.getenv("OPENAI_API_KEY")
  completion=openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    max_tokens=200,
    temperature=0
  )
  response = completion.choices[0].message.content
  return response

for each_post in redditor_data:
    comments="".join(each_post["opinions"])
    output=llm_parser(comments)
    print(output)
