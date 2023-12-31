from typing import Generator, Self


class GuildMember:

    def __init__(self,
                 name:str,
                 position: str=None,
                 job: str=None,
                 level:int=None,
                 last_login:int=None,
                 contribution:int=None,
                 ) -> None:
        self.name:str = name
        self.position:str = position
        self.job:str = job
        self.level:int = level
        self.last_login:int = last_login
        self.contribution:int = contribution

    def update(self, member: Self,
               permissions: dict[str]
               ) -> None:
        if permissions["position"]:
            self.position = member.position
        if permissions["job"]:
            self.job = member.job
        if permissions["level"]:
            self.level = member.level
        if permissions["last_login"]:
            self.last_login = member.last_login
        if permissions["contribution"]:
            self.contribution = member.contribution

    def __str__(self) -> str:
        answer = f"이름 : {self.name}\n"
        if self.position:
            answer += f"직위 : {self.position}\n"
        if self.job:
            answer += f"직업 : {self.job}\n"
        if self.level:
            answer += f"레벨 : {self.level}\n"
        if self.last_login:
            answer += f"마지막 접속일 : {self.last_login}\n"
        if self.contribution:
            answer += f"기여도 : {self.contribution}\n"
        return answer


'''
    @parameter
        server: 메이플 서버 한글로
        name: 길드 이름 한글로
        gid: 이건 Webscrapper로 얻는 데이터임
        
'''


class Guild:
    position_name: list[str] = ["gm", "gvm", "gmem1", "gmem2", "gmem3", "gmem4",
                                "gmem5", "gmem6", "gmem7", "gmem8", "gmem9", "gmem10"]

    def __init__(self, server: str, name: str, position_count: int = 5) -> None:
        self.members: list[GuildMember] = list()
        self.members_names: dict[str, int] = dict()
        self.server: str = server
        self.name: str = name
        self.maple_id: str = str()
        self.maple_password: str = str()
        self.gid: int = int()
        self.position_count: int = position_count
        self.position_alias: dict[str, str] = dict()
        self.position_highest_level_members: dict[str, str] = dict()
        self.vacant_positions: set = set()
        self.property_permissions: dict[str, bool] = {
            "position": True,
            "job": True,
            "level": True,
            "last_login": True,
            "contribution": True
        }
        self.exception_members: set = set()

    def __getitem__(self, item) -> GuildMember:
        return self.members[item]

    def __len__(self) -> int:
        return len(self.members)

    def __delitem__(self, key) -> None:
        for m in self.members[key:]:
            self.members_names[m.name] -= 1
        del self.members[key]

    def __eq__(self, other: Self) -> bool:
        if other.name == self.name:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self.server} 서버의 {self.name} 길드"

    def get_maple_id(self):
        return self.maple_id

    def get_maple_password(self):
        return self.maple_password

    def get_name(self):
        return self.name

    def get_server(self):
        return self.server

    def get_members(self):
        return self.members

    def get_jobs(self) -> list[str]:
        jobs = set()
        for m in self.members:
            jobs.add(m.job)
        return list(jobs)

    def get_permitted_properties(self) -> Generator[str, None, None]:
        for p in self.property_permissions:
            yield p

    def is_available_maple_page(self) -> bool:
        if self.maple_id is not None and self.maple_password is not None:
            return True
        else:
            return False

    def get_available_positions(self) -> Generator[str, None, None]:
        for p in self.position_name[:self.position_count]:
            yield p

    def get_gid(self) -> int:
        return self.gid

    def get_member_positions(self) -> Generator[str, None, None]:
        for p in self.position_name[2:]:
            yield p

    def get_member_count(self) -> int:
        return self.position_count - 2

    def get_position_count(self) -> int:
        return self.position_count

    def get_position_index(self, position) -> int:
        return self.position_name.index(position)

    def get_next_position(self, position: str) -> str:
        index = self.position_name.index(position)
        if index < self.position_count:
            return self.position_name[index + 1]
        else:
            return position

    def get_account(self):
        data:dict[str,str] = dict()
        data["id"] = self.maple_id
        data["pw"] = self.maple_password
        return data

    def master(self) -> str:
        return Guild.position_name[0]

    def vise_master(self) -> str:
        return self.position_name[1]

    def add_position_highest_level_member(self, name, position) -> None:
        self.position_highest_level_members[name] = position

    def set_gid(self, gid) -> None:
        self.gid = gid

    def member_position(self, num) -> str:
        return self.position_name[num + 1]

    def set_account(self, maple_id, password) -> None:
        self.maple_id = maple_id
        self.maple_password = password

    def set_position_count(self, count) -> None:
        self.position_count = count

    '''
        
    '''

    def set_position_alias(self, position, alias) -> None:
        if position in self.position_name:
            # this may cause bugs
            # position_index = self.position_name.index(name)
            # if position_index >= self.position_count:
            #     self.position_count = position_index + 1
            self.position_alias[position] = alias
        else:
            raise KeyError

    def append(self, item: GuildMember) -> None:
        if item.name in self.exception_members:
            pass
        elif item.name in self.members_names:
            index = self.members_names[item.name]
            self.members[index].update(item, self.property_permissions)

        else:
            self.members_names[item.name] = len(self.members)
            self.members.append(item)

    def remove(self, item: GuildMember) -> None:
        if item.name in self.members_names:
            index = self.members_names[item.name]
            for m in self.members[index:]:
                self.members_names[m.name] -= 1
            del self.members[index]

    def is_permitted(self, permission: str) -> bool:
        if self.property_permissions[permission]:
            return True
        else:
            return False

    def get_permissions(self) -> dict:
        return self.property_permissions

    def set_permissions(self, position, job, level, last_login, contribution) -> None:
        self.property_permissions["position"] = position
        self.property_permissions["job"] = job
        self.property_permissions["level"] = level
        self.property_permissions["last_login"] = last_login
        self.property_permissions["contribution"] = contribution

    def clear_highest_level_members(self) -> None:
        self.position_highest_level_members = {}

    def get_position_alias(self, position) -> str:
        if position in self.position_alias:
            return self.position_alias[position]
        else:
            return None


    def get_highest_level_members(self) -> dict[str, str]:
        return self.position_highest_level_members