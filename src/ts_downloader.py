# -*- coding: UTF-8 -*-

import os
from requests import get
from tqdm import tqdm

from src.constants import MSG_ERROR_DOWNLOAD, TMP_DOWNLOAD_PATH

def get_ts_urls(content):
    urls = list()

    for line in content.split('\n'):
        if line.endswith(".ts"):
            urls.append(line.strip("\n"))
    
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
    if convert_to_mp4:
        output_path += '.mp4'
    else:
        output_path += '.ts'

    with open(output_path, "wb+") as file:
        for i in range(max_no):
            filename = os.path.join(input_dir, '{}.ts'.format(i + 1))
            file.write(open(filename, "rb").read())

    clear_tmp_dir(TMP_DOWNLOAD_PATH)

    return output_path

def clear_tmp_dir(dir):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
