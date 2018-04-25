import os
from enum import Enum


class SongManager:

    class File(Enum):
        osu_ext = '.osu'
        song_dir = 'Songs'

    def __init__(self):
        self.osu_dir = os.path.abspath(os.sep)
        self.downloaded = None
        self.find_downloaded_songs()

    def find_downloaded_songs(self, dir_loc):
        if self.verify_osu_root(dir_loc):
            self.downloaded = os.listdir(dir_loc)
        return self.downloaded

    def find_downloaded_songs(self):
        if self.downloaded is not None:
            return self.downloaded
        else:
            songs_loc = self.find_dir()
            if songs_loc is not None:
                self.downloaded = os.listdir(songs_loc)

    def find_dir(self):
        for root, dirs, file in os.walk(self.osu_dir):
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

    def add_song(self, song):
        pass
