# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
from functools import wraps
import os
import re
from requests import get
import sys
from time import sleep
import traceback

"""
    Disable warning.
"""
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from src.browser import Browser
from src.constants import *
from src.exceptions import RetryException
from src.secret import USERNAME, PASSWORD
from src.ts_downloader import concatenate_ts_files, download_ts_files, get_ts_urls

"""
    Usage:
        python main.py *urls_file*
    
    Args:
        *urls_file*: URLs input path (a file including one URL per line).

    Notice:
        Put chromedriver[.exe] in folder /bin.
        Copy secret.py.dist as secret.py in the same folder.
"""

def output_log(msg, traceback_option=True):
    with open(LOG_PATH, 'a', encoding='utf8') as output_file:
        output_file.write(msg)
    if traceback_option:
        traceback.print_exc(file=open(LOG_PATH, 'a', encoding='utf8'))

def retry(attempt=10, wait=1):
    def wrap(func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RetryException:
                if attempt > 1:
                    sleep(wait)
                    return retry(attempt - 1, wait)(func)(*args, **kwargs)
                else:
                    if func.__name__ == 'check_login':
                        tmp = 'log in. (username: {}, password: {})'.format(USERNAME, PASSWORD)

                    msg = '{} - Error: Failed to {}\n'.format(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tmp)
                    output_log('\n' + msg, True)

                    exc = RetryException(msg)
                    exc.__cause__ = None

                    raise exc

        return wrapped_f

    return wrap

def set_cookies():
    global cookies

    cookies_list = browser.driver.get_cookies()
    for cookie in cookies_list:
        cookies[cookie['name']] = cookie['value']

def load_urls(path):
    with open(path, 'r') as file:
        return [url.strip() for url in file.readlines() if re.match(PATTERN_POST, url)]
    
def login():
    username = USERNAME
    password = PASSWORD

    browser.get(URL_ROOT)

    agree_btn = browser.find_one('td a')
    agree_btn.click()

    u_input = browser.find_one('input[name="username"]')
    u_input.send_keys(username)
    p_input = browser.find_one('input[name="password"]')
    p_input.send_keys(password)

    login_btn = browser.find_one(".pn.vm")
    login_btn.click()

    @retry()
    def check_login():
        if browser.find_one('input[name="username"]'):
            raise RetryException()

    check_login()

    set_cookies()

def web_crawler(urls_file):
    login()

    urls = load_urls(urls_file)

    for i in range(len(urls)):
        print("\n{} - Info: Start downloading post \'{}\'. (Overall progress: {}/{})\n".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), urls[i], (i + 1), len(urls)))
        html = get(urls[i], cookies=cookies).text
        soup = BeautifulSoup(html, 'lxml')

        post_name = soup.select('meta[name="description"]')[0]["content"]
        post_name = ''.join(char for char in post_name if char not in INVALID_CHAR)

        player_list = soup.select(".cc5278_player")
        video_src_list = [player["src"] for player in player_list]

        if not os.path.exists(TMP_DOWNLOAD_PATH):
            os.makedirs(TMP_DOWNLOAD_PATH)

        if not os.path.exists(DOWNLOAD_PATH):
            os.makedirs(DOWNLOAD_PATH)

        headers = {
            "Referer": urls[i]
        }
        video_num = len(video_src_list)
        for j in range(video_num):
            print("\n{} - Info: Start downloading video \'{}\'. (Progress of this post: {}/{})\n".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), video_src_list[j], (j + 1), len(video_src_list)))
            m3u8_src = get(video_src_list[j], headers=headers, cookies=cookies).text
            url_m3u8 = re.search(PATTERN_M3U8, m3u8_src).group(1)
            m3u8_content = get(url_m3u8, headers=headers).text

            url_root = url_m3u8[: url_m3u8.rfind('/') + 1]
            ts_urls = get_ts_urls(m3u8_content)

            max_no = download_ts_files(ts_urls, url_root, TMP_DOWNLOAD_PATH)
            if max_no != MSG_ERROR_DOWNLOAD:
                filename = os.path.join(DOWNLOAD_PATH, '{}'.format(post_name))
                if video_num != 1:
                    filename += '_{}'.format(post_name, str(j + 1))
                while os.path.exists(filename):
                    msg = '{} - Warning: The file \'{}\' exists. Rename as \'{}\'.\n'.format(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename, filename + '_')
                    filename += '_'
                    output_log('\n' + msg, False)

                filename = concatenate_ts_files(max_no, TMP_DOWNLOAD_PATH, filename, CONVERT_TO_MP4)
                print('\n{} - Info: The video has been saved as \'{}\'.\n'.format(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename))
            else:
                msg = '{} - Error: Failed to download all ts files. (URL: {})\n'.format(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), video_src_list[j])
                output_log('\n' + msg, False)


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Error: The number of arguments is incorrect.'

    browser = Browser(HAS_SCREEN)
    cookies = dict()

    urls_file = sys.argv[1]
    web_crawler(urls_file)
