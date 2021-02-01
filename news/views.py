from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views import View
from datetime import datetime
import itertools
import json
from random import randint

# settings.NEWS_JSON_PATH
path_for_json = 'C:/Users/Siyovush/PycharmProjects/HyperNews Portal/HyperNews Portal/task/news.json'
with open(path_for_json, "r") as json_file:
    articles = json.load(json_file)

articles_list = articles
COUNTER = len(articles)
articles = {article['link']: article for article in articles}


# Create your views here.
class NewsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            data = self.search(query)
            data = self.grouped_news(data)
        else:
            data = self.grouped_news(articles_list)
        context = {'articles': data}
        return render(request, "news/index.html", context=context)

    def grouped_news(self, data):
        sorted_news = sorted(data, key=lambda i: i['created'], reverse=True)
        grouped_news = []
        for group, item in itertools.groupby(sorted_news,
                                             lambda i: i['created'][:10]):
            grouped_news.append([group, list(item)])
        return grouped_news

    def search(self, query):
        result = []
        for article in articles_list:
            if query in article['title']:
                result.append(article)
        return result


class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")


class ArticleView(View):
    def get(self, request, article_id, *args, **kwargs):
        if article_id not in articles:
            raise Http404
        context = {"article": articles[int(article_id)]}
        return render(request, "news/news.html", context=context)





class CreateArticleView(View):
    links = set(articles.keys())

    def get(self, request, *args, **kwargs):
        return render(request, "news/create_article.html")

    def post(self, request, *args, **kwargs):
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = request.POST.get('title')
        text = request.POST.get('text')
        link = len(articles_list) + 1
        article = {
            'created': created,
            'title': title,
            'text': text,
            'link': link
        }
        articles[link] = article
        articles_list.append(article)
        print(articles)
        return redirect('/news/')

    def generate_link(self):
        link = randint(1, 100000)
        while link in self.links:
            link = randint(1, 100000)
            if link not in self.links:
                self.links.add(link)
        self.links.add(link)
        return link
