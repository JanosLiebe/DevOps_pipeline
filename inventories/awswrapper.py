import sys
import os
import json
from shlex import split
from StringIO import StringIO


if os.environ.get('LC_CTYPE', '') == 'UTF-8':
    os.environ['LC_CTYPE'] = 'en_US.UTF-8'

import awscli.clidriver

def aws_ec2(args):
    args = split('ec2 '+args)
    stdout = sys.stdout
    #print 'Exec: aws '+' '.join(args)
    sys.stdout = StringIO()
    out = ''
    try:
        driver = awscli.clidriver.create_clidriver()
        driver.main(args)
        out = sys.stdout.getvalue()
    finally:
        sys.stdout = stdout
    if out != '':
        #print 'OUT:', out
        return json.loads(out)

if __name__ == '__main__':
    print aws_ec2(sys.argv[1:])
