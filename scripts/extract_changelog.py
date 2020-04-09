#!/usr/bin/env python

import sys
import re
from argparse import ArgumentParser

try:
    from urllib.parse import quote as quote_uri
except ImportError:
    from urllib import quote as quote_uri

IGNORE_LINES = [
    'github_changelog_generator',
]


def line_ignored(line):
    for term in IGNORE_LINES:
        if term in line:
            return True
    return False


def main():
    parser = ArgumentParser(description='Extract changelog entry for a certain version')
    parser.add_argument('version', help='Version to extract', metavar='VERSION')
    parser.add_argument('--changelog', default='CHANGELOG.md', help='File to parse')
    parser.add_argument('--github-action-output', dest='action_output',
                        metavar='VAR', help='Return GitHub Action Output')

    args = parser.parse_args()

    # Use the last part of a full git ref
    version = re.sub(r'^refs/(heads|tags|remotes)/', '', args.version)

    fh = open(args.changelog, 'r')

    found = False
    content = ""

    for line in fh.readlines():
        line = line.strip()

        if line.startswith("##"):
            # is a version header
            if found:
                # this is the next version header
                break
            elif version in line:
                # the version we are interested in?
                found = True
        elif found and not line_ignored(line):
            # inside the version block
            content += line + "\n"

    fh.close()

    content = content.strip()

    # Print found content
    if args.action_output:
        # Print for GitHub actions
        # see https://help.github.com/en/actions/reference/workflow-commands-for-github-actions#setting-an-output-parameter
        print('::set-output name=%s::%s' % (args.action_output, quote_uri(content)))
    else:
        # Return plain output
        print(content.strip())

    return 0


if __name__ == '__main__':
    sys.exit(main())
