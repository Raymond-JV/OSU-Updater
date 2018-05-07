from gooey import Gooey
from gooey import GooeyParser

from src.cmd_menu import run


@Gooey(program_name='Download Missing Beatmaps')
def display():
    parser = GooeyParser(description="OSU! Updater")
    parser.add_argument('Username', type=str)
    parser.add_argument('Password', type=str, widget='PasswordField')

    args = parser.parse_args()
    run(args.Username, args.Password)


display()
