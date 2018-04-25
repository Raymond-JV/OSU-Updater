import getpass
from gooey import Gooey
from gooey import GooeyParser


def pre_processing():
    pass


@Gooey(program_name='Download Missing Beatmaps')
def command_line():

    parser = GooeyParser(description="OSU! Updater")
    parser.add_argument('Username', type=str)
    parser.add_argument('Password', type=str, widget='PasswordField')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass('OSU! Password:')


command_line()





