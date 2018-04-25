from enum import Enum
from typing import NamedTuple
from selenium import webdriver
from collections import namedtuple
from src.song_manager import SongManager


class PageLink(Enum):
    login = 'https://osu.ppy.sh/forum/ucp.php?mode=login'
    beatmaps = 'https://osu.ppy.sh/beatmaps/packs?type=standard&page='
    extension = '/download'
    href = 'href'
    start_page = 1


class Element(Enum):
    user_field = 'username'
    password_field = 'password'
    login_confirm = 'btnmain'
    pack = 'beatmap-pack'
    pack_name = 'beatmap-pack__name'
    song_set = 'beatmap-pack-items__set'
    song_status = 'beatmap-pack-items__icon'
    song_title = 'beatmap-pack-items__title'
    song_artist = 'beatmap-pack-items__artist'
    cleared_property = 'cleared'
    title_property = 'title'
    song_download = 'beatmap-pack-items__link'


class Authenticator:

    def __init__(self, driver: webdriver, user, password):
        self.driver = driver
        self.user = user
        self.password = password

    def __type_login(self):
        user_element = self.driver.find_element_by_name(Element.user_field.value)
        user_element.send_keys(self.user)

    def __type_password(self):
        password_element = self.driver.find_element_by_name(Element.password_field.value)
        password_element.send_keys(self.password)

    def login(self):
        self.driver.get(PageLink.login.value)
        self.__type_login()
        self.__type_password()
        self.driver.find_element_by_class_name(Element.login_confirm.value).click()
        for c in self.driver.get_cookies():
            print(c)


class ClearedParser:

    class SongInfo(NamedTuple):
        artist: str
        href: str
        pack_name: str

    def __init__(self, driver):
        self.page = 1
        self.driver = driver
        self.manager = SongManager()

    def init(self):
        while self.parse_page() != 0:
            pass

    def find_packs(self):
        self.driver.get(PageLink.beatmaps.value + str(self.page))
        return self.driver.find_elements_by_class_name(Element.pack.value)

    def parse_page(self):
        packs = self.find_packs()
        for pack in packs:
            self.parse_pack(pack)
        self.page += 1
        return len(packs)

    def parse_pack(self, pack):
        pack.click()
        songs = pack.find_elements_by_class_name(Element.song_set.value)
        self.parse_songs(pack, songs)

    def parse_songs(self, pack, songs):
        pack_name_element = pack.find_element_by_class_name(Element.pack_name.value)
        pack_name = str(pack_name_element.text).strip()
        for song in songs:
            self.parse_song(song, pack_name)

    def parse_song(self, attributes, pack_name):
        cleared = attributes.find_element_by_class_name(Element.song_status.value)
        needed = cleared.get_property(Element.title_property.value).strip()
        if needed != Element.cleared_property.value:
            return
        self.extract_info(attributes, pack_name)

    def extract_info(self, song, pack_name):
        title = song.find_element_by_class_name(Element.song_title.value).text.strip()
        self.verify(title, song, pack_name)
        artist = song.find_element_by_class_name(Element.song_artist.value).text
        download = self.find_download_page(song)
        self.update_by_title(title, artist, download, pack_name)

    def verify(self, title, song, pack_name):
        if title == "":
            self.extract_info(song, pack_name)

    def update_by_title(self, title, artist, download, pack_name):
        SongInfo = namedtuple('SongInfo', 'title artist download pack_name')
        entry = SongInfo(title, artist, download, pack_name)
        downloaded = self.manager.find_downloaded_songs()
        if entry.title not in downloaded:
            self.manager.add_song(entry)

    def find_download_page(self, song):
        download_element = song.find_element_by_class_name(Element.song_download.value)
        link = download_element.get_property(PageLink.href.value)
        return link + PageLink.extension.value
