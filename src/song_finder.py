import os
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

import requests

SongInfo = namedtuple('SongInfo', 'title artist link pack_name')


class SongAdder:

    def __init__(self, driver):
        self.song_finder = SongFinder()
        self.song_downloader = SongDownloader(self.song_finder.get_osu_home(), driver)

    def add_song(self, song: SongInfo):
        if not self.song_finder.has_song(song.title):
            self.song_downloader.download(song.link)


class SongFinder:
    class File(Enum):
        osu_ext = '.osu'
        song_dir = 'Songs'

    def __init__(self):
        self.root_dir = os.path.abspath(os.sep)
        self.osu_dir = self.find_dir()
        self.downloaded = self.find_downloaded_songs()

    def has_song(self, song_name):
        return song_name in self.downloaded

    def get_osu_home(self):
        return self.osu_dir

    def find_downloaded_songs(self):
        if self.verify_osu_root(self.osu_dir):
            self.downloaded = os.listdir(self.osu_dir)
        return self.downloaded

    def find_dir(self):
        for root, dirs, file in os.walk(self.root_dir):
            for d in dirs:
                dir_loc = self.scan_dir(d, root)
                if dir_loc is not None:
                    return dir_loc

    def scan_dir(self, directory, root):
        if directory == self.File.song_dir.value:
            dir_loc = os.path.join(root, directory)
            if self.verify_osu_root(dir_loc):
                return dir_loc

    def verify_osu_root(self, directory):
        for root, dirs, file in os.walk(directory):
            if self.File.osu_ext.value in str(file):
                return True
        return False


class SongDownloader:
    class Http(Enum):
        disposition = 'Content-Disposition'
        length = 'Content-Length'
        file_name_param = 'filename'
        buffer_size = 2 ** 15
        song_throttle = 8

    def __init__(self, osu_dir, driver):
        self.session = requests.session()
        self.osu_dir = osu_dir
        self.download_queue = ThreadPoolExecutor(max_workers=self.Http.song_throttle.value)
        for cookie in driver.get_cookies():
            name = cookie['name']
            payload = cookie['value']
            self.session.cookies.set(name, payload)

    def download(self, link):
        self.download_queue.submit(self.__async_download, link)

    def __async_download(self, link):
        song_data = self.session.get(link)
        song_name = song_data.headers[self.Http.disposition.value]
        song_size = song_data.headers[self.Http.length.value]
        song_name = self.remove_markup(song_name.split(';filename=')[1])
        song_size = self.remove_markup(song_size)
        self.verify_write_file(song_name, song_size, song_data)

    def remove_markup(self, attribute):
        attribute = attribute.strip(';').strip('"')
        return attribute

    def verify_write_file(self, song_name, song_size, song_data):
        song_path = self.osu_dir + '\\' + song_name

        exists = os.path.exists(song_path)

        if exists and os.path.getsize(song_path) < song_size:
            print("Corrupt file detected. Redownloading %s." % song_name)
            self.write_song(song_path, song_data)

        elif not exists:
            print("Adding %s" % song_name)
            self.write_song(song_path, song_data)
        else:
            print("%s already owned" % song_name)

    def write_song(self, song_path, song_data):
        with open(song_path, 'wb') as f:
            for chunk in song_data.iter_content(self.Http.buffer_size.value):
                f.write(chunk)
        print("Wrote beatmap to %s" % song_path)
