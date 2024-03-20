from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import json
from scrape.utils import convert_time_string
from config import SCROLL_COUNT, CHROME_OPTIONS, JSON_OUTPUT

def setup_driver():
    options = webdriver.ChromeOptions()
    for opt in CHROME_OPTIONS:
        options.add_argument(opt)
    return webdriver.Chrome(options=options)

def extract_link_data(box):
    link_dict = {"link": None, "publisher": None, "date": None, "type": None}
    s = box.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    box_text = re.split('\n', box.text)

    for string in box_text:
        if "•" in string:
            link_data = string.split("•")
            link_dict["publisher"] = link_data[0]
            link_dict["date"] = convert_time_string(link_data[1])

    return s, link_dict

def main():
    driver = setup_driver()

    # Navigate
    driver.get(f'https://finance.yahoo.com/news/')

    time.sleep(2)
    height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(SCROLL_COUNT):
        driver.execute_script(f"window.scrollBy(0, {height*5});")
        time.sleep(1)

    news_boxes = driver.find_elements(By.CLASS_NAME, 'Cf')
    patterns = {
        "news": re.compile(r'https://finance\.yahoo\.com/news/.+\.html'),
        "media": re.compile(r'https://finance\.yahoo\.com/m/.+\.html'),
        "video": re.compile(r'https://finance\.yahoo\.com/video/.+\.html'),
    }

    news_links = []

    for box in news_boxes:
        link, link_dict = extract_link_data(box)
        for category, pattern in patterns.items():
            if pattern.match(link):
                link_dict["link"] = link
                link_dict["type"] = category
                news_links.append(link_dict)
                break

    # Remove duplicates
    unique_links = {}
    for d in news_links:
        link = d["link"]
        if link not in unique_links:
            unique_links[link] = d
        else:
            existing_entry = unique_links[link]
            if existing_entry["publisher"] is None and d["publisher"] is not None:
                unique_links[link] = d
                
    news_links = list(unique_links.values())

    with open(JSON_OUTPUT + "_step1.json", "w") as json_file:
        json.dump(news_links, json_file, default=str)

    driver.quit()

if __name__ == "__main__":
    main()