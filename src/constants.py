# -*- coding: UTF-8 -*-

URL_ROOT = 'http://www.5278.cc/forum.php?gid=22'
URL_TS = 'seg-{}-v1-a1.ts'
PATTERN_POST = r"^http[s]?://[www\.]?5278\.cc/forum\.php\?mod=viewthread\&tid=([\d+]*)"
PATTERN_M3U8 = r"player\.src\('(.*)'\);"
PATTERN_BOOKMARK = r"<DT><A HREF=\"(http://www\.5278\.cc/forum\.php\?mod=viewthread\&tid=[\d+].*?)\".*<\/A>"
PATTERN_TS = r"seg-(\d+)-v1-a1.ts"

LOG_PATH = 'output.log'
TMP_DOWNLOAD_PATH = 'tmp'
DOWNLOAD_PATH = 'result'
BOOKMARK_PATH = 'bookmark.txt'

INVALID_CHAR = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}

HAS_SCREEN = True
CONVERT_TO_MP4 = True
MSG_ERROR_DOWNLOAD = -1
