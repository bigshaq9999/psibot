import requests

import os
import sys
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
parent_dir = os.path.dirname(current_dir)
commands_dir = os.path.join(parent_dir, 'commands')
sys.path.append(commands_dir)
from remove_tags import remove_tags


def get_thread_replies(board: str, thread_id: str) -> list:
    url = f'https://a.4cdn.org/{board}/thread/{thread_id}.json'
    thread_json = requests.get(url) 
    replies = thread_json.json()
    
    result = []
    
    for post in replies['posts']:
        post_info_dict = {
            "ID 🔑": post['no'],
            "TIME 🕖": post['time'],
            "COMMENT 💬": remove_tags(post['com']) if 'com' in post else 'NO COMMENT'
        }
        
        if 'filename' in post: 
            media_url = f"https://i.4cdn.org/{board}/{post['tim']}{post['ext']}\n"
            post_info_dict["FILENAME 🖼️"] = f"{post['filename']}{post['ext']}"
            post_info_dict["LINK 🌐"] = media_url
        
        result.append(post_info_dict)
    
    return result

if __name__ == '__main__':
    board = 'g'
    thread_id = 94474774
    replies_in_thread = get_thread_replies(board, thread_id)
    print(replies_in_thread)