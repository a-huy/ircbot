import urllib
import re
import lib
import sys
from dicts import *
from django.conf import settings
from django.utils import simplejson

def is_cmd(line):
    return line[0] == '!'

def execcmd(cmd):
    args = filter(bool, cmd[1:].split(' '))
    cmd = args.pop(0)
    kwargs = {}
    for arg in args:
        match = re.search(r'^(\w+)\s*=\s*(\w+)$', arg)
        if match: kwargs[match.group(1)] = match.group(2)
    try:
        return getattr(lib, cmd)(*args, **kwargs)
    except AttributeError:
        return { 'error': 'I am sorry, but I could not recognize the command "%s".' % cmd }

def post_chat(line):
    endpoint = 'https://api.groupme.com/v3/bots/post'
    bot_id = settings.BOT_ID
    opts = {
        'bot_id': bot_id,
        'text': line,
    }
    result = urllib.urlopen(endpoint, data=urllib.urlencode(opts)).read()
    print result
    if result:
        meta = simplejson.loads(result)['meta']
        if meta['code'] != 200:
            err_str = 'Posting to chat returned code %d: %s\n' % (meta['code'], meta['errors'][0])
            sys.stderr.write(err_str)
