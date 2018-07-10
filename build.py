from jinja2 import Environment, FileSystemLoader
from jinja2_markdown import MarkdownExtension
import json


def load_config():
    with open('config.json', 'r', encoding='utf8') as file:
        return json.load(file)


def load_markdown_article(path):
    with open(path, 'r', encoding='utf8') as file:
        return file.read()


def get_articles_by_topic(articles_info, topic):
    return [article for article in articles_info['articles'] if article['topic'] == topic]


if __name__ == '__main__':
    articles_info = load_config()
    # print(articles_info['topics'])

    env = Environment(loader=FileSystemLoader(
        searchpath='templates/'),
        extensions=[MarkdownExtension]
    )
    index_template = env.get_template('index.html')
    display_dictionary = {'topics': articles_info['topics']}
    output = index_template.render(display_dictionary)
    with open('static/index.html', 'w', encoding='utf8') as f:
        f.write(output)

    for article in articles_info['articles']:
        article_template = env.get_template('article.html')
        article_data = load_markdown_article('articles/{}'.format(article['source']))
        display_dictionary = {'article_data': article_data}
        output = article_template.render(display_dictionary)
        with open('static/{}.html'.format(article['source'].split('/')[1]), 'w', encoding='utf8') as f:
            f.write(output)
