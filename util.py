import urllib
import urllib.request
import json
from multiprocessing import Pool
import pyperclip


def image_from_url(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_image(emote_id):
    url = f"https://cdn.frankerfacez.com/emoticon/{emote_id}/2"
    return image_from_url(url), emote_id


def get_images(emotes):
    if not emotes:
        return
    ids = list(zip(*emotes))[1]
    with Pool(processes=16) as p:
        images_and_ids = p.map_async(get_image, ids).get()
    return images_and_ids


def get_emote_url(emote_id, source):
    if source == "FFZ":
        pyperclip.copy(f"https://cdn.frankerfacez.com/emoticon/{emote_id}/1")
    elif source == "7TV":
        pyperclip.copy(f"https://cdn.frankerfacez.com/emoticon/{emote_id}/1")
    elif source == "BTTV":
        pyperclip.copy(f"https://cdn.frankerfacez.com/emoticon/{emote_id}/1")
    else:
        print("Specify correct source!")
        return None


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
    #url = f"https://7tv.app/emotes?sortBy=popularity&page=0&query={search_string}"
    #driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    #time.sleep(5)
    #driver.get(url)
    #time.sleep(5)
    #page = driver.page_source
    #page_soup = BeautifulSoup(page, 'html.parser')
    #images = []
    #for img in page_soup.find_all('img'):
    #    images.append(img.get('src'))
    # print(images)
    # exit(-1)
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
