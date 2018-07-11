from jinja2 import Environment, FileSystemLoader
from jinja2_markdown import MarkdownExtension
import json
import os
from livereload import Server


def load_config():
    with open('config.json', 'r', encoding='utf8') as file:
        return json.load(file)


def load_markdown_article(path):
    with open(path, 'r', encoding='utf8') as file:
        return file.read()


def save_page(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8') as f:
        f.write(content)


def get_jinja_env():
    return Environment(loader=FileSystemLoader(
        searchpath='templates/'),
        extensions=[MarkdownExtension]
    )


def render_pages(articles_info):
    env = get_jinja_env()
    for article in articles_info['articles']:
        article_template = env.get_template('article.html')
        article_data = load_markdown_article('articles/{}'.format(article['source']))
        article_display_dictionary = {'article_data': article_data}
        article_output_page = article_template.render(article_display_dictionary)
        if ' ' in article['source']:
            article['source'] = article['source'].replace(' ', '')
        article_html_path = 'static/{}.html'.format(article['source'].split('.')[0])
        save_page(article_html_path, article_output_page)
    index_template = env.get_template('index.html')
    index_display_dictionary = {
        'topics': articles_info['topics'],
        'articles': articles_info['articles']
    }
    index_output_page = index_template.render(index_display_dictionary)
    save_page('static/index.html', index_output_page)


def make_site():
    articles_info = load_config()
    render_pages(articles_info)


if __name__ == '__main__':
    server = Server()
    server.watch('templates/', make_site)
    server.watch('articles/', make_site)
    server.watch('static/img', make_site)
    server.serve(root='static/')
