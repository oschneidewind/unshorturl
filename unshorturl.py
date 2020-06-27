#!/usr/bin/env python3
# Copyright (C) 2020, Oliver Schneideiwnd
# Authors: Oliver Schneidewind <oliver@printfdebugging.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; Version 2 only
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# -*- coding: utf-8 -*-
import argparse
import http
import sys
import requests


def unshorturl(shorturl: str):
    '''
    Spam mails ofen contain urls which should be concealed with a shortner url
    service. Fortunately, most shortened URLs work by naming the correct URL as
    the location field of a 30x response. this function use this behavior by
    sending a HEAD request (not a GET as usual) to the short url service and
    then returning the long URL.

    Keyword arguments:
    shorturl -- the short url which should be checked.
    '''
    allowed_status = [
        http.HTTPStatus.MULTIPLE_CHOICES,
        http.HTTPStatus.MOVED_PERMANENTLY,
        http.HTTPStatus.FOUND,
        http.HTTPStatus.SEE_OTHER,
        http.HTTPStatus.NOT_MODIFIED,
        http.HTTPStatus.USE_PROXY,
        http.HTTPStatus.TEMPORARY_REDIRECT,
        http.HTTPStatus.PERMANENT_REDIRECT,
    ]

    session = requests.session()
    response = session.head(shorturl)
    if response.status_code in allowed_status:
        return response.headers.get('Location')
    return "No short Url found"


def cmdparse(args=None):
    '''
    function to parse the command line options
    '''
    parser = argparse.ArgumentParser(
        description='Simple script to get al long url from a shorturl')
    parser.add_argument('-s', '--shorturl', type=str,
                        help='the shorturl to be examined with protocol (like http [s])')
    return parser.parse_args(args)


if __name__ == "__main__":
    args = cmdparse()
    if args.shorturl:
        shorturl = args.shorturl
    else:
        shorturl = input('please enter the short url: ')
    try:
        longurl = unshorturl(shorturl)
        print(f'the longurl is: {longurl}')
    except requests.exceptions.MissingSchema:
        print(f'short url seams to be invalid {shorturl}')
