from browser_history import get_history
from browser_history import get_bookmarks
from browser_history.browsers import Chrome
import requests
import html2text
import pickle

htext_obj = html2text.HTML2Text()
htext_obj.ignore_links = True

def get_all_history(browser_type='all', restrict_bookmarks=False):
    if browser_type == 'all':
        outputs = get_history()
    elif browser_type == "Chrome":
        outputs = Chrome().fetch_history()
    else:
        return [
            (0, "https://www.nytimes.com/live/2023/10/14/world/israel-news-hamas-war-gaza", "Israel"),
            (1, "https://www.forbes.com/sites/tomsanderson/2023/10/13/fc-barcelona-captain-sergi-roberto-agrees-to-leave-club-reports/", "Barcelona Soccer")
            (2, "https://en.wikipedia.org/wiki/Latent_space", "Latent space")
        ]
    user_data = outputs.histories
    print(f'Read {len(user_data)} links')
    return user_data  # [datetime.datetime, url, title, folder]


def get_summary_from_html(html: str) -> str:
    # input is html text with tags, output is cleaned [text] segments
    scraped_text = htext_obj.handle(html)
    # get_chat_gpt_output(f"{}")
    return scraped_text


def scrape_websites(history):
    raw_html = []
    for datetime, url, title in history:
        print(title)
        try:
            f = requests.get(url)
            raw_html.append(f.text)
        except requests.exceptions.InvalidSchema as e:
            print(f"Couldn't read website {url}")
    return raw_html


def get_data_from_browser(browser_type='all'):
    history = get_all_history(browser_type=browser_type)
    raw_html = scrape_websites(history)
    print('parsing texts scraped from html')
    website_texts = [get_summary_from_html(html) for html in raw_html]
    return website_texts

if __name__ == '__main__':
    website_texts = get_data_from_browser(browser_type='fake')
    print(website_texts)