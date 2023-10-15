import json
from collections import defaultdict
from scraper_main import *
from life_summarizer import add_deltas

if __name__ == "__main__":
    profile = json.load(open("example/profile.json"))
    website_texts = get_data_from_browser(use_recent=True, time_limit=240, browser_type='Chrome')[-5:] # HACK
    print(f"getting deltas for {len(website_texts)} websites")
    print(website_texts)
    deltas = defaultdict(list)
    for website_text in website_texts:
        add_deltas(profile, website_text, deltas)
    print("deltas:")
    print(deltas)
    print("Confirming deltas on frontend...")

