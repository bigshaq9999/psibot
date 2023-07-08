import requests
import re
import html
from bs4 import BeautifulSoup

def remove_tags(text:str):
    text = re.sub(r'<wbr>', '', text)
    text = html.unescape(text)
    text = text.replace('\\/', '/')
    soup = BeautifulSoup(text, 'html.parser')
    plain_text = soup.get_text(separator='\n')
    return plain_text

def generate_catalog(board: str, keyword: str) -> list:
    url = f'https://a.4cdn.org/{board}/catalog.json'
    response = requests.get(url)
    data = response.json()
    
    catalog = []

    for page in data:
        threads = []
        for thread in page['threads']:
            if 'sub' in thread and keyword.lower() in thread['sub'].lower():
                thread_info_dict = {
                    'ID': thread['no'],
                    'SUB': thread['sub'],
                    'STATUS': 'closed 🔒' if 'closed' in thread else 'alive 🔓',
                    'REPLIES': thread['replies'],
                    'IMAGES': thread['images'],
                    'COMMENT': remove_tags(thread['com']) if 'com' in thread else 'NO COMMENT'
                }
                # thread_info = "\n".join(thread_info_dict)
                threads.append(thread_info_dict)
        catalog.append({'page': page['page'], 'threads': threads})

    return catalog


if __name__ == '__main__':
    board = 'g'
    catalog = generate_catalog(board, "general")
    for page in catalog:
        # print(f"PAGE {page['page']}\n\n")
        for thread in page['threads']:
            for key, element in thread.items():
                print(key, element)