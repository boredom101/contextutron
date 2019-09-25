from cairosvg import svg2png
from tkinter.ttk import Button
from tkinter import PhotoImage
from xdg import IconTheme

class GButton:
    def __init__(self, theme, root, data):
        name = IconTheme.getIconPath(data.icon, theme=theme)
        self.photo = PhotoImage(data = svg2png(url = name, parent_width = 24, parent_height = 24))
        self.data = data
        self.button = Button(root, image = self.photo, command = self.data.call)
