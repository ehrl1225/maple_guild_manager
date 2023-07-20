from Guild import Guild
import pickle
import os
from typing import Generator

class DataManager:
    guilds: dict[str, Guild] = dict()
    data_folder: str = "data"
    data_file_name: str = "data.pkl"

    def __init__(self):
        pass

    @staticmethod
    def get_data_file_path():
        return os.path.join(DataManager.data_folder, DataManager.data_file_name)

    @staticmethod
    def save():
        with open(DataManager.get_data_file_path(), "wb") as f:
            pickle.dump(DataManager.guilds, f)

    @staticmethod
    def load(self):
        if os.path.isdir(DataManager.data_folder):
            path = DataManager.get_data_file_path()
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    guilds: list[Guild] = pickle.load(f)
                    for g in guilds:
                        DataManager.guilds[g.name] = g

    @staticmethod
    def get_data_keys() -> list[str]:
        return list(DataManager.guilds.keys())

    @staticmethod
    def is_in(name):
        if name in DataManager.guilds:
            return True
        else:
            return False
