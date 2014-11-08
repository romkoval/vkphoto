vkphoto
=======

vkontakte photo uploader

How to start:

pip install vk
pip install pillow

usage: vkphoto.py [-h] [-l] [-a ALBUM] [-c] [-u USER_LOGIN] [-p USER_PASSWORD]
                  [-e FILE_EXTENSIONS]
                  [file [file ...]]

positional arguments:
  file                  files or direcories with images to upload

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-albums     List VK albums or photos in album, default: False
  -a ALBUM, --album ALBUM
                        Album title where photos to add or list
  -c, --create          Create album if not exists
  -u USER_LOGIN, --user-login USER_LOGIN
                        VK user login or email
  -p USER_PASSWORD, --user-password USER_PASSWORD
                        VK user password. Will prompt a password if not
                        specified
  -e FILE_EXTENSIONS, --file-extensions FILE_EXTENSIONS
                        Comma separated file extensions. Used when directory
                        specified

