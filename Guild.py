from typing import Generator, Self


class GuildMember:

    def __init__(self,
                 name,
                 position=None,
                 job=None,
                 level=None,
                 last_login=None,
                 contribution=None,
                 ) -> None:
        self.name = name
        self.position = position
        self.job = job
        self.level = level
        self.last_login = last_login
        self.contribution = contribution

    def update(self, member: Self,
               overwrite_position=True,
               overwrite_job=True,
               overwrite_level=True,
               overwrite_last_login=True,
               overwrite_contribution=True
               ) -> None:
        self.position = member.position
        self.job = member.job
        self.level = member.level
        self.last_login = member.last_login
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

    def __init__(self, server=None, name=None, gid=None) -> None:
        self.members: list[GuildMember] = list()
        self.members_names: dict[str, int] = dict()
        self.server: str = server
        self.name: str = name
        self.maple_id: str = str()
        self.maple_password: str = str()
        self.gid: int = gid
        self.position_count: int = 5
        self.position_alias: list[str] = list()
        self.position_highest_level_members: dict[str, str] = dict()
        self.vacant_positions: set = set()

    def __getitem__(self, item) -> GuildMember:
        return self.members[item]

    def __len__(self) -> int:
        return len(self.members)

    def __delitem__(self, key) -> None:
        for m in self.members[key:]:
            self.members_names[m.name] -=1
        del self.members[key]

    def __eq__(self, other: Self):
        if other.name == self.name:
            return True
        else:
            return False

    def get_gid(self) -> int:
        return self.gid

    def get_member_positions(self) -> Generator[str, None, None]:
        for p in self.position_name[2:]:
            yield p

    def get_member_count(self):
        return self.position_count-2

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
        적용시키려는 직위 이름이 길드가 가지고 있을 직위의 개수를 넘어가는 직위 번호라면 (예를 들어 position count 변수가 )
        길드 클래스가 가지고 있는 직위 개수값이 틀렸을 것이라는 판단하에 직위 개수값을 변경한다.
    '''

    def set_position_alias(self, name, alias) -> None:
        if name in self.position_name:
            position_index = self.position_name.index(name)
            if position_index >= self.position_count:
                self.position_count = position_index + 1
            self.position_alias[name] = alias
        else:
            # raise here
            pass


    def append(self, item: GuildMember, overwrite: bool = False) -> None:
        if item.name in self.members_names:
            index = self.members_names[item.name]
            self.members[index].update(item)

        else:
            self.members_names[item.name] = len(self.members)
            self.members.append(item)

    def remove(self, item: GuildMember):
        if item.name in self.members_names:
            index = self.members_names[item.name]
            for m in self.members[index:]:
                self.members_names[m.name] -= 1
            del self.members[index]
