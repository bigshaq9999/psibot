import requests

import os
import sys
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
parent_dir = os.path.dirname(current_dir)
commands_dir = os.path.join(parent_dir, 'commands')
sys.path.append(commands_dir)
from remove_tags import remove_tags


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
                    'ID 🔑': thread['no'],
                    'COMMENT 💬': remove_tags(thread['com']) if 'com' in thread else 'NO COMMENT',
                    'SUB': thread['sub'],
                    'REPLIES': thread['replies'],
                    'IMAGES 🖼️': thread['images']
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
