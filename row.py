from button import Button
from plugin import Plugin
import xml.etree.ElementTree as ET
import re

def get_nodes(bus, name, pattern):
    xml = bus.get_object(name, "/").Introspect()
    root = ET.fromstring(xml)
    current = [(root, "/")]
    temp = []
    for item in pattern:
        for element in current:
            for node in element[0].findall("node"):
                if re.search(item, node.get("name")):
                    data = bus.get_object(name, element[1] + node.get("name")).Introspect()
                    temp.append((ET.fromstring(data), element[1] + node.get("name") + "/"))
        current = temp
        temp = []
    results = []
    for element in current:
        results.append(element[1])
    return results

def kde_tab_getter(bus, name):
    buttons = []
    method = bus.get_object(name, "/Windows/1").setCurrentSession
    for node in get_nodes(bus, name, ["Sessions", "[0-9]+"]):
        obj = bus.get_object(name, node[0:-1])
        title = obj.title(1)
        icon = "utilities-terminal"
        button = Button(method, [int(node[-2])], icon, "org.kde.konsole.Window", title)
        buttons.append(button)
    return buttons

plugins = {
    "kde-tabs": Plugin("kde-tabs", "^org\.kde\.konsole-[0-9]+", kde_tab_getter)
}
