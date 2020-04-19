import argparse
import threading
import logging
from queue import Queue
from spider import Spider
from file_creator import *
from Parser import Parser


queue_file = 'queue.txt'
queue = Queue()


def main(arg):
    """Program entry point"""

    logging.basicConfig(filename="crawler.log", level=logging.INFO)
    logging.info("Program started")

    if arg.clear:
        logging.info("Start clear")
        clear()
    if arg.update:
        logging.info("Start update")
        Spider('update')
        number_of_threads = 5
        go_spider(number_of_threads)
        crawl()
    if arg.url:
        logging.info("Start crawl url %s" % arg.url)
        domain = Parser.get_domain_without_protocol(arg.url)
        logging.info("Start make dir")
        make_dir(domain)
        Spider(arg.url)
        number_of_threads = 5
        go_spider(number_of_threads)
        crawl()
        set_to_passed_all_file(Spider.passed, Spider.passed_all_file)
    logging.info("Done!")


def go_spider(number_of_threads):
    """Create threads and start"""

    for _ in range(number_of_threads):
        t = threading.Thread(target=go)
        t.daemon = True
        t.start()


def go():
    """Get link from queue and put it to Spider"""

    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


def crawl():
    """Checking if there's an empty queue,
    if it's ok, it keeps crawl"""

    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        put_and_crawl()


def put_and_crawl():
    """Put found links to queue and continues crawl"""

    for link in file_to_set(queue_file):
        queue.put(link)
    queue.join()
    crawl()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This program "
                                                 "crawled websites. "
                                                 "Arguments: valid link.")
    parser.add_argument("-url", type=str, help="Input url for crawler")
    parser.add_argument("-clear", help="delete all files on result",
                        action='store_const', const=True)
    parser.add_argument("-update", help="Update load pages",
                        action='store_const', const=True)
    args = parser.parse_args()
    main(args)
