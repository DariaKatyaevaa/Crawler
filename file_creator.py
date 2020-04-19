from os import path, mkdir
from shutil import rmtree
import logging

PATH = path.dirname(path.abspath(__file__))


def create_file_to_result(html, name, links, domain):
    """Create html file and put it to result"""
    html_with_mirror = replace_links_to_local(html, links, domain)
    try:
        file = path.join(PATH, "result", domain, name + ".html")
        with open(file, 'w', encoding='utf-8') as f:
            f.write(html_with_mirror)
    except Exception as e:
        logging.info(e.__str__())
        file = path.join("result/", domain, name + ".html")
        with open(file, 'w', encoding='utf-8') as f:
            f.write(html_with_mirror)


def replace_links_to_local(html, links, domain):
    """Find links and replaces them with local addresses"""
    for link in links:
        name = create_filename("", "", link).strip()
        name = name.replace("#", "%23")
        adr = path.join(PATH, "result", domain, name + ".html")
        html = html.replace("href=\"" + link + "\"", "href=\"" + adr + "\"")
    return html


def create_filename(title, domain, url):
    """Create name for html file"""
    name = url[len(domain):].replace('/', ' ').strip()
    return name


def append_to_file(file_path, data):
    """Append data to file_path"""
    with open(file_path, "a") as file:
        file.write(data+'\n')


def delete_file_content(file_path):
    """Delete all data in file_path"""
    with open(file_path, 'w'):
        pass


def clear():
    """Delete all files in result dir"""

    delete_file_content("passed.txt")
    delete_file_content("queue.txt")
    delete_file_content("passed_all.txt")
    try:
        rmtree(path.join(PATH, "result/"))
    except OSError:
        pass
    try:
        mkdir(path.join(PATH, "result/"))
    except PermissionError:
        try:
            mkdir(path.join("result/"))
        except FileExistsError:
            pass
    except FileExistsError:
        pass


def file_to_set(file_name):
    """Return links from file"""
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def set_to_file(links, file):
    """Boot links from set to file"""
    delete_file_content(file)
    for link in sorted(links):
        append_to_file(file, link)


def set_to_passed_all_file(links, file):
    for link in sorted(links):
        with open(file, "a") as f:
            f.write(link + '\n')


def make_dir(domain):
    """Create dir for pages from one site"""
    dir_path = path.join(PATH, "result/", domain + "/")
    try:
        logging.info("Trying make dir")
        mkdir(dir_path)
        logging.info("Making dir")
    except PermissionError:
        logging.info("Permission Error")
        mkdir(path.join("result/", domain + "/"))
    except FileExistsError:
        logging.info("File Exist Error")
    except OSError:
        logging.info("OS Error")
        print("Creation of the directory %s failed" % dir_path)
    logging.info("Make dir done")
