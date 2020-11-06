# -*- coding: UTF-8 -*-

import os
import re
from requests import get
from tqdm import tqdm

from src.constants import MSG_ERROR_DOWNLOAD, PATTERN_TS, TMP_DOWNLOAD_PATH, URL_TS

def get_ts_urls(content):
    urls = list()

    for line in content.split('\n')[::-1]:
        match = re.match(PATTERN_TS, line)
        if match:
            no = int(match.group(1))
            urls = [URL_TS.format(i) for i in range(1, no + 1)]
            break

    return urls

def download_ts_files(urls, url_root, path):
    len_urls = len(urls)
    for i in tqdm(range(len_urls), desc='Downloading ts files'):
        try:
            response = get(url_root + urls[i], stream=True, verify=False)
        except Exception:
            return MSG_ERROR_DOWNLOAD

        download_path = os.path.join(path, "{}.ts".format(i + 1))
        with open(download_path, "wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    return len_urls

def concatenate_ts_files(max_no, input_dir, output_path, convert_to_mp4=False):
    print('***************** {}'.format(output_path))
    with open(output_path + '.ts', "wb+") as file:
        for i in range(max_no):
            filename = os.path.join(input_dir, '{}.ts'.format(i + 1))
            file.write(open(filename, "rb").read())

    clear_tmp_dir(TMP_DOWNLOAD_PATH)

    if convert_to_mp4:
        import subprocess
        command = [
            'ffmpeg', '-y', '-i', output_path + '.ts', output_path + '.mp4'
        ]
        ffmpeg = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        ffmpeg.communicate()
        os.remove(output_path + '.ts')
        output_path += '.mp4'
    else:
        output_path += '.ts'

    return output_path

def clear_tmp_dir(dir):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
