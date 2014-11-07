#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import vk
import argparse

def readOpts():
    parser = argparse.ArgumentParser(description='vk photo uploader')
    parser.add_argument('fname', metavar='file', nargs="*",
                        help='files or direcories with images to upload')
    parser.add_argument('-l', '--list-albums', dest='list_albums',
                        default=False,
                        action="store_true",
                        help='svn repository url, default: %(default)s')
    parser.add_argument('-a', '--access-token', dest='access_token',
                        help='application access token')
    parser.add_argument('-u', '--user-login', dest='user_login', help='VK user login or email')
    parser.add_argument('-p', '--user-password', dest='user_password', help='VK user password')

    args = parser.parse_args()
    return args


def listAlbums(vkapp):
    albums = vkapp.photos.getAlbums()
    if len(albums) == 0:
        print('no albums found')
    else:
        for i in albums.get('items'):
            print (i.get('title'))


def main():
    opts = readOpts()
    vkapp = vk.API(app_id=4624575,
                   user_login=opts.user_login, user_password=opts.user_password,
                   scope='photos')
    if opts.list_albums:
        listAlbums(vkapp)

if __name__ == '__main__':
    main()
