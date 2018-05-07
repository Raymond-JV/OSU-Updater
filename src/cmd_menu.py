import argparse
import getpass

from selenium import webdriver

from src.parser import Authenticator
from src.parser import ClearedParser


def pre_processing():
    pass


def command_line():
    parse = argparse.ArgumentParser(description="OSU! Beatmaps Updater")
    parse.add_argument('-u', '--username', help='OSU! username required for homepage login', type=str, required=True)
    parse.add_argument('-v', '--verbose', help="Display Status")
    args = parse.parse_args()

    password = getpass.getpass('OSU! Password:')
    run(args.username, password)


def run(user, password):
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    auth = Authenticator(driver, user, password)
    auth.login()
    downloader = ClearedParser(driver)
    downloader.init()


command_line()
