import email
import getpass
from email.header import decode_header
from imaplib import IMAP4_SSL, IMAP4


class ImapClient:
    @staticmethod
    def print_message(status: str, response: str):
        if status.lower() != 'ok':
            print(str(response))
        else:
            print(f'{status}: {str(response)}')

    @staticmethod
    def decode_list(list_data: list) -> str:
        result = []

        for data_tuple in list_data:
            data, charset = data_tuple

            if charset is not None:
                result.append(data.decode(charset))
                continue

            if isinstance(data, bytes):
                result.append(data.decode())
                continue

            result.append(data)

        return ', '.join(result)

    def print_messages(self, settings: dict):
        imap_server = None

        if settings.get('ssl'):
            imap_server = IMAP4_SSL(settings['addr'], settings['port'])
        else:
            imap_server = IMAP4(settings['addr'], settings['port'])

        settings['password'] = getpass.getpass('Введите пароль: ')

        status = None
        response = None

        try:
            status, response = imap_server.login(settings.get('user'), settings.get('password'))
        except IMAP4.error as e:
            print(f'Error: {e}')
            return

        self.print_message(status, str(response))

        try:
            imap_server.starttls()
        except IMAP4.abort as e:
            print(f'Error: {e}')

        imap_server.select('INBOX')
        status, message_ids = imap_server.search(None, 'ALL')

        message_ids = message_ids[0].split()

        for ind in message_ids:
            id_value = int(ind.decode())

            if id_value < settings.get('n1'):
                break

            if settings.get('n2') != 'all' and settings.get('n2') < id_value:
                break

            status, messages = imap_server.fetch(ind, '(RFC822)')
            self.print_message(status, f'Message by id {id_value} was get')

            data = messages[0][1]

            msg = email.message_from_bytes(data)

            sender = self.decode_list(decode_header(msg['From']))
            subject = self.decode_list(decode_header(msg['Subject']))

            to = msg['To']
            date = msg['Date']

            message_size = len(data)

            print(f'\nMessage, from: {sender}, to: {to}, subject: {subject}, '
                  f'date: {date}, message size: {message_size}\n')

        imap_server.close()
        imap_server.logout()
