import requests
import re
import html

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    text = html.unescape(text)
    return TAG_RE.sub('', text)

def get_thread_replies(board: str, thread_id: str) -> list:
    url = f'https://a.4cdn.org/{board}/thread/{thread_id}.json'
    thread_json = requests.get(url) 
    replies = thread_json.json()
    
    result = []
    
    for post in replies['posts']:
        post_info_list = [
            f"REPLY ID: {post['no']}",
            f"TIME: {post['time']}",
            f"\nCOMMENT: {remove_tags(post['com']) if 'com' in post else 'NO COMMENT'}\n",
        ]

        reply = '\n'.join(post_info_list)
        
        if 'filename' in post: 
            media_url = f"https://i.4cdn.org/{board}/{post['tim']}{post['ext']}\n"
            media_info_list = [
                f"MEDIA filename: {post['filename']}{post['ext']}",
                f"MEDIA link: {media_url}"
            ]
            media_sect = '\n'.join(media_info_list)
            reply += media_sect
        
        result.append(reply)
    
    return result

if __name__ == '__main__':
    board = 'g'
    thread_id = 94474774
    replies_in_thread = get_thread_replies(board, thread_id)
    for reply in replies_in_thread[0:3]:
        print(reply)