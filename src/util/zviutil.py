import functools
import glob
import linecache
import operator
import importlib.resources
import re
import os
from itertools import zip_longest

from PyQt5.QtGui import QPixmap
import src.assets.startup
import src.assets.icons
import src.assets.docs
import src.assets.images
import src.assets.images.browser


class Singleton:
    _state = {}

    def __init__(self):
        self.__dict__ = self._state


def walkPath(path, depth=1):
    for i in range(depth):
        path = os.path.dirname(path)
    return path


def strtobool(string, asInt=False):
    toCheckTrue = ["y", "yes", "Yes", "1", "2", "3", "true", "True"]
    toCheckFalse = ["n", "no", "No", "0", "false", "False"]
    if string in toCheckTrue:
        if asInt:
            return 1
        else:
            return True
    elif string in toCheckFalse:
        if asInt:
            return 0
        else:
            return False
    else:
        if string is None:
            return False
        raise ValueError


def getFromDict(dataDict, objectName):
    if isinstance(objectName, list):
        return functools.reduce(operator.getitem, objectName, dataDict)
    elif "." in objectName:
        objectName = objectName.split(".")
        return functools.reduce(operator.getitem, objectName, dataDict)
    else:
        ls = [""]
        if any(string in objectName for string in ls):
            objectName = objectName[:-2]
        return dataDict[objectName]


def setInDict(dataDict, objectName, value):
    if "." in objectName:
        objectName = objectName.split(".")
        getFromDict(dataDict, objectName[:-1])[objectName[-1]] = value
    else:
        if isinstance(objectName, list):
            getFromDict(dataDict, objectName[:-1])[objectName[-1]] = value
        else:
            ls = [""]
            if any(string in objectName for string in ls):
                objectName = objectName[:-2]
            dataDict[objectName] = value


def grouper(n, iterable, fillValue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillValue, *args)


def getLineFromFile(filename, string=None, lineNum=0, asText=False):
    if string is not None:
        with open(filename) as file:
            line = re.findall(r'^{0}.*$'.format(string),
                              file.read(), re.MULTILINE)[0]
            if "Type" in string:
                return re.findall(r'M\w-\w+-\w+', line)
            else:
                return list(map(float, re.findall(r'\d+\.\d+', line)))
    elif string is None:
        text = linecache.getline(filename, lineNum)
        if asText:
            return text
        else:
            return list(map(float, text.split()))


def replaceValuesFromString(pattern, string, newValues):
    matches = re.finditer(pattern, string)
    for match, value in zip(matches, newValues):
        string = string.replace(match.group(), "{0}{1}".format(match.group(1), value))
    return string


def getResource(resource, location=None, isConnected=False):
    if ".ico" in resource:
        pixmap = QPixmap()
        pixmap.load(importlib.resources.open_text(src.assets.icons, resource).name)
        return pixmap
    elif "browser_" in resource:
        resource = resource[resource.index('_') + 1:]
        pixmap = QPixmap()
        pixmap.load(importlib.resources.open_text(src.assets.images.browser, resource).name)
        return pixmap
    elif ".png" in resource or ".bmp" in resource:
        pixmap = QPixmap()
        pixmap.load(importlib.resources.open_text(src.assets.images, resource).name)
        return pixmap
    elif ".html" in resource or ".qhc" in resource:
        return importlib.resources.open_text(src.assets.docs, resource).name
    elif ".json" in resource:
        if not location:
            if not isConnected and "*" in resource:
                contents = importlib.resources.contents(src.assets.startup)
                return [importlib.resources.open_text(src.assets.startup, x).name for x in contents if
                        x.startswith("type")]
            elif "*" in resource:
                return glob.glob(importlib.resources.open_text(src.assets.startup, resource).name)
            else:
                return importlib.resources.open_text(src.assets.startup, resource).name
        else:
            if "*" in resource:
                return glob.glob(os.path.join(location + "\\startup\\", resource))
            else:
                return os.path.join(location + "\\startup\\", resource)
    return ''


def getDesktopDir(systemType):
    if "Windows" in systemType:
        ls = ["~/Desktop", "~/OneDrive/Desktop",
            "~/OneDrive - /Desktop", "~/OneDrive-/Desktop"]
        for folder in ls:
            f = os.path.expanduser(folder)
            if os.path.exists(f):
                return f
    else:
        return os.path.join(os.path.join(os.environ['HOME']), 'Desktop')


def replace(file_name, line_num, text, line_num1="", text1=""):
    """Replace text for .OUT"""
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            lines[line_num] = text
            if line_num1 != "":
                lines[line_num1] = text1
        with open(file_name, 'w') as file:
            file.writelines(lines)
    except (ValueError, TypeError):
        return


def get_deep_attr(obj, attrs):
    for attr in attrs.split("."):
        obj = getattr(obj, attr)
    return obj


def has_deep_attr(obj, attrs):
    try:
        get_deep_attr(obj, attrs)
        return True
    except AttributeError:
        return False
