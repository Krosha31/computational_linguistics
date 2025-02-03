# from newsapi import NewsApiClient

# # Init
# newsapi = NewsApiClient(api_key='55709e6437514ab590f10a54841520e2')

# top_headlines = newsapi.get_top_headlines(q='bitcoin',
#                                           category='business',
#                                           language='en',
#                                           country='us')

# all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=2)

# sources = newsapi.get_sources()

# print(all_articles)


import requests

def fetch_news(api_key, category):
    url = f'https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}&pageSize=100'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching news: {response.status_code}")
        return None

# def extract_articles(news_data):
#     articles = []
#     if news_data and 'articles' in news_data:
#         for article in news_data['articles']:
#             title = article.get('title')
#             description = article.get('description')
#             content = article.get('content')
#             tags = []  # Здесь вы можете добавить логику для извлечения тегов, если они доступны
            
#             # Пример: если у вас есть способ извлечь теги из текста
#             # tags = extract_tags_from_text(content)
            
#             articles.append({
#                 'title': title,
#                 'description': description,
#                 'content': content,
#                 'tags': tags
#             })
#     return articles

# def main():
#     query = 'technology'  # Замените на нужный вам запрос
#     news_data = fetch_news(api_key, query)
    
#     articles = extract_articles(news_data)
    
#     for article in articles:
#         print(f"Title: {article['title']}")
#         print(f"Description: {article['description']}")
#         print(f"Content: {article['content']}")
#         print(f"Tags: {article['tags']}")
#         print('-' * 80)

# if __name__ == '__main__':
#     main()



api_key = '55709e6437514ab590f10a54841520e2'  # Замените на ваш API ключ

results = fetch_news(api_key, "business")
print(len(results["articles"]))
with open("result.json", "w") as f:
    for article in results["articles"]:
        article_new = {
            "article_id": article["url"],
            "title": article["title"],
            "category": article[:]
        }
        print(article)
        break