# -*- coding: UTF-8 -*-

URL_ROOT = 'http://www.5278.cc/forum.php?gid=22'
PATTERN_M3U8 = r"player\.src\('(.*)'\);"
PATTERN_BOOKMARK = r"<DT><A HREF=\"(http://www\.5278\.cc/forum\.php\?mod=viewthread.*?)\".*<\/A>"

LOG_PATH = 'output.log'
TMP_DOWNLOAD_PATH = 'tmp'
DOWNLOAD_PATH = 'result'
BOOKMARK_PATH = 'bookmark.txt'

INVALID_CHAR = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}

HAS_SCREEN = True
CONVERT_TO_MP4 = False
MSG_ERROR_DOWNLOAD = -1
