class Parser:
    """Class for parsing html"""

    def __init__(self, html_, domain_):
        self.html = html_
        self.links = set()
        self.real_links = []
        self.domain = domain_
        self.outbound_links = []

    def normalize_link(self, link):
        """Make the link absolute"""

        if link[0] == "/":
            return self.domain + link
        return self.domain + "/" + link

    def get_referred_links(self):
        """Get inbound referred links"""

        for link in self.html.xpath('//a/@href'):
            if ((("http" in link) or ("ftp" in link)) and
                    (self.domain not in link)):
                self.outbound_links.append(link)
                continue
            if not link or (":" in link):
                continue
            buff = ""
            if link[0:4] != "http" and link[0:3] != "ftp":
                buff = self.normalize_link(link)
            normal_link = buff
            self.real_links.append(link)
            if buff[-1] == "#":
                normal_link = buff.replace('#', '')
            if ((normal_link in self.links) or
                    ((normal_link + "/") in self.links) or
                    (normal_link[:len(normal_link) - 1] in self.links)):
                continue
            self.links.add(normal_link)

    @staticmethod
    def get_title(html_):
        """Get html title"""

        return html_.findtext('.//title')

    @staticmethod
    def get_domain(link):
        """Get link domain"""

        try:
            token = link.split('https://')[1].split('/')[0]
            protocol = 'https://'
        except IndexError:
            token = link.split('http://')[1].split('/')[0]
            protocol = 'http://'
        domain_ = token.split('.')[-2] + '.' + token.split('.')[-1]
        return protocol + domain_

    @staticmethod
    def get_domain_without_protocol(link):
        """Get link domain without protocol"""
        try:
            token = link.split('https://')[1].split('/')[0]
        except IndexError:
            token = link.split('http://')[1].split('/')[0]
        domain_ = token.split('.')[-2]

        return domain_
