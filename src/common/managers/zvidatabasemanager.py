import sqlite3

from src.constants.zviconstants import constants


class DatabaseManager:
    def __init__(self):
        self.databaseLocation = constants.path["Database"] + "login.db"
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.databaseLocation)
        except sqlite3.Error as er:
            raise ConnectionError

    def execute(self, command, infoTuple):
        self.connect()
        result = self.connection.execute(command, infoTuple)
        result = result.fetchall()[0][4] if "PASSWORD" in command else result.fetchall()
        if "INSERT" in command:
            self.commit()
        self.disconnect()
        return result

    def commit(self):
        self.connection.commit()

    def disconnect(self):
        self.connection.close()
