import html
from bs4 import BeautifulSoup
import re

def remove_tags(text:str):
    text = re.sub(r'<wbr>', '', text)
    text = html.unescape(text)
    text = text.replace('\\/', '/')
    soup = BeautifulSoup(text, 'html.parser')
    plain_text = soup.get_text(separator='\n')
    return plain_text

if __name__ == '__main__':
    pass