from urllib.request import urlopen
from Parser import Parser
from file_creator import *
import urllib.error
from os import path
from lxml.html import fromstring
from sys import stderr

PATH = path.dirname(path.abspath(__file__))


class Spider:
    """Class for crawl link"""

    queue = set()
    passed = set()
    queue_file = 'queue.txt'
    passed_file = 'passed.txt'
    passed_all_file = 'passed_all.txt'

    def __init__(self, start_url):
        if start_url == 'update':
            self.queue = file_to_set(Spider.passed_all_file)
            start_url = self.queue.pop()
        else:
            self.boot()
            self.start_url = start_url
            Spider.queue.add(start_url)
        self.crawl_page('start spider', start_url)

    @staticmethod
    def boot():
        """Boot links from files for start crawl"""

        delete_file_content(Spider.queue_file)
        Spider.passed = file_to_set(Spider.passed_file)

    @staticmethod
    def crawl_page(thread_name, url):
        """Handle link"""

        if url not in Spider.passed:
            links = Spider.get_referred_links(url)
            if links is not False:
                Spider.add_links_to_queue(links)
                try:
                    Spider.queue.remove(url)
                    Spider.passed.add(url)
                except KeyError:
                    Spider.queue.add(url)
                Spider.update_files()

    @staticmethod
    def get_referred_links(url):
        """Return referred links in html
        and create html file for this url"""

        if Spider.is_link_alive(url):
            html = Spider.open_link(url)
            dom = fromstring(html)
            domain = Parser.get_domain(url)
            parser = Parser(dom, domain)
            title = Parser.get_title(dom)
            name = create_filename(title, domain, url)
            parser.get_referred_links()
            domain_ = Parser.get_domain_without_protocol(url)
            create_file_to_result(html, name, parser.real_links, domain_)
            return parser.links
        return False

    @staticmethod
    def is_link_alive(url):
        """Check whether the link can be opened and
        return True if it's okay"""

        try:
            Spider.open_link(url)
            return True
        except urllib.error.HTTPError as ex:
            print(url, ex, file=stderr)
        except urllib.error.ContentTooShortError as ex:
            print(url, ex, file=stderr)
        except urllib.error.URLError as ex:
            print(url, ex, file=stderr)
        except TypeError as ex:
            print(url, ex, file=stderr)
        except UnicodeDecodeError as ex:
            print(url, ex, file=stderr)

    @staticmethod
    def open_link(link):
        """Open url, read and decode html"""

        return urlopen(link).read().decode('utf-8')

    @staticmethod
    def add_links_to_queue(links):
        """Add links in queue set"""

        for url in links:
            if url in Spider.queue or url in Spider.passed:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        """Load received links into the queue and passed"""

        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.passed, Spider.passed_file)


if __name__ == '__main__':
    spider = Spider('https://anytask.org/')
