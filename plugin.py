import re

class Plugin:
    def __init__(self, name, pattern, getter):
        self.name = name
        self.pattern = pattern
        self.getter = getter
    
    def check(self, name):
        match = re.search(self.pattern, name)
        if match:
            return True
        else:
            return False
