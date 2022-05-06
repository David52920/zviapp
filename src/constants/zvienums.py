import enum


class ZVI(enum.Enum):
    SETTINGS = 0,
    ADD = 1,
    VALUECHANGE = 2,
    PROGRESS = 3,
    IMPORT = 4,
    WINDOW = 5,
    FINISHED = 6,
    MESSAGEBOX = 7


class WINDOW(enum.Enum):
    RESIZE = 0,
    CLOSE = 1,
    SHOW = 2,
    HIDE = 3,
    CENTER = 4,
    DOCK = 5


class MSGBOX(enum.Enum):
    STANDARDOK = 0,
    WARNINGOK = 1,
    FLOWMESSAGE = 2,
    MESSAGE = 3