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


def unshorturl(shorturl: str, recursive: bool = False):
    '''
    Spam mails ofen contain urls which should be concealed with a shortner url
    service. Fortunately, most shortened URLs work by naming the correct URL as
    the location field of a 30x response. this function use this behavior by
    sending a HEAD request (not a GET as usual) to the short url service and
    then returning the long URL.

    Keyword arguments:
    shorturl  -- the short url which should be checked.
    recursive -- if this is set, the function follows all 30x answers until
                 something else comes.
    '''
    allowed_status = [
        http.HTTPStatus.MULTIPLE_CHOICES,       # Status Code 300
        http.HTTPStatus.MOVED_PERMANENTLY,      # Status Code 301
        http.HTTPStatus.FOUND,                  # Status Code 302
        http.HTTPStatus.SEE_OTHER,              # Status Code 303
        http.HTTPStatus.NOT_MODIFIED,           # Status Code 304
        http.HTTPStatus.USE_PROXY,              # Status Code 305
        http.HTTPStatus.TEMPORARY_REDIRECT,     # Status Code 307
        http.HTTPStatus.PERMANENT_REDIRECT,     # Status Code 308
    ]

    longurl = None
    with requests.session() as session:
        response = session.head(shorturl)
        if recursive:
            while response.status_code in allowed_status:
                longurl = response.headers.get('Location')
                response = session.head(longurl)
        elif response.status_code in allowed_status:
            longurl = response.headers.get('Location')
    if not longurl:
        raise ValueError
    return longurl


def cmdparse(args=None):
    '''
    function to parse the command line options
    '''
    parser = argparse.ArgumentParser(
        description='Simple script to get a long url from a shorturl')
    parser.add_argument('shorturl', type=str, nargs="?", default=None,
                        help='the shorturl to be examined with protocol (like http[s])')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='follow short urls recursively until the long url appears')
    return parser.parse_args(args)


def main():
    args = cmdparse()
    if args.shorturl:
        shorturl = args.shorturl
    else:
        shorturl = input('please enter the short url: ')
    try:
        longurl = unshorturl(shorturl, args.recursive)
        print(f'the longurl is: {longurl}')
    except requests.exceptions.MissingSchema:
        print(f'short url seams to be invalid {shorturl}')
    except ValueError:
        print(f"{shorturl} seams not to be a short url")


if __name__ == "__main__":
    main()
