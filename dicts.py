'''
Commands that look up the definition of words.
Sources include UrbanDictionary and Google.
'''

import urllib
import json
import ast
import re
from conf import settings

def urban(*args, **kwargs):
    '''
    !urban word [count]
    Defines a word from the urban dictionary
      - words: list of words to define
      - count: number of definitions to show (max 10)
    '''
    count = 3
    if not args: return { 'error': 'At least one word must be specified' }
    word = args[0]
    if len(args) > 1:
        try:
            count = int(args[-1])
            if count < 1 or count > 10: return { 'error': 'Count must be in [1, 10]' }
        except ValueError: pass
    endpoint = 'http://api.urbandictionary.com/v0/define?'
    feed = json.load(urllib.urlopen('%s%s' % (endpoint, urllib.urlencode({ 'term': word }))))
    deflist = ''
    for argi, entry in enumerate(feed['list'][:count]):
        if 'definition' in entry:
            if len(entry['definition']) > settings.RESPONSE_CHAR_LIMIT: continue
            deflist += '%d. %s\n\n' % (argi + 1, entry['definition'])
    if not deflist: return { 'error': 'I do not know what "%s" means. Maybe you misspelled it?' % word }
    return { 'result': str(deflist) }

def sanitize_html(in_str):
    '''
    NO_RECORD
    '''
    return re.sub(r'<[^>]*>', '', in_str)

def extract_defn(def_dict, count):
    '''
    NO_RECORD
    '''
    def_str = ''
    sound_url = ''
    def_ind = 1
    for term in def_dict['terms']:
        if term['type'] == 'text':
            def_str += '%s (%s)\n' % (term['text'], term['labels'][0]['text'])
    for entry in def_dict['entries']:
        if def_ind > count: break
        if entry['type'] == 'meaning':
            def_str += '%d. %s\n' % (def_ind, sanitize_html(entry['terms'][0]['text']))
            def_ind += 1
    return def_str

def get_sound_url(res_tree):
    '''
    NO_RECORD
    '''
    for term in res_tree['primaries'][0]['terms']:
        if term['type'] == 'sound': return term['text']

def define(*args, **kwargs):
    '''
    !define word [count]
    Defines a word using the Google dictionary.
    If Google doesn't know, urbandictionary is asked.
      - word: word to define
      - count: number of definitions to show
    '''
    count = 3
    word = 'nothing' if not args else args[0]
    if len(args) > 1:
        try:
            count = int(args[-1])
            if count < 1: return { 'error': 'Count must be greater than 0' }
        except ValueError: pass
    endpoint = 'http://www.google.com/dictionary/json?'
    opts = {
        'callback': 'dict_api.callbacks.id100',
        'sl': 'en',
        'tl': 'en',
        'restrict': 'pr%2Cde',
        'client': 'te',
        'q': word
    }
    feed = urllib.urlopen('%s%s' % (endpoint, urllib.urlencode(opts)))
    feed_str = feed.read()
    feed_str = feed_str[feed_str.find('{'):feed_str.rfind('}') + 1]
    feed_dict = ast.literal_eval(feed_str)
    if 'primaries' not in feed_dict: return urban(word, count)
    res_str = ''
    for argi, defn in enumerate(feed_dict['primaries']):
        res_str += '%s\n---\n' % extract_defn(defn, count)
    res_str += 'Pronounciation: %s\n' % get_sound_url(feed_dict)
    return { 'result': res_str }
