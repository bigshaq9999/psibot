import requests
import re
import html


TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    text = html.unescape(text)
    # return text
    return TAG_RE.sub('', text)

def generate_catalog(board: str, keyword: str) -> list:
    url = f'https://a.4cdn.org/{board}/catalog.json'
    response = requests.get(url)
    data = response.json()
    
    catalog = []

    for page in data:
        threads = []
        for thread in page['threads']:
            if 'sub' in thread and keyword in thread['sub']:
                thread_info_list = [
                    f"ID: {thread['no']}",
                    f"SUB: {thread['sub']}",
                    f"STATUS: {'closed 🔒' if 'closed' in thread else 'alive 🔓'}",
                    f"REPLIES: {thread['replies']}",
                    f"IMAGES: {thread['images']}",
                    f"\nCOMMENT: {remove_tags(thread['com'][:2000]) if 'com' in thread else 'NO COMMENT'}\n"
                ]
                thread_info = "\n".join(thread_info_list)
                threads.append(thread_info)
        catalog.append({'page': page['page'], 'threads': threads})

    return catalog


if __name__ == '__main__':
    board = 'g'
    catalog = generate_catalog(board, "general")
    for page in catalog:
        # print(f"PAGE {page['page']}\n\n")
        for thread in page['threads']:
            print(thread)