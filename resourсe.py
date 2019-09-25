import json
import os


class Resource:
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.self_urls = list()
        self.html = ""
        self.domain = ""
        self._name_of_file = ""

    def create_file(self):
        path = os.path.dirname(os.path.abspath(__file__)) + r"\result" + "\\"
        with open(path + self._name_of_file + ".json", 'w', encoding='utf-8') as f:
            f.write(self.to_json())

    def create_filename(self):
        name = self.url[len(self.domain):].replace('/', ' ')
        if name != "" or name != " ":
            self._name_of_file = name
        if self._name_of_file == "" or self._name_of_file == " ":
            self._name_of_file = self.title

    def get_domain(self):
        try:
            token = self.url.split('https://')[1].split('/')[0]
            protocol = 'https://'
        except Exception as exc:
            token = self.url.split('http://')[1].split('/')[0]
            protocol = 'http://'
        self.domain = protocol + token.split('.')[-2] + '.' + token.split('.')[-1]
        self._name_of_file = token.split('.')[-2] + '.' + token.split('.')[-1]

    def to_json(self):
        dictionary = {
            'url': self.url,
            'title': self.title,
            'domain': self.domain,
            'found own links': self.self_urls,
            'html': self.html
        }
        return json.dumps(dictionary, ensure_ascii=False, indent=4)


