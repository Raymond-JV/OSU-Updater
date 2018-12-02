import argparse
import getpass

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from src.parser import Authenticator
from src.parser import ClearedParser


def command_line():
    parse = argparse.ArgumentParser(description="OSU! Beatmaps Updater")
    parse.add_argument('-u', '--username', help='OSU! username required for homepage login', type=str, required=True)
    parse.add_argument('-v', '--verbose', help="Display Status")
    args = parse.parse_args()

    password = getpass.getpass('OSU! Password:')
    run(args.username, password)


def create_driver():
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options)
    driver.implicitly_wait(10)
    return driver


def run(user, password):
    driver = create_driver()
    auth = Authenticator(driver, user, password)
    auth.login()
    downloader = ClearedParser(driver)
    downloader.init()


command_line()
