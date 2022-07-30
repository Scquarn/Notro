import PySimpleGUI as Sg
from util import get_search_result, get_images
from io import BytesIO
import win32clipboard
from PIL import Image
import io


class GUI:
    def __init__(self):
        Sg.theme("Black")
        self.name = "Nostro"
        self.layout = []
        self.window = None
        self.source = "FFZ"
        self.cache = {}

        self.display_search()

    def main_loop(self):
        while True:
            event, values = self.window.read()
            print(event, values)
            if event == Sg.WIN_CLOSED or event == "Cancel":
                break
            if event == "btnSearch":
                self.search_button(values["inpSearch"])
            if "btnEmote" in event:
                self.emote_button(event)
        self.window.close()

    def display_search(self, default_text=""):
        if self.window:
            self.window.close()
        self.layout = [[Sg.InputText(default_text, focus=True, key="inpSearch"), Sg.Button("Search", key="btnSearch", bind_return_key=True)]]
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
        self.display_search()
        emote_id = str(event).split("-")[1]

        image = Image.open(io.BytesIO(self.cache[emote_id]))
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
