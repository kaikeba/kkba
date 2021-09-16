import getopt

from .ulti import *


def main():
    _opts = ['help', 'version']
    _s_opts = 'rfFsSvVh'
    opt, arg = getopt.getopt(sys.argv[1:], _s_opts, _opts)
    color, feed_back = convert_main(opt)
    console = Console()
    console.print(f'=' * os.get_terminal_size()[0], justify='center')
    console.print(f'[bold {color}]{feed_back}[/]', justify='center')
    console.print(f'=' * os.get_terminal_size()[0], justify='center')


if __name__ == '__main__':
    main()
