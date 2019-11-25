from cairosvg import svg2png
from tkinter.ttk import Button
from tkinter import PhotoImage
from xdg import IconTheme

class GButton:
    def __init__(self, theme, root, data, size):
        name = IconTheme.getIconPath(data.icon, theme=theme)
        self.photo = PhotoImage(data = svg2png(url = name, parent_width = size, parent_height = size))
        self.data = data
        self.view = Button(root, image = self.photo, command = self.data.call, text = data.text, compound="left")
    
    def __hash__(self):
        return hash(self.data)
    
    def destroy(self):
        self.view.destroy()
