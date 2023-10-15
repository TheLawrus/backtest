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
- Method comments
- Typesafety
- Test different prompts/update prompt pipeline
