# News Scraping and Analysis Pipeline

## Setup & Usage

1. **Create/setup a virtual environment**  
   ```bash
   python3 -m venv venv
   source env/bin/activate
   pip3 install -r requirements.txt
   ```
2. **Environment Variables**  
   Create a .env file and set the `OPENAI_API_KEY`

4. **Usage**
   ```bash
   # run from step 1
   python3 main.py

   # run from a specific step
   python3 main.py [step number 1-5]
   ```

## Contributing  
- Scrape exact date/time from links in [step 2](https://github.com/Cardinal-Trading-UW-Madison/EDA/blob/c87c577efb7ed19c83bf0d2071e7b2985b5ffc7a/alternative_data/news_scrape/scrape/scrape_links.py#L9C5-L9C17)
- Method comments
- Typesafety
- Test different prompts/update prompt pipeline
