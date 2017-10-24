# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor


class SamanthaBeeIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?samanthabee\.com/episode/[0-9a-z-]+/clip/(?P<id>[a-z0-9-]+)/'
    _TESTS = [{
        'url': 'http://samanthabee.com/episode/46/clip/not-the-white-house-correspondents-dinner-pt-1-peaches-and-monologue/',
        'md5': '2cfca93b7da2aa45fb883d879c1cd2ca',
        'info_dict': {
            'id': 'not-the-white-house-correspondents-dinner-pt-1-peaches-and-monologue',
            'ext': 'mp4',
            'title': 'Not The White House Correspondents\' Dinner, Pt. 1: Peaches and Monologue | Full Frontal with Samantha Bee',
            'description': 'Peaches destroys our set and Sam destroys the mediaNew episodes air on TBS every Wednesdays at 10:30/9:30c',
        }
    }, {
        'url': 'http://samanthabee.com/episode/47/clip/miami-rights/',
        'md5': '01e00a7faec140a8865bccf621e8eb75',
        'info_dict': {
            'id': 'miami-rights',
            'ext': 'mp4',
            'title': 'Miami Rights | Full Frontal with Samantha Bee',
            'description': 'Florida: the surf, the sun, the sand, the fight for basic voting rights!New episodes air on TBS every Wednesdays at 10:30/9:30c',
        }
    }, {
        'url': 'http://samanthabee.com/episode/bonus-act/clip/steve-king-say-anything-else/',
        'md5': '49b027b4493ed9fca4b087542536f965',
        'info_dict': {
            'id': 'steve-king-say-anything-else',
            'ext': 'mp4',
            'title': 'Steve King Say Anything (Else) | Full Frontal with Samantha Bee',
            'description': 'Steve King finally let his true colors show, and they are very, very whiteNew episodes air on TBS every Wednesdays at 10:30/9:30c',
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = self._og_search_title(webpage)
        thumbnail = self._og_search_thumbnail(webpage)
        description = self._og_search_description(webpage)

        url = self._search_regex(
            r'data-plyr-url[^"]+"([^"]+)',
            webpage, 'data-plyr-url')

        return {
            'url': url,
            'id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail
        }


class SamanthaBeePlaylistBaseIE(InfoExtractor):

    def _extract_playlist_entries(self, playlist):
        return [
            self.url_result(
                episode, SamanthaBeeIE.ie_key()
            )
            for episode in playlist
        ]


class SamanthaBeePlaylistIE(SamanthaBeePlaylistBaseIE):
    _VALID_URL = r'https?://(?:www\.)?samanthabee\.com/episode/(?P<id>[^/?#]+)/'

    _TESTS = [{
        'url': 'http://samanthabee.com/episode/45/',
        'info_dict': {
            'id': '45',
            'title': 'Episode 45 | Full Frontal with Samantha Bee',
            'description': '04/05/2017 - We Told You So: Russian Hacking, Heir to the White House Throne, You\'re! Not! Helping!, Yay Men!, New episodes air on TBS every Wednesdays at 10:30/9:30c',
        },
        'playlist_count': 5,
    }, {
        'url': 'http://samanthabee.com/episode/32/',
        'info_dict': {
            'id': '32',
            'title': 'Episode 32 | Full Frontal with Samantha Bee',
            'description': '12/05/2016 - Eroding Electoral Confidence, The Big Lie, Fake News, Real Consequences, And the Thunder Cunt Goes To..., New episodes air on TBS every Wednesdays at 10:30/9:30c',
        },
        'playlist_count': 5,
    }]

    def _real_extract(self, url):
        playlist_id = self._match_id(url)
        webpage = self._download_webpage(url, playlist_id)

        title = self._og_search_title(webpage)
        thumbnail = self._og_search_thumbnail(webpage)
        description = self._og_search_description(webpage)

        episodes = re.findall(
            r'data-plyr-url[^"]+"([^"]+)',
            webpage)

        entries = self._extract_playlist_entries(episodes)

        return self.playlist_result(entries, playlist_id, title, description)
