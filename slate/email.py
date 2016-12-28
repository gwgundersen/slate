"""Handles emailing users.
"""

import subprocess


def send(contents, subject, to):
    """Send email to user.
    """
    # Using mailx for now. I do not want to setup a separate Gmail account
    # just for this (yet).
    cmd = 'echo "%s" | mailx -s "%s" "%s"' % (
        contents, subject, to)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT).stdout.read()
