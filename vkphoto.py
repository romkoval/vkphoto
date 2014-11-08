#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import vk
import argparse
import getpass
import sys
import os
import datetime

try:
    from PIL import Image
except:
    pass


def readOpts():
    parser = argparse.ArgumentParser(description='vk photo uploader')
    parser.add_argument('fname', metavar='file', nargs="*",
                        help='files or direcories with images to upload')
    parser.add_argument('-l', '--list-albums', dest='list_albums',
                        default=False,
                        action="store_true",
                        help='List VK albums or photos in album, default: %(default)s')
    parser.add_argument('-a', '--album', dest='album',
                        help='Album title where photos to add or list')
    parser.add_argument('-c', '--create', dest='create', default=False,
                        action='store_true',
                        help='Create album if not exists')
    parser.add_argument('-u', '--user-login', dest='user_login', help='VK user login or email')
    parser.add_argument('-p', '--user-password', dest='user_password',
                        help='VK user password. Will prompt a password if not specified')
    parser.add_argument('-e', '--file-extensions', dest='file_extensions',
                        default='jpg,jpeg,gif,png',
                        help='Comma separated file extensions. Used when directory specified')

    args = parser.parse_args()
    if not args.user_password:
        args.user_password = getpass.getpass()
    return args


def imageDateTaken(path):
    if 'PIL' in sys.modules:
        return Image.open(path)._getexif()[36867]
    else:
        return None


def listAlbums(vkapi):
    albums = vkapi.photos.getAlbums()
    if len(albums) == 0:
        print('no albums found')
    else:
        for i in albums.get('items'):
            title = i.get('title') + ' '
            print ("%s [% 4d]" % (title.ljust(50, '.'), i.get('size')))


def listInAlbum(vkapi, album):
    aid = getAid(vkapi, album)
    if not aid:
        print('album not found: %s' % album, file=sys.stderr)
    else:
        res = vkapi.photos.get(album_id=aid)
        for photo in res.get('items'):
            print('id: %s %sx%s %s' % (photo.get('id'), photo.get('width'),
                  photo.get('height'), photo.get('text')))
        print('total %d photos in %s' % (res.get('count'), album))


def uploadOnePhoto(vkapi, url, aid, filename):
    import requests

    filedata = open(filename, 'rb')
    try:
        upload = requests.post(url, files={'file1': (filename, filedata)})
        if upload.status_code == 200:
            res = upload.json()
            ctime_str = imageDateTaken(filename)
            saved = vkapi.photos.save(album_id=aid, server=res.get('server'),
                                      photos_list=res.get('photos_list'),
                                      hash=res.get('hash'),
                                      caption=os.path.basename(filename) + '\n' + ctime_str)
            return saved[0].get('id')
    except requests.exceptions.ReadTimeout as to:
        print(to, file=sys.stderr)
    except requests.exceptions.ConnectionError as ce:
        print(ce, file=sys.stderr)

    return None


def uploadPhotosAid(vkapi, uploadUrl, files, extensions, aid):
    for f in files:
        if os.path.isdir(f):
            print('entering directory: %s' % f)
            listing = [os.path.join(f, fp) for fp in os.listdir(f)]
            uploadPhotosAid(vkapi, uploadUrl, listing, extensions, aid)
        else:
            ext = os.path.splitext(f)[1]
            if not ext or ext[1:].lower() not in extensions:
                print('skiping %s' % f)
                continue

            for t in range(3):
                print('%s %s ... ' % (t > 0 and 'retrying' or 'uploading', f), end='')
                photoid = uploadOnePhoto(vkapi, uploadUrl, aid, f)
                if photoid:
                    print('OK (%d)' % photoid)
                    break
                else:
                    print('failed')


def getAid(vkapi, album):
    albums = vkapi.photos.getAlbums()
    for a in albums.get('items'):
        if a.get('title') == album:
            return a.get('id')

    return None


def createAlbum(vkapi, title):
    res = vkapi.photos.createAlbum(title=title, privacy=3, comment_privacy=3)
    return res.get('id')


def uploadPhotos(vkapi, opts):
    aid = getAid(vkapi, opts.album)
    if not aid:
        print('unable to find album: %s' % (opts.album))
        if opts.create:
            print('creating album')
            aid = createAlbum(vkapi, opts.album)
    if not aid:
        return None

    uploadServer = vkapi.photos.getUploadServer(album_id=aid)
    uploadUrl = uploadServer.get('upload_url')
    valid_extensions = opts.file_extensions.split(',')
    uploadPhotosAid(vkapi, uploadUrl, opts.fname, valid_extensions, aid)


def main():
    opts = readOpts()
    vkapi = vk.API(app_id=4624575,
                   user_login=opts.user_login, user_password=opts.user_password,
                   scope='photos')
    if opts.list_albums:
        if opts.album:
            listInAlbum(vkapi, opts.album)
        else:
            listAlbums(vkapi)
    else:
        uploadPhotos(vkapi, opts)

if __name__ == '__main__':
    try:
        main()
    except vk.api.VkAuthorizationError as e:
        print (e)
        sys.exit(1)
