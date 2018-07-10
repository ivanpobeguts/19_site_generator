from jinja2 import Environment, FileSystemLoader
from jinja2_markdown import MarkdownExtension
import json


def load_config():
    with open('config.json', 'r', encoding='utf8') as file:
        return json.load(file)


def load_markdown_article(path):
    with open(path, 'r', encoding='utf8') as file:
        return file.read()


def save_page(path, content):
    with open(path, 'w', encoding='utf8') as f:
        f.write(content)


def get_jinja_env():
    return Environment(loader=FileSystemLoader(
        searchpath='templates/'),
        extensions=[MarkdownExtension]
    )


def get_articles_by_topic(articles_info, topic):
    return [article for article in articles_info['articles'] if article['topic'] == topic]


def render_pages(articles_info):
    env = get_jinja_env()
    index_template = env.get_template('index.html')
    display_dictionary = {'topics': articles_info['topics']}
    index_output = index_template.render(display_dictionary)
    save_page('static/index.html', index_output)
    for article in articles_info['articles']:
        article_template = env.get_template('article.html')
        article_data = load_markdown_article('articles/{}'.format(article['source']))
        display_dictionary = {'article_data': article_data}
        article_output = article_template.render(display_dictionary)
        acticle_html_path = 'static/{}.html'.format(article['source'].split('/')[1].split('.')[0])
        save_page(acticle_html_path, article_output)


if __name__ == '__main__':
    articles_info = load_config()
    render_pages(articles_info)
