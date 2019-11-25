class Button:
    def __init__(self, method, args, icon, interface, text):
        self.method = method
        self.args = args
        self.icon = icon
        self.interface = interface
        self.text = text
    
    def call(self):
        self.method(*(self.args), dbus_interface = self.interface)
    
    def __hash__(self):
        return hash((self.interface, self.icon, *self.args))
