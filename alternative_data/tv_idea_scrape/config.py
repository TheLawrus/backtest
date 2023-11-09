from dotenv import load_dotenv
import os

load_dotenv()

# Configuration variables
SCROLL_COUNT = 20 # grabs more links, generally #links = 20 + SCROLL_COUNT * 10
CHROME_OPTIONS = ['--disable-gpu', "--headless"]
JSON_OUTPUT = "data" # JSON header, do not include the .json
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"
TEST_MODE = True # if you turn this off, expect a $5 charge on openai every time you run itç