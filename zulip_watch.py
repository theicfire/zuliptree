#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import optparse
import random
from pymongo import MongoClient
import zulip

client = MongoClient('104.131.112.57', 49158)
db = client.zulipTree
messages = db['messages']


def main():
    usage = """message-watch --user=<bot's email address> --api-key=<bot's api key> [options]

    Prints out each message received by the indicated bot or user.

    Example: message-watch --user=tabbott@zulip.com --api-key=a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5

    You can omit --user and --api-key arguments if you have a properly set up ~/.zuliprc
    """

    parser = optparse.OptionParser(usage=usage)
    parser.add_option_group(zulip.generate_option_group(parser))
    (options, args) = parser.parse_args()

    client = zulip.init_from_options(options)

def print_message(message):
    print 'Someone said: ', message['content']
    print 'Inserting Message:', message
    messages.insert(message)

def zulip_watch(email, api_key):
    print 'Watching for Zulip Messages'
    client = zulip.Client(email=email, api_key=api_key, config_file=None,
                  verbose=False, site=None, client='API: Python')
    client.call_on_each_message(print_message)

# This is a blocking call, and will continuously poll for new messages
if __name__ == '__main__':
    main()