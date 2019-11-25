import dbus
import sys
from plugin import Plugin
from button import Button as ButtonData
from gbutton import GButton
from row import plugins as row_plugins
from grow import GRow
import xml.etree.ElementTree as ET
import re
import threading

from tkinter import Tk, PhotoImage, RIGHT
from tkinter.ttk import Button

theme = sys.argv[1]
size = int(sys.argv[2] or 24)
splash = False
if sys.argv[3] == "ON":
    splash = True

buttons = []
gbuttons = []
photos = []

icons = {
    "KDE_file_new": "document-new",
    "KDE_file_open": "document-open",
    "KDE_next_tab": "go-next",
    "KDE_prev_tab": "go-previous",
    "KDE_file_quit": "window-close",
    "KDE_fullscreen": "view-fullscreen",
    "KDE_Audio": "audio-x-generic",
    "KDE_Image": "image-x-generic",
    "KDE_view_zoom_in": "zoom-in",
    "KDE_view_zoom_out": "zoom-out",
    "GNOME_quit": "application-exit",
    "GNOME_new-window": "window-new",
    "GNOME_new-window": "window-new",
    "GNOME_new-document": "document-new"
}

def get_name(bus, pid):
    names = bus.list_names()
    result = []
    for name in names:
        if pid == pid_to_name(name):
            result.append(name)
    return result

def plugin_filter(names, plugs):
    result = {}
    for name in names:
        for plugin in plugs.values():
            if plugin.check(name):
                result[name] = plugin.name
                break
    return result

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

def kde_getter(bus, name):
    buttons = []
    items = get_nodes(bus, name, ["[a-z]+", "[a-zA-Z]+_1", "actions", "[a-z_]+"])
    for item in items:
        if ("KDE_" + item.split("/")[-2]) in icons:
            icon = icons["KDE_" + item.split("/")[-2]]
            method = bus.get_object(name, item[0:-1]).trigger
            buttons.append(ButtonData(method, [], icon, "org.qtproject.Qt.QAction", icon))
    return buttons

def gnome_getter(bus, name):
    buttons = []
    method = bus.get_object(name, "/org/gnome/" + name.split(".")[-1]).Activate
    items = bus.get_object(name, "/org/gnome/" + name.split(".")[-1]).List(dbus_interface="org.gtk.Actions")
    for item in items:
        if ("GNOME_" + item) in icons:
            icon = icons["GNOME_" + item]
            buttons.append(ButtonData(method, [item, dbus.Array([], signature='s'), dbus.Dictionary({}, signature='ss')], icon, "org.gtk.Actions", icon))
    return buttons

plugins = {"kde-app": Plugin("kde-app", "^org\.kde\.[a-z]+-[0-9]+", kde_getter),
           "gnome-app": Plugin("gnome-app", "^org\.gnome\.[a-z]+", gnome_getter)}

bus = dbus.SessionBus()

pid_to_name = bus.get_object("org.freedesktop.DBus", "/").GetConnectionUnixProcessID

names = {}

root = Tk()

def my_mainloop(root, buttons, gbuttons):
    while True:
        buttons = []
        names = {}
        pid = int(sys.stdin.readline())
        temp = plugin_filter(get_name(bus, pid), plugins)
        if temp:
            names = temp
        for name in names:
            buttons = plugins[names[name]].getter(bus, name)
        row_names = plugin_filter(get_name(bus, pid), row_plugins)
        rows = []
        for row in row_names:
            rows.append(row_plugins[row_names[row]].getter(bus, row))
        if buttons or rows:
            new_buttons = []
            for button in buttons:
                gbutton = GButton(theme, root, button, size)
                new_buttons.append(gbutton)
            for row in rows:
                grow = GRow(theme, root, row, size)
                new_buttons.append(grow)
            add = set(new_buttons) - set(gbuttons)
            destroy = set(gbuttons) - set(new_buttons)
            for item in add:
                item.view.pack(side = RIGHT)
            for item in destroy:
                item.destroy()
            gbuttons = new_buttons

thread = threading.Thread(target=my_mainloop, args=(root, buttons, gbuttons))
thread.start()

if splash:
    root.attributes('-type', 'dock')

root.mainloop()
