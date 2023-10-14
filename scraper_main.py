from browser_history import get_history
from browser_history import get_bookmarks
from browser_history.browsers import *
import requests
import html2text

htext_obj = html2text.HTML2Text()
htext_obj.ignore_links = True

def get_all_history(browser_type='all', restrict_bookmarks=False):
    if browser_type != 'all':
        try:
            f = eval(f'{browser_type}()')
        except:
            raise ValueError()
        outputs = f.fetch_history()
    else:
        outputs = get_history()
    user_data = outputs.histories
    return user_data  # [datetime.datetime, url, title, folder]


def get_text_from_html(html: str) -> str:
    # input is html text with tags, output is cleaned [text] segments
    scraped_text = htext_obj.handle(html)
    return scraped_text


def scrape_websites(history):
    raw_html = []
    for datetime, url, title in history:
        try:
            f = requests.get(url)
            raw_html.append(f.text)
        except requests.exceptions.InvalidSchema as e:
            print("Couldn't read website")


def get_data_from_browser(browser_type='all'):
    history = get_all_history(browser_type=browser_type)
    raw_html = scrape_websites(history)
    website_texts = [get_text_from_html(html) for html in raw_html]
    return website_texts

if __name__ == '__main__':
    website_texts = get_data_from_browser(browser_type='Edge')
    print(website_texts)