from gbutton import GButton

from tkinter import Frame, LEFT

class GRow():
    
    def __init__(self, theme, root, data, size):
        self.data = data
        self.graphics = []
        self.view = Frame(root, borderwidth=1)
        for item in data:
            self.graphics.append(GButton(theme, self.view, item, size))
            self.graphics[-1].view.pack(side = LEFT)
    
    def __hash__(self):
        return hash(tuple(self.graphics))
    
    def destroy(self):
        self.view.destroy()
        for graphic in self.graphics:
            graphic.destroy
