from urllib.request import urlopen
from resourсe import Resource
from lxml.html import fromstring


class Parser:
    def __init__(self, url):
        self.resource = Resource(url)
        self.resource.get_domain()
        self.links = set()

    def get_referred_links(self, dom):
        for link in dom.xpath('//a/@href'):
            if (link == "") or (":" in link) or ((("http" in link) or ("ftp" in link))
                                                 and (self.resource.domain not in link)):
                continue
            buff = ""
            if link[0:4] != "http" and link[0:3] != "ftp":
                buff = self.normalize_link(link)
            normal_link = buff
            if buff[-1] == "#":
                normal_link = buff.replace('#', '')
            if (normal_link == self.resource.url) or \
                    (normal_link in self.links) or \
                    ((normal_link+"/") in self.links) or \
                    (normal_link[:len(normal_link)-1] in self.links):
                continue
            self.links.add(normal_link)
            self.resource.self_urls.append(normal_link)

    def normalize_link(self, link):
        if link[0] == "/":
            return self.resource.domain + link
        return self.resource.domain + "/" + link

    def get_title(self, dom):
        self.resource.title = dom.findtext('.//title')

    def get_content(self, html):
        self.resource.html = html

    @staticmethod
    def open_link(link):
        try:
          opened_link = urlopen(link).read().decode('utf-8')
          return opened_link
        except:
            print("ссылка поломалась  ", link)

    @staticmethod
    def is_link_alive(link):
        try:
           test = urlopen(link).read().decode('utf-8')
           return True
        except TypeError:
            pass

    def make_resource(self):
        html = self.open_link(self.resource.url)
        self.get_content(html)
        dom = fromstring(html)
        self.get_referred_links(dom)
        self.get_title(dom)
        self.resource.create_filename()
        self.resource.create_file()


if __name__ == '__main__':
    parser = Parser("http://interdikt.com/")
    parser.make_resource()




