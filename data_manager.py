from Guild import Guild
import pickle
import os
from typing import Generator, Callable


class DataManager:
    position_names = [
                         "길드 마스터",
                         "길드 부마스터"
                     ] + [f"길드 멤버원{n}" for n in range(1, 11)]
    guilds: dict[str, dict[str, Guild]] = dict()
    data_folder: str = "data"
    data_file_name: str = "data.pkl"
    current_guild_name: str = str()
    current_guild_server: str = str()
    update_functions: list[Callable[[],None]] = list()

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
    def add_guild(name: str, server: str, position_count: int) -> None:
        new_guild = Guild(server=server, name=name, position_count=position_count)
        DataManager.guilds[server][name] = new_guild

    @staticmethod
    def set_guild_account(name: str, server: str, maple_id: str, password: str) -> None:
        DataManager.guilds[server][name].set_account(maple_id=maple_id, password=password)

    @staticmethod
    def set_guild_position_alias(name: str, server: str, position: str, alias: str):
        DataManager.guilds[server][name].set_position_alias(position=position, alias=alias)

    @staticmethod
    def posisiton_kor_to_eng(kor_position):
        index = DataManager.position_names.index(kor_position)
        eng_position = Guild.position_name[index]
        return eng_position

    @staticmethod
    def update_signal():
        for f in DataManager.update_functions:
            f()

    @staticmethod
    def add_update_function(func: Callable[[],None]):
        DataManager.update_functions.append(func)
