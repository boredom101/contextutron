class Button:
    def __init__(self, method, args, icon, interface):
        self.method = method
        self.args = args
        self.icon = icon
        self.interface = interface
    
    def call(self):
        self.method(*(self.args), dbus_interface = self.interface)
