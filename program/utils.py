from django.conf import settings

import json
import urllib
import bisect
import hashlib
from os.path import join
from datetime import datetime, date, timedelta
from functools import partial


def get_automation_id_choices():
    base_url = getattr(settings, 'AUTOMATION_BASE_URL', None)
    cache_dir = getattr(settings, 'AUTOMATION_CACHE_DIR', 'cache')
    cached_shows = join(cache_dir, 'shows.json')
    shows = []
    if base_url:
        try:
            shows_json = urllib.urlopen(base_url).read()
            shows_list = json.loads(shows_json)['shows']
            multi_shows_list = json.loads(shows_json)['multi-shows']
        except IOError:
            try:
                with open(cached_shows) as cache:
                    shows_list = json.loads(cache.read())['shows']
                    multi_shows_list = json.loads(cache.read())['multi-shows']
            except IOError:
                shows_list = []
                multi_shows_list = []
        else:
            with open(cached_shows, 'w') as cache:
                cache.write(shows_json)

        shows = [(s['id'], '%d | %s' % (s['id'], s['title']), s['title']) for s in shows_list if not s.get('multi')]

        [bisect.insort(shows, (s['id'], '%05d | %s' % (s['id'], s['title']), s['title'])) for s in multi_shows_list]

        shows.sort(key=lambda show: show[2].lower())

        shows = [(s[0], s[1]) for s in shows]

    return shows


def get_cached_shows():
    cache_dir = getattr(settings, 'AUTOMATION_CACHE_DIR', 'cache')
    cached_shows = join(cache_dir, 'shows.json')
    shows = {}
    with open(cached_shows) as shows_json:
        shows = json.loads(shows_json.read())

    return shows


def tofirstdayinisoweek(year, week):
    # http://stackoverflow.com/questions/5882405/get-date-from-iso-week-number-in-python
    ret = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        ret -= timedelta(days=7)
    return ret


def hash_file(file, block_size=65536):
    hasher = hashlib.sha256()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()
