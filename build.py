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
    static_url = '/19_site_generator/static'
    for article in articles_info['articles']:
        article_template = env.get_template('article.html')
        article_data = load_markdown_article(os.path.join('articles/', article['source']))
        article_context = {
            'article_data': article_data,
            'STATIC_URL': static_url
        }
        article_output_page = article_template.render(article_context)
        slug = article['source'].replace(' ', '')
        article_html_path = 'static/{}.html'.format(os.path.splitext(slug)[0])
        save_page(article_html_path, article_output_page)
    index_template = env.get_template('index.html')
    index_context = {
        'topics': articles_info['topics'],
        'articles': articles_info['articles'],
        'STATIC_URL': static_url
    }
    index_output_page = index_template.render(index_context)
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
