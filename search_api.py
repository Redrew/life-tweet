from googlesearch import search  # pip install googlesearch-python
import requests
from bs4 import BeautifulSoup
from openai_api import get_chat_gpt_output


def get_title(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    page_titles = []
    for title in soup.find_all('title'):
        page_titles.append(title.get_text())
    return '|'.join(page_titles[:3])


def google_search(diff, num_results=3, verbose=False):
    query = get_chat_gpt_output(f"Given that you learned this user information recently: {diff}, give"
                                f"the user an interesting followup question",
                                top_p=0.6)
    if verbose:
        print(query)

    search_results = list(search(query, num_results=num_results))
    search_titles = list(map(get_title, search_results))
    return list(zip(search_titles, search_results))

if __name__ == "__main__":
    # query = input("Enter your search query: ")
    diff = "Alex started playing frisbee"
    # diff = "Alex bought a squash racket"
    results = google_search(diff, num_results=2)

    if results:
        for i, (title, url) in enumerate(results, start=1):
            print(f"{i}. {title}. {url}")
    else:
        print("No results found.")
