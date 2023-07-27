from Guild import Guild
from WebScrapper import WebScrapper, server_name
import pickle
import os
from typing import Generator, Callable


class DataManager:
    position_names = [
                         "길드 마스터",
                         "길드 부마스터"
                     ] + [f"길드 멤버원{n}" for n in range(1, 11)]
    guilds: dict[str, dict[str, Guild]] = {s:dict() for s in server_name}
    data_folder: str = "data"
    data_file_name: str = "data.pkl"
    current_guild_name: str = str()
    current_guild_server: str = str()
    update_functions: list[Callable[[], None]] = list()

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_data_file_path() -> str:
        return os.path.join(DataManager.data_folder, DataManager.data_file_name)

    @staticmethod
    def get_guilds(server: str) -> Generator[Guild, None, None]:
        if server != "":
            for g_n in DataManager.guilds[server]:
                yield DataManager.guilds[server][g_n]

    @staticmethod
    def get_servers() -> Generator[str,None,None]:
        for s in DataManager.guilds:
            if len(DataManager.guilds[s])>0:
                yield s


    @staticmethod
    def get_guild(server, name):
        return DataManager.guilds[server][name]

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
    def set_current_guild(server: str, name: str) -> None:
        DataManager.current_guild_server = server
        DataManager.current_guild_name = name

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
    def posisiton_kor_to_eng(kor_position) -> str:
        index = DataManager.position_names.index(kor_position)
        eng_position = Guild.position_name[index]
        return eng_position

    @staticmethod
    def update_changes() -> None:
        for f in DataManager.update_functions:
            f()

    @staticmethod
    def add_update_function(func: Callable[[], None]) -> None:
        DataManager.update_functions.append(func)

    @staticmethod
    def server_eng_to_kor(eng_server) -> str:
        for k in server_name:
            if server_name[k] == eng_server:
                return k

    @staticmethod
    def get_current_position_length() -> int:
        return DataManager.get_current_guild().get_position_count()

    @staticmethod
    def get_position_alias(kor_position) -> str:
        index = DataManager.position_names.index(kor_position)
        eng_position = Guild.position_name[index]
        return DataManager.get_current_guild().get_position_alias(eng_position)

    @staticmethod
    def get_position_name(index) -> str:
        return DataManager.position_names[index]

    @staticmethod
    def set_current_permission(position, job, level, last_login, contribution) -> None:
        current_guild = DataManager.get_current_guild()
        current_guild.set_permissions(
            position=position,
            job=job,
            level=level,
            last_login=last_login,
            contribution=contribution
        )

    @staticmethod
    def get_current_permission() -> dict[str,str]:
        current_guild = DataManager.get_current_guild()
        return current_guild.get_permissions()

    @staticmethod
    def add_current_highest_level_member(name, position) -> None:
        current_guild= DataManager.get_current_guild()
        current_guild.add_position_highest_level_member(name=name, position=position)

    @staticmethod
    def clear_current_highest_level_members() -> None:
        current_guild = DataManager.get_current_guild()
        current_guild.clear_highest_level_members()

    @staticmethod
    def get_current_highest_level_members():
        current_guild = DataManager.get_current_guild()
        return current_guild.get_highest_level_members()

    @staticmethod
    def get_current_available_positions() -> list[str]:
        current_guild = DataManager.get_current_guild()
        return [p for p in current_guild.get_available_positions()]