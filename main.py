import hashlib
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
        return fp.readlines()


def get_remote_md5_sum(url):
    return hash_remote_file(urlopen(url), "md5")


def hash_remote_file(remote, algorithm="md5"):
    max_file_size = 100 * 1024 * 1024

    if algorithm == "md5":
        hash_type = hashlib.md5()
    elif algorithm == "sha1":
        hash_type = hashlib.sha1()
    elif algorithm == "sha256":
        hash_type = hashlib.sha256()
    elif algorithm == "sha384":
        hash_type = hashlib.sha384()
    elif algorithm == "sha512":
        hash_type = hashlib.sha512()
    else:
        raise Exception("Hash type '{}' not found.".format(algorithm))

    total_read = 0
    while True:
        data = remote.read(4096)
        total_read += 4096

        if not data or total_read > max_file_size:
            break

        hash_type.update(data)

    return hash_type.hexdigest()


def report_dirty_channel(client, channel, message):
    try:
        result = client(functions.account.ReportPeerRequest(
            peer=client.get_entity(channel),
            reason=types.InputReportReasonOther(),
            message=message))

        print('{}: {} - {}'.format(channel, result, message))

        return result
    except Exception as e:
        exception_msg = str(e)
        print('{}: error - {}'.format(channel, exception_msg))
        # A wait of 70088 seconds is required (caused by ResolveUsernameRequest)
        res = re.search(r"wait of (\d+) seconds", exception_msg)
        if res:
            delay = int(res.group(1)) + 10
            print("\nWaiting for {} seconds... Time to get a new api_id/api_hash!\n".format(delay))
            time.sleep(delay)


def report_dirty_channels(api_id, api_hash):
    session_file_path = 'data/{}/{}'.format(api_id, api_hash)
    with TelegramClient(session_file_path, api_id, api_hash) as tg_client:
        with open(result_file_path, 'a+') as result_file:
            result_file.seek(0)
            result_file_content = result_file.read()
            for dirty_channel in dirty_channels:
                dirty_channel = dirty_channel.strip()
                if dirty_channel in result_file_content:
                    print("Skipped the channel {} because it has already reported it.".format(dirty_channel))
                    continue
                msg = random.choice(messages).strip()
                if not report_dirty_channel(tg_client, dirty_channel, msg):
                    time.sleep(40 + random.randint(1, 128))
                    continue
                if len(result_file_content) > 0:
                    result_file.write("\n")

                result_file.write(dirty_channel)
                result_file.flush()

                time.sleep(40 + random.randint(1, 128))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_help()
        exit(1)

    app_api_id = int(sys.argv[1])
    app_api_hash = sys.argv[2]
    dirty_channels_file_url = sys.argv[3]

    messages = get_messages()

    result_file_path = os.path.join(
        os.path.dirname(os.path.relpath(__file__)),
        'data/{}/reported.txt'.format(app_api_id)
    )

    result_file_directory = os.path.dirname(result_file_path)
    if not os.path.exists(result_file_directory):
        os.makedirs(result_file_directory)

    latest_hash_sum = ''
    wait_secs = 30

    try:
        while True:
            dirty_channels = get_dirty_channels(dirty_channels_file_url)
            new_hash_sum = get_remote_md5_sum(dirty_channels_file_url)

            if new_hash_sum == latest_hash_sum:
                print("Wait {} seconds for next updates.".format(wait_secs))
                time.sleep(wait_secs)
                continue

            latest_hash_sum = new_hash_sum

            report_dirty_channels(api_id=app_api_id, api_hash=app_api_hash)
    except KeyboardInterrupt:
        print('Closed..')
