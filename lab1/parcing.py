from bs4 import BeautifulSoup
import requests
import json
import os


categories = {
    "science": "https://lenta.ru/rubrics/science/science/",
    "history": "https://lenta.ru/rubrics/science/history/",
    "football": "https://lenta.ru/rubrics/sport/football/",
    "economics": "https://lenta.ru/rubrics/economics/economy/"
}

if "articles_links.json" not in os.listdir():
    out = []
    for category, url in categories.items():
        page = 1
        total_results = 0
        while total_results < 1000:
            result = requests.get(url + f'{page}/')
            soup = BeautifulSoup(result.text, "html.parser")
            allNews = soup.findAll('a', class_='card-full-news')
            allNews = str(allNews).split("</a>, <a ")
            print(category, total_results)
            for i in range(len(allNews)):
                allNews[i] = {
                    "link" : allNews[i].split('class="card-full-news _subrubric" href="')[1].split('"><h3 class="card-full-news__title"')[0],
                    "category": category
                }
                out.append(allNews[i])
            page += 1
            total_results += len(allNews)

    with open("articles_links.json", "w") as f:
        json.dump(out, f, indent=4)

if "data.json" not in os.listdir():
    with open("articles_links.json") as f:
        data = json.load(f)

    with open("data.json", "w", encoding='utf-8') as f:
        f.write("[\n")
        total_articles = 0
        for article in data:
            total_articles += 1
            if total_articles % 100 == 0:
                print(total_articles)
            url = "https://lenta.ru" + article["link"]
            result = requests.get(url)
            soup = BeautifulSoup(result.text, "html.parser")
            html_text = str(soup.findAll('p', class_='topic-body__content-text'))

            html_text = html_text.strip('[]')
            html_parts = html_text.split(', ')

            cleaned_text = ''
            for part in html_parts:
                soup2 = BeautifulSoup(part, 'html.parser')
                cleaned_text += soup2.get_text() + ' '

            cleaned_text = ' '.join(cleaned_text.split())

            title = str(soup).split('ogTitle": "')[1].split('",')[0]
            article_new = {
                "article_id": url,
                "title": title,
                "category": article["category"],
                "tags": [],
                "text": cleaned_text
            }
            json.dump(article_new, f, indent=4, ensure_ascii=False)
            if total_articles != len(data):
                f.write(",\n")
        f.write("\n]")        