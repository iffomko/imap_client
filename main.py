import sys

from cli_parser.Parser import Parser
from imap.imap_client import ImapClient


def main():
    settings = Parser().parse(sys.argv)

    if settings.get('help'):
        print(settings.get('help_text'))
        return

    ImapClient().print_messages(settings)


if __name__ == '__main__':
    main()

