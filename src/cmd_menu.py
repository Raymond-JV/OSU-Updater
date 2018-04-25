import argparse
import getpass
from src.parser import Authenticator
from src.parser import ClearedParser
from selenium import webdriver


def pre_processing():
    pass


def command_line():

    parse = argparse.ArgumentParser(description="OSU! Beatmaps Updater")
    parse.add_argument('-u', '--username', help='OSU! username required for homepage login', type=str, required=True)
    parse.add_argument('-p', '--password', help='OSU! password required for homepage login', type=str)
    parse.add_argument('-v', '--verbose', help="Display Status")
    args = parse.parse_args()

    if not args.password:
        args.password = getpass.getpass('OSU! Password:')

    run(args.username, args.password)


def run(user, password):

    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    auth = Authenticator(driver, user, password)
    auth.login()
    downloader = ClearedParser(driver)
    downloader.init()


command_line()


