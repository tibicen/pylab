# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 15:37:21 2015

@author: Tibicen
"""
import os
from shutil import copyfile
import requests
import zipfile


FONTS_ARCHIVE = "https://github.com/google/fonts/archive/master.zip"


def downloadFile(url, overwriteName=None):
    if overwriteName:
        overwriteName + '.' + url.split('.')[-1]
        pass
    else:
        localFile = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(localFile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return localFile


def downloadFonts(FONTS_ARCHIVE):
    downloadFile(FONTS_ARCHIVE)
    zip_ref = zipfile.ZipFile(os.path.join(
        os.getcwd(), FONTS_ARCHIVE.split('/')[-1]), 'r')
    os.mkdir('FONTS-GIT')
    zip_ref.extractall(os.path.join(os.getcwd(), 'FONTS-GIT'))
    zip_ref.close()
    os.remove(os.path.join(os.getcwd(), FONTS_ARCHIVE.split('/')[-1]))

fonts_folder = 'C:\\POBRANE\\fonts-master\\fonts-master'
win_fonts_folder = 'C:\\Fonts'
if "Fonts" not in os.listdir('c:\\'):
    os.mkdir('C:\\Fonts')
def extractFonts(fonts_folder=None):
    if fonts_folder is None:
        fonts_folder = os.path.join(os.getcwd(), 'FONTS')
    for p, d, files in os.walk(fonts_folder):
        for f in files:
            if f.endswith('.ttf'):
                print(f, end='')
                if f in os.listdir(win_fonts_folder):
                    print('\t\t\t already in system!!!!!!!!')
                else:
                    copyfile(os.path.join(p, f), os.path.join(win_fonts_folder, f))
                    print('\t\t\t installed.')

# TODO Install fonts to OS-specyfic folder


# extractFonts(fonts_folder)
# downloadFonts(FONTS_ARCHIVE)
