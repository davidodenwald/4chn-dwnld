"""Usage: 4chn [-h] [--help] URL

-h --help    show this
"""

import docopt
import pathlib
import bs4
import requests
import tqdm


def arg_pharse():
    arguments = docopt.docopt(__doc__)
    return arguments["URL"]


def get_html(url):
    return requests.get(url).text


def get_title(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    thread = soup.find("div", {"class": "thread"})
    return thread["id"]


def get_image_links(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    tags = [tag for tag in soup.find_all("a", {"class": "fileThumb"})]
    return ["http:" + image['href'] for image in tags]


def get_image_titles(images):
    return [title[20:] for title in images]


def create_folder(name):
    path = pathlib.Path(name)
    if not path.exists():
        path.mkdir()


def progress(images, names, folder):
    for x in tqdm.tqdm(range(len(images)), bar_format = "{l_bar}{bar}|{remaining}"):
        save_file(download_image(images[x]), names[x], folder)


def download_image(image):
    return requests.get(image, stream=True)


def save_file(file, name, folder):
    path = folder + "/" + name
    with open(path, 'wb') as handle:
        for block in file.iter_content(1024):
            handle.write(block)


if __name__ == '__main__':
    url = arg_pharse()

    html = get_html(url)
    title = get_title(html)

    create_folder(title)

    image_links = get_image_links(html)
    image_titles = get_image_titles(image_links)

    progress(image_links, image_titles, title)