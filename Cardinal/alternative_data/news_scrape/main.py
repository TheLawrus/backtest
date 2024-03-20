import argparse
from scrape.extract_links import main as extract_links_main
from scrape.scrape_links import main as scrape_links_main
from llm.extractor import main as extractor_main
from llm.analysis import main as analysis_main
from llm.tickers import main as tickers_main

def run_steps(start_from=0):
    steps = [
        {"name": "Step 1: Extract Links", "function": extract_links_main},
        {"name": "Step 2: Scrape Links", "function": scrape_links_main},
        {"name": "Step 3: Extractor", "function": extractor_main},
        {"name": "Step 4: Analysis", "function": analysis_main},
        {"name": "Step 5: Tickers", "function": tickers_main}
    ]
    
    for _, step in enumerate(steps[start_from:], start=start_from):
        try:
            print(f"Running {step['name']}...")
            step['function']()
            print(f"{step['name']} completed.")
        except Exception as e:
            print(f"Error encountered at {step['name']}. Error message: {e}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run different steps.')
    parser.add_argument('step', type=int, nargs='?', default=1,
                        help='an integer for the accumulator (default: 1)')
    
    args = parser.parse_args()
    run_steps(args.step-1)
