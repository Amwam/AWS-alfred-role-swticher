#!/usr/bin/python
# encoding: utf-8

import json
import sys
from os.path import expanduser

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3


def main(wf):
    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    args = wf.args
    query = None
    if len(wf.args):
        query = wf.args[0]

    home = expanduser("~")

    with open('{}/.aws/config'.format(home)) as f:
        lines = [line.replace('\n','') for line in f.readlines()]

    log.info(lines)

    roles = []
    current_role = {}
    for line in lines:
        if '[profile ' in line:
            current_role['title'] = line.replace('[profile ', '').replace(']', '')
        elif 'role_arn' in line:
            role_arn = line.replace('role_arn = ', '')
            split = role_arn.split('/')
            role = split[1]
            account_id = split[0].replace('arn:aws:iam::', '').replace(':role', '')
            current_role['role'] = role
            current_role['account_id'] = account_id
        else:
            if current_role:
                roles.append(current_role)
                current_role = {}

    items = wf.filter(query, roles, lambda x: x['title'])

    if not items:
        wf.add_item('No matches')

    log.info('Adding items')
    for item in items:
        log.info('Adding {}'.format(item))

        wf.add_item(title=item['title'],
        subtitle='Account: {}'.format(item['account_id']),
        valid=True,
        arg=('https://signin.aws.amazon.com/'
             'switchrole?account={}&roleName={}&displayName={}').format(
                item['account_id'],
                item['role'],
                item['title']
            )
        )

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    log = wf.logger
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
