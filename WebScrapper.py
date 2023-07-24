from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
import requests
import chromedriver_autoinstaller
from urllib import parse
from Guild import GuildMember, Guild

server_name = {
    "루나": "luna",
    "스카니아": "scania",
    "엘리시움": "elysium",
    "크로아": "croa",
    "오로라": "aurora",
    "제니스": "zenith",
    "이노시스": "enosis",
    "아케인": "arcane",
    "노바": "nova",
    "레드": "red",
    "베라": "bera",
    "유니온": "union",
    "리부트": "reboot",
    "리부트2": "reboot2"
}
server_id = [
    "전체월드",
    "리부트2",
    "리부트",
    "오로라",
    "레드",
    "이노시스",
    "유니온",
    "스카니아",
    "루나",
    "제니스",
    "크로아",
    "베라",
    "엘리시움",
    "아케인",
    "노바",
    "버닝",
    "버닝2"
    "버닝3",
    "버닝4"
]

wid = {
    "리부트2": 46,
    "리부트": 45,
    "오로라": 44,
    "레드": 43,
    "이노시스": 29,
    "유니온": 10,
    "스카니아": 0,
    "루나": 3,
    "제니스": 4,
    "크로아": 5,
    "베라": 1,
    "엘리시움": 16,
    "아케인": 50,
    "노바": 51,
    "버닝": 49,
    "버닝2": 48,
    "버닝3": 52,
    "버닝4": 54
}



