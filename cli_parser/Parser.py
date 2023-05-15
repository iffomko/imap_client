class Parser:
    @staticmethod
    def parse(args: list) -> dict:
        settings = dict()

        if '-h' in args or '--help' in args:
            settings['help'] = True
            settings['help_text'] = '-h/--help - справка\n' \
                                    '--ssl - разрешить использование ssl, если сервер поддерживает ' \
                                    '(по умолчанию не использовать).\n' \
                                    '-s/--server - адрес (или доменное имя) ' \
                                    'IMAP-сервера в формате адрес[:порт] (порт по умолчанию 143).\n' \
                                    '-n N1 [N2] - диапазон писем, по умолчанию все.\n' \
                                    '-u/--user - имя пользователя, ' \
                                    'пароль спросить после запуска и не отображать на экране.\n'
            return settings

        settings['help'] = False

        settings['ssl'] = False

        if '--ssl' in args:
            settings['ssl'] = True

        if '-u' not in args and '--user' not in args:
            print('Вы не ввели имя пользователя')
            return dict()

        user_key = '-u'

        if '--user' in args:
            user_key = '--user'

        settings['user'] = args[args.index(user_key) + 1]

        if '-s' not in args and '--server' not in args:
            print('Вы не ввели адрес IMAP сервера')
            return dict()

        server_key = '-s'

        if '--server' in args:
            server_key = '--server'

        server = args[args.index(server_key) + 1]

        double_dot_index = server.find(':')

        if double_dot_index == -1:
            settings['addr'] = server
            settings['port'] = 143
        else:
            settings['addr'] = server[0:server.find(':')]
            settings['port'] = int(server[(server.find(':') + 1):len(server)])

        if '-n' not in args:
            print('Вы не ввели диапазон писем')
            return dict()

        try:
            settings['n1'] = int(args[args.index('-n') + 1])
        except ValueError:
            print('Вы ввели не корректное значение для n1')
            return dict()

        try:
            settings['n2'] = int(args[args.index('-n') + 2])
        except ValueError:
            settings['n2'] = 'all'

        if settings['n2'] != 'all' and settings['n1'] > settings['n2']:
            print('Вы ввели некорректный диапазон')
            return dict()

        return settings

