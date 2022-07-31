import PySimpleGUI as Sg
from util import get_search_result, get_images, download_url, resize_emote, copy_to_clipboard, delete_file_delayed, \
    delete_leftovers


class GUI:
    def __init__(self):
        Sg.theme("Black")
        self.name = "Nostro"
        self.layout = []
        self.window = None
        self.source = "FFZ"
        self.sleep_time = 60
        self.cache = {}

        self.display_search()

    def main_loop(self):
        while True:
            event, values = self.window.read()
            if event == Sg.WIN_CLOSED or event == "Cancel":
                break
            if event == "btnSearch":
                self.search_button(values["inpSearch"])
            if "btnEmote" in event:
                self.emote_button(event)
        delete_leftovers()
        self.window.close()

    def display_search(self, default_text=""):
        if self.window:
            self.window.close()
        self.layout = [[Sg.InputText(default_text, focus=True, key="inpSearch"),
                        Sg.Button("Search", key="btnSearch", bind_return_key=True)]]
        self.window = Sg.Window(self.name, self.layout, finalize=True, use_default_focus=True)
        self.window.TKroot.focus_force()
        self.window.Element("inpSearch").SetFocus()

    def display_images_as_grid(self, images_and_ids):
        if self.window:
            self.window.close()

        new_layout = []
        row = []
        emotes_per_col = 10
        col = 0
        for image in images_and_ids:
            img, im_id = image
            new_element = Sg.Button("", image_data=img, key=f"btnEmote-{im_id}")

            if col % emotes_per_col != 0 or col == 0:
                row.append(new_element)
            else:
                new_layout.append(row)
                row = []

            col = col + 1

        if not new_layout:
            self.display_search("NoResults")
        else:
            self.layout = new_layout
            self.window = Sg.Window(self.name, self.layout)

    def search_button(self, search_string):
        self.window.close()
        emotes = get_search_result(search_string, self.source)
        if not emotes:
            self.display_search("Error")
            return
        images = get_images(emotes)
        if not images:
            self.display_search("Error")
            return

        for img in images:
            self.cache[str(img[1])] = img[0]

        self.display_images_as_grid(images)

    def emote_button(self, event):
        emote_id = str(event).split("-")[1]
        emote_filename = f"__tmp__Notro-{emote_id}.png"

        url = f"https://cdn.frankerfacez.com/emoticon/{emote_id}/2"
        download_url(url, emote_filename)
        resize_emote(emote_filename)
        copy_to_clipboard(emote_filename)

        delete_file_delayed(emote_filename, self.sleep_time)

        self.display_search()
