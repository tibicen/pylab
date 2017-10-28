# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 13:18:09 2014

@author: Dawid Huczyński
"""
import os

from PIL import Image

PATH = ''
IMG_MAX_SIZE = (1500, 1000)

print('start')

def res_imgs(img_max_size, path):
    """Resize all images files to smaller sizes."""
    count = 0
    size_old = 0
    size_new = 0
    print('inside')
    filename = None
    for root, directory, files in os.walk(path):
        for file in files:
            #            if file.endswith('.JPG'):
            #                file = file.replace('.JPG', '.jpg')
            #                os.rename(root+'\\'+ file)
            if file.endswith(('.JPG', '.jpg', '.jpeg',
                              '.png', '.tif', '.tiff')):
                if filename is None or filename != root.split('\\')[-1]:
                    counter = 0
                    filename = root.split('\\')[-1]
                print(file)
                newname = '{}-{}.{}'.format(root.split('\\')[-1],
                                            str(counter).zfill(3),
                                            file.split('.')[-1].lower())
                os.rename(root + '\\' + file, root + '\\' + newname)
                file = newname
                count += 1
                counter += 1
                file_stats = os.stat(root + '\\' + file)
                tmp_file_size = file_stats.st_size / float(1024) / 1024
                size_old += tmp_file_size
                img = Image.open(root + '\\' + file, 'r')
                size = img.size
                if size[0] <= img_max_size[0] or size[1] <= img_max_size[1]:
                    pass
                else:
                    if size[0] >= size[1]:
                        factor = img_max_size[1] / float(size[1])
                        img = img.resize(
                            (int(size[0] * factor), int(size[1] * factor)),
                            Image.ANTIALIAS)
                    else:
                        factor = img_max_size[0] / float(size[0])
                        img = img.resize(
                            (int(size[0] * factor), int(size[1] * factor)),
                            Image.ANTIALIAS)
                img.save(root + '\\' + 'a' + file.rstrip('png') +
                         'jpg', 'JPEG', optimize=True, quality=85)
                file_stats = os.stat(root + '\\' + file)
                tmp_file_size = file_stats.st_size / float(1024) / 1024
                size_new += tmp_file_size
            else:
                print('!!!!!!!!!!!!!!!!!!  ' + file)
    return (size_old, size_new)


SIZE_OLD, SIZE_NEW = res_imgs(IMG_MAX_SIZE, PATH)
