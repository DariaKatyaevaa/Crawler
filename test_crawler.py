import unittest
from lxml.html import fromstring
from crawler import *


class Test(unittest.TestCase):

    def test_open_link_error_first(self):
        link = "http://interdikt.com/bankrotstvo/"
        self.assertNotEqual(Spider.is_link_alive(link), True)

    def test_open_link_error_second(self):
        self.assertNotEqual(Spider.is_link_alive("http://foo.ru/"), True)

    def test_title(self):
        with open("test_title.html",
                  encoding='utf-8') as f:
            file = f.read()
        dom = fromstring(file)
        self.assertEqual(Parser.get_title(dom),
                         "Дорамы смотреть онлайн с русской озвучкой")

    def test_domain(self):
        link = "http://interdikt.com/bankrotstvo/"
        self.assertEqual(Parser.get_domain(link),
                         "http://interdikt.com")

    def test_find_link(self):
        html = Spider.open_link("https://anytask.org/")
        dom = fromstring(html)
        pars = Parser(dom, "https://anytask.org")
        pars.get_referred_links()
        self.assertEqual(pars.links.__len__(), 23)
        for i in pars.links:
            self.assertEqual(("https://anytask.org" in i), True)

    def test_outbound_link(self):
        html = Spider.open_link("http://button.dekel.ru/")
        dom = fromstring(html)
        pars = Parser(dom, "http://button.dekel")
        pars.get_referred_links()
        for j in pars.outbound_links:
            cond = j in pars.links
            self.assertEqual(cond, False)

    def test_outbound_link_len(self):
        html = Spider.open_link("https://ulearn.me/")
        dom = fromstring(html)
        pars = Parser(dom, "https://ulearn.me/")
        pars.get_referred_links()
        len_ = pars.outbound_links.__len__()
        self.assertEqual(len_, 2)

    def test_crawler(self):
        make_dir("anytask")
        Spider("https://anytask.org/")
        number_of_threads = 5
        go_spider(number_of_threads)
        crawl()
        clear()
        self.assertEqual(len(Spider.passed), 24)


if __name__ == '__main__':
    unittest.main()
