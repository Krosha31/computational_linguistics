# # from newsapi import NewsApiClient

# # # Init
# # newsapi = NewsApiClient(api_key='55709e6437514ab590f10a54841520e2')

# # top_headlines = newsapi.get_top_headlines(q='bitcoin',
# #                                           category='business',
# #                                           language='en',
# #                                           country='us')

# # all_articles = newsapi.get_everything(q='bitcoin',
# #                                       sources='bbc-news,the-verge',
# #                                       domains='bbc.co.uk,techcrunch.com',
# #                                       language='en',
# #                                       sort_by='relevancy',
# #                                       page=2)

# # sources = newsapi.get_sources()

# # print(all_articles)


# import requests
# import json

# def fetch_news(api_key, category, page):
#     url = f'https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}&page={page}'
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Error fetching news: {response.status_code}")
#         return None

# # def extract_articles(news_data):
# #     articles = []
# #     if news_data and 'articles' in news_data:
# #         for article in news_data['articles']:
# #             title = article.get('title')
# #             description = article.get('description')
# #             content = article.get('content')
# #             tags = []  # Здесь вы можете добавить логику для извлечения тегов, если они доступны
            
# #             # Пример: если у вас есть способ извлечь теги из текста
# #             # tags = extract_tags_from_text(content)
            
# #             articles.append({
# #                 'title': title,
# #                 'description': description,
# #                 'content': content,
# #                 'tags': tags
# #             })
# #     return articles

# # def main():
# #     query = 'technology'  # Замените на нужный вам запрос
# #     news_data = fetch_news(api_key, query)
    
# #     articles = extract_articles(news_data)
    
# #     for article in articles:
# #         print(f"Title: {article['title']}")
# #         print(f"Description: {article['description']}")
# #         print(f"Content: {article['content']}")
# #         print(f"Tags: {article['tags']}")
# #         print('-' * 80)

# # if __name__ == '__main__':
# #     main()



# api_key = ""
# with open("apikey") as f:
#     api_key = f.read()

# categories = ["politics", "business"]
# with open("result.json", "w") as f:
#     for category in categories:
#         articles = 0
#         page = 1
#         while articles < 1000:
#             results = fetch_news(api_key, category, page)["articles"]
#             print(results[0]["content"])
#             break
#             articles += len(results)
#             page += 1
#             for article in results["articles"]:
#                 article_new = {
#                     "article_id": article["url"],
#                     "title": article["title"],
#                     "category": category
#                 }
#                 json.dump(article_new, f, indent=4)
#                 f.write("\n")



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