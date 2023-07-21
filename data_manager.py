from Guild import Guild
import pickle
import os
from typing import Generator

class DataManager:
    guilds: dict[str, dict[str, Guild]] = dict()
    data_folder: str = "data"
    data_file_name: str = "data.pkl"
    current_guild_name: str = str()
    current_guild_server: str = str()

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_data_file_path() -> str:
        return os.path.join(DataManager.data_folder, DataManager.data_file_name)

    @staticmethod
    def get_guilds() -> Generator[Guild, None, None]:
        for g_s in DataManager.guilds:
            for g_n in DataManager.guilds[g_s]:
                yield DataManager.guilds[g_s][g_n]

    @staticmethod
    def save() -> None:
        with open(DataManager.get_data_file_path(), "wb") as f:
            pickle.dump(DataManager.guilds, f)

    @staticmethod
    def load() -> None:
        if os.path.isdir(DataManager.data_folder):
            path = DataManager.get_data_file_path()
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    guilds: list[Guild] = pickle.load(f)
                    for g in guilds:
                        DataManager.guilds[g.server][g.name] = g

    @staticmethod
    def get_data_keys() -> list[str]:
        return list(DataManager.guilds.keys())

    @staticmethod
    def is_in(name) -> bool:
        if name in DataManager.guilds:
            return True
        else:
            return False

    @staticmethod
    def set_current_guild(guild: Guild) -> None:
        DataManager.current_guild_name = guild.name
        DataManager.current_guild_server = guild.server

    @staticmethod
    def get_current_guild() -> Guild:
        if DataManager.current_guild_name != "":
            return DataManager.guilds[DataManager.current_guild_server][DataManager.current_guild_name]
        else:
            return Guild(server="", name="")

    @staticmethod
    def add_guild(name:str, server:str, position_count: int) -> None:
        new_guild = Guild(server=server, name=name, position_count= position_count)
        DataManager.guilds[server][name] = new_guild

    @staticmethod
    def set_guild_account(name:str, server:str, maple_id:str, password:str) -> None:
        pass