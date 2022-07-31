import multiprocessing
import threading
import urllib
import urllib.request
import requests
import json
from multiprocessing import Pool
import subprocess as Sp
from PIL import Image, ImageFilter
import os
import time

def image_from_url(url):
    response = urllib.request.urlopen(url)
    return response.read()


def resize_emote(file_name):
    im = Image.open(file_name).convert('RGBA')
    im.thumbnail((48, 48), resample=Image.LANCZOS)
    im = im.filter(ImageFilter.SHARPEN)
    im.save(file_name)


def copy_to_clipboard(file_name):
    command = f"Set-Clipboard -Path .\{file_name}"
    Sp.run(["powershell", "-Command", command], capture_output=True)


def get_image(emote_id):
    url = f"https://cdn.frankerfacez.com/emoticon/{emote_id}/2"
    return image_from_url(url), emote_id


def delete_file_delayed(filename, sleep_time=20):
    deleter = threading.Thread(target=delete_file, args=(filename, sleep_time))
    deleter.daemon = True
    deleter.start()


def delete_file(filename, sleep_time):
    time.sleep(sleep_time)
    if os.path.exists(filename):
        os.remove(filename)


def delete_leftovers():
    for filename in os.listdir("."):
        f = os.path.join(".", filename)
        if os.path.isfile(f):
            if "__tmp__Notro-" in f and ".png" in f:
                os.remove(f)


def download_url(url, file_name):
    r = requests.get(url)
    open(file_name, 'wb').write(r.content)
    return


def get_images(emotes):
    if not emotes:
        return
    with Pool(processes=multiprocessing.cpu_count() * 2 + 2) as p:
        images_and_ids = p.map(get_image, list(zip(*emotes))[1])
        p.join()

    return images_and_ids


def get_search_result(search_string, source):
    if source == "FFZ":
        return get_emotes_ffz(search_string)
    elif source == "7TV":
        return get_emotes_7tv(search_string)
    elif source == "BTTV":
        return get_emotes_bttv(search_string)
    else:
        print("Specify correct source!")
        return None


def get_emotes_7tv(search_string):
    # url = f"https://7tv.app/emotes?sortBy=popularity&page=0&query={search_string}"
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    # time.sleep(5)
    # driver.get(url)
    # time.sleep(5)
    # page = driver.page_source
    # page_soup = BeautifulSoup(page, 'html.parser')
    # images = []
    # for img in page_soup.find_all('img'):
    #   images.append(img.get('src'))
    # print(images)
    print("Not implemented")
    exit(-1)


def get_emotes_bttv(search_string):
    print("Not implemented")
    exit(-1)


def get_emotes_ffz(search_string):
    url = f"https://api.frankerfacez.com/v1/emotes?q={search_string}&sensitive=false&sort=count&high_dpi=off&page=1&per_page=60"
    request = urllib.request.urlopen(url).read().decode("utf-8")
    json_emotes = json.loads(request)["emoticons"]

    emotes = []
    for e in json_emotes:
        emotes.append((e["name"], e['id']))
    return emotes
