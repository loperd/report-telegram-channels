import sys
import os
import random
import re
import time

from urllib.request import urlopen
from telethon.sync import TelegramClient
from telethon import functions, types


def print_help() -> None:
    print('Usage:')
    print('\tpython main.py <api_id> <api_hash> <channel_list_url>')


def get_dirty_channels(filepath) -> list:
    with urlopen(filepath) as request:
        charset = request.info().get_content_charset()
        return request.read().decode(charset).split('\n')


def get_messages() -> list:
    with open(os.path.join(os.path.dirname(os.path.relpath(__file__)), 'messages.txt'), 'r') as fp:
        messages = fp.readlines()

    return messages


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_help()
        exit(1)

    api_id = int(sys.argv[1])
    api_hash = sys.argv[2]
    dirty_channels_filepath = sys.argv[3]

    dirty_channels = get_dirty_channels(dirty_channels_filepath)
    messages = get_messages()

    try:
        with TelegramClient('ReportDirtyChannels', api_id, api_hash) as client:
            for dirty_channel in dirty_channels:
                dirty_channel = dirty_channel.strip()
                msg = random.choice(messages).strip()
                try:
                    result = client(functions.account.ReportPeerRequest(
                        peer=client.get_entity(dirty_channel),
                        reason=types.InputReportReasonOther(),
                        message=msg
                    ))
                    print('{}: {} - {}'.format(dirty_channel, result, msg))
                    time.sleep(40 + random.randint(1, 128))
                except Exception as e:
                    exception_msg = str(e)
                    print('{}: error - {}'.format(dirty_channel, exception_msg))
                    # A wait of 70088 seconds is required (caused by ResolveUsernameRequest)
                    res = re.search(r"wait of (\d+) seconds", exception_msg)
                    if res:
                        delay = int(res.group(1)) + 10
                        print('Waiting for {} seconds... Time to get a new api_id/api_hash!'.format(delay))
                        time.sleep(delay)
    except KeyboardInterrupt:
        print('Closed..')

