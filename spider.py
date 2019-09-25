from collections import deque
from parser import Parser


class Spider:
    def __init__(self, url, deep=None):
        self.start_url = url
        self.deep = deep
        self.queue = deque()
        self.queue.append(self.start_url)
        self.passed = set()

    def go(self):
        while True:
            try:
                url = self.queue.popleft()
            except:
                break
            if url not in self.passed:
                parser = Parser(url)
                if parser.is_link_alive(url):
                    parser.make_resource()
                self.passed.add(url)
                self.put_link_in_queue(parser.resource)

    def put_link_in_queue(self, resource):
        for link in resource.self_urls:
            if link in self.passed:
                continue
            self.queue.append(link)


if __name__ == '__main__':
    spider = Spider('https://anytask.org/')
    spider.go()
