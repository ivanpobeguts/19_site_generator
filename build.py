from jinja2 import Environment, FileSystemLoader
import json


def load_config():
    with open('config.json', 'r', encoding='utf8') as file:
        return json.load(file)


# def get_articles_by_topic(articles_info, topic):
#     return [article for article in articles_info['articles'] if article['topic'] == topic]


if __name__ == '__main__':
    articles_info = load_config()
    # print(articles_info['topics'])

    env = Environment(loader=FileSystemLoader(
        searchpath='templates/')
    )
    template = env.get_template('index.html')
    display_dictionary = {'topics': articles_info['topics']}
    output = template.render(display_dictionary)
    with open('static/index.html', 'w', encoding='utf8') as f:
        f.write(output)
