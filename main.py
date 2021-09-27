from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse   import quote
import json

def parse_page(path):
    html = urlopen(path)
    bs = BeautifulSoup(html.read(), 'html.parser')
    article_titles = bs.findAll('h2', {'class': 'tm-article-snippet__title tm-article-snippet__title_h2'})
    authors = bs.findAll('a', {'class': 'tm-user-info__username'})
    links = bs.find_all('a', {'class': 'tm-article-snippet__title-link'}, href=True)
        
    data = []

    for i in range(len(article_titles)):
        data.append({
            'title': article_titles[i].get_text(),
            'author': authors[i].get_text().replace('\n', '').strip(' '),
            'link': 'https://habr.com' + links[i]['href']
        })

    return data

data = parse_page('https://habr.com/ru/search/?q=' + quote('Парсинг') + '&target_type=posts&order=relevance')
data += parse_page('https://habr.com/ru/search/page2/?q=' + quote('Парсинг') + '&target_type=posts&order=relevance')  
data += parse_page('https://habr.com/ru/search/page3/?q=' + quote('Парсинг') + '&target_type=posts&order=relevance')  
    
with open('data.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=2, separators=(',', ':'))

print('parsing is done')