class WebScrapper:
    chromedriver_path: str = "driver/"

    def __init__(self) -> None:
        self.driver: webdriver.Chrome

    def set_chrome_driver(self) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        return webdriver.Chrome(service=Service(chromedriver_autoinstaller.install(path=WebScrapper.chromedriver_path)),
                                options=chrome_options)

    def update_guild(self, guild: Guild) -> None:
        maple_gg_need_permissions = "position job last_login level".split(" ")
        maple_page_need_permission = "contribution"
        maple_rank_need_permission = "position job level".split(" ")
        if guild.is_permitted(maple_gg_need_permissions[0]) or \
            guild.is_permitted(maple_gg_need_permissions[1]) or \
            guild.is_permitted(maple_gg_need_permissions[2]) or \
            guild.is_permitted(maple_gg_need_permissions[3]):
            self.get_from_maple_gg(guild)
        if guild.is_permitted(maple_page_need_permission):
            self.get_from_maple_page(guild)
        if guild.is_permitted(maple_rank_need_permission[0]) or \
            guild.is_permitted(maple_rank_need_permission[1]) or \
            guild.is_permitted(maple_rank_need_permission[2]):
            self.get_from_maple_rank(guild)

    def get_from_maple_gg(self, guild: Guild) -> None:
        driver = self.set_chrome_driver()
        url = "https://" + parse.quote(f"maple.gg/guild/{server_name[guild.server]}/{guild.name}")
        driver.get(url)
        element = driver.find_element(By.CLASS_NAME, "btn-outline-success")
        if element.text == "정보갱신":
            element.click()
            alert = Alert(driver)
            alert.accept()
            driver.implicitly_wait(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mb-2"))
            )
        finally:
            pass
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        driver.quit()
        guild_managers = soup.find_all("div", attrs={"class": "member-grade-content"})
        for index, gm in enumerate(guild_managers):
            name = gm.find("a", attrs={"class": "font-size-14 text-black"}).text
            job, level = gm.find("span", attrs={"class": "font-size-12"}).text.strip().replace("Lv.", "").split("/")
            last_login = gm.find("span", attrs={"class": "user-summary-date"}).text().strip().replace("마지막 활동일: ", "")
            if index == 0:
                position = guild.master()
            else:
                position = guild.vise_master()
            guild.append(
                GuildMember(
                    name=name,
                    job=job,
                    level=level,
                    last_login=last_login,
                    position=position
                )
            )

        members = soup.find_all("div", attrs={"class": "col-lg-3 col-md-6 col-sm-6 mt-4"})
        for m in members[len(guild_managers):]:
            name = m.find("a", attrs={"class": "font-size-14 text-grape-fruit"}).text
            job, level = m.find("span", attrs={"class": "font-size-12"}).text.strip().replace("Lv.", "").split("/")
            last_login = m.find("span", attrs={"class": "user-summary-date"}).text.strip().replace("마지막 활동일: ", "")
            guild.append(
                GuildMember(
                    name=name,
                    job=job,
                    level=level,
                    last_login=last_login
                )
            )

    def get_from_maple_page(self, guild: Guild) -> None:
        if guild.is_available_maple_page():

            driver = self.set_chrome_driver()
            driver.get("https://maplestory.nexon.com/Authentication/Login#a")
            driver.find_element(By.ID, "eid").send_keys(guild.maple_id)
            driver.find_element(By.ID, "epw").send_keys(guild.maple_password)
            driver.find_element(By.CLASS_NAME, "login_btn_wrap").click()
            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="gnbMyInfo"]/a/span[1]'))
                )
            except TimeoutException:
                driver.quit()
                print("로그인 실패")
            driver.get("https://maplestory.nexon.com/MyMaple/Profile")
            xpath = "//*[@id='container']/div/div/div/div[1]/div[2]/a/img"
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
            finally:
                element = driver.find_element(By.XPATH, "//*[@id='container']/div/div/div/div[1]/div[2]/a").get_attribute(
                    'href')
            driver.get(element.split("?")[0] + "/GuildMembers" + '?' + element.split("?")[1])
            html = driver.page_source
            driver.quit()
            soup = BeautifulSoup(html, "lxml")
            members = soup.find_all("div", attrs={"class": "fr_name"})
            for m in members:
                name = m.find("a").text
                contribution = m.find("span", attrs={"class": "gd_fr_info"}).text.split(" / ")[1].replace("기여도", "").strip()
                guild.append(
                    GuildMember(
                        name=name,
                        contribution=contribution
                    )
                )

    def get_from_maple_rank(self, guild: Guild) -> None:
        if guild.gid is None:
            rank_url = f"https://maplestory.nexon.com/N23Ranking/World/Guild?w={server_id.index(guild.server)}&n=" + parse.quote(
                f"{guild.name}")
            res = requests.get(rank_url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "lxml")
            href = soup.find("td", attrs={"class": "left"}).find("a")["href"]
            gid = int(href[href.find("gid="):href.find("&wid=")].replace("gid=", ""))
            guild.set_gid(gid)

        else:
            gid = guild.get_gid()
        pre_position = guild.vise_master()
        pre_level = 0
        pre_is_manager = False
        position_count = 2
        for p in range(1, 21):
            guild_url = f"https://maplestory.nexon.com/Common/Guild?gid={gid}&wid={wid[guild.server]}&orderby=1&page={p}"
            res = requests.get(guild_url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "lxml")
            members = soup.find_all("tr")
            if not members:
                break
            for m in members[1:]:
                name = m.find("a").text
                job = m.find("dd").text
                position_data = m.find("td").text
                level = int(m.find("dd").findNext().text.replace("Lv.", ""))
                if position_data == "마스터":
                    position = guild.master()
                    pre_is_manager = True
                    pre_level = level
                elif position_data == "부마스터":
                    position = guild.vise_master()
                    pre_is_manager = True
                    pre_level = level
                else:
                    if pre_level < level:
                        if pre_is_manager:
                            next_position = guild.member_position(1)
                            pre_is_manager = False
                        else:
                            next_position = guild.get_next_position(pre_position)
                        position = next_position
                        pre_position = next_position
                        position_count += 1
                    else:
                        position = pre_position
                        pre_position = position

                    if name in guild.position_highest_level_members:
                        position = guild.position_highest_level_members[name]
                        pre_position = position

                    pre_level = level

                guild.append(
                    GuildMember(
                        name=name,
                        job=job,
                        position=position,
                        level=level
                    )
                )
        if (position_count != guild.get_position_count()):
            # raise here
            pass

    @staticmethod
    def set_driver_path(path: str) -> None:
        WebScrapper.chromedriver_path = path


if __name__ == '__main__':
    guild = Guild(
        server="오로라",
        name="봄날"
    )
    guild.set_position_count(7)
    # guild.add_position_highest_level_member(name="멜론퐁듀", position=guild.member_position(1))
    # guild.add_position_highest_level_member(name="안녕반갑소", position=guild.member_position(2))
    # guild.add_position_highest_level_member(name="밥야", position=guild.member_position(3))
    # guild.add_position_highest_level_member(name="황소령", position=guild.member_position(4))
    guild.add_position_highest_level_member(name="노득장인", position=guild.member_position(5))

    webscrapper = WebScrapper()
    webscrapper.get_from_maple_rank(guild)
    # for i in guild.members:
    #     print(i)
