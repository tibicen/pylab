# -*- coding: utf-8 -*-
'''Script to download images from search results.
'''
import os
import re
import sys
# import argparse
from multiprocessing import Pool
from selenium import webdriver
from time import sleep

import colorama
import requests
from colorama import Fore, Style

colorama.init()

TOPIC = 'animals'
if len(sys.argv) > 1:
    SEARCH = sys.argv[1]
else:
    SEARCH = 'dog'
if len(sys.argv) > 2:
    WORK_DIR = sys.argv[2]
else:
    WORK_DIR = os.getcwd()
    # WORK_DIR = '/home/tibicen/tf_files/star_wars'


def get_driver():
    ''' Webdriver wrapper.
    returns: driver
    '''
    if os.name == 'nt':
        CHROME_DRIVER = "C:\\webdriver\\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = CHROME_DRIVER
        driver = webdriver.Chrome(CHROME_DRIVER)
    else:
        driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    return driver


def download_file(url, overwriteName=None):
    if overwriteName:
        localFile = overwriteName + '.' + url.split('.')[-1].replace('?', '')
    else:
        localFile = url.split('/')[-1].replace('?', '')
    if localFile not in os.listdir():
        r = requests.get(url, stream=True)
        with open(localFile, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)


def find_bing_links(search, driver):
    ADRESS = 'https://www.bing.com/?scope=images'
    driver.get(ADRESS)
    searchbox = driver.find_element_by_name('q')
    searchBnt = driver.find_element_by_name("go")
    searchbox.send_keys(search)
    searchBnt.click()
    tmp = len(driver.find_elements_by_class_name('dg_b'))
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        if len(driver.find_elements_by_class_name('dg_b')) > tmp:
            tmp = len(driver.find_elements_by_class_name('dg_b'))
        else:
            break
    sleep(2)
    links = []
    for n in driver.find_elements_by_xpath('//a[@m]'):
        links.append(re.findall('imgurl:"(.*?)"',
                                n.get_attribute('m'))[0].split('?')[0])
    # footer = driver.find_element_by_class_name('fbar')
    # footer.click()
    return links


def find_google_links(search, driver):
    ADRESS = 'https://www.google.pl/imghp'
    driver.get(ADRESS)
    searchbox = driver.find_element_by_name('q')
    search_btn = driver.find_element_by_name("btnG")
    searchbox.send_keys(search)
    search_btn.click()
    links = []
    tmpPics = []
    while True:
        more = driver.find_element_by_id('smc')
        if more.get_attribute('style') == 'display: none;':
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
        else:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            moreButton = driver.find_element_by_id('smb')
            moreButton.click()
            sleep(2)
        pics = driver.find_elements_by_class_name('rg_l')
        if len(pics) == len(tmpPics):
            break
        tmpPics = pics
    links = [re.findall('\\?imgurl=(.*?)\\&imgrefurl=', requests.utils.unquote(
        p.get_attribute('href')))[0].split('?')[0] for p in pics]
    return links


def find_all_links(search):
    driver = get_driver()
    if search.replace(' ', '_') + '.txt' in os.listdir():
        with open(os.path.join(os.getcwd(), search.replace(' ', '_') +
                               '.txt'), 'r') as f:
            links = f.readlines()
        links = [l.rstrip('\n') for l in links]
    else:
        links = find_google_links(search, driver) + \
            find_bing_links(search, driver)
    # saves all the links to a txt file
    f = open(search.replace(' ', '_') + '.txt', 'w')
    tmp = []
    links.sort()
    for url in links:
        if url != tmp[-1]:  # clean duplicates
            f.write(url + '\n')
            tmp.append(url)
    f.close()
    return links


def download_links(search, links, download_folder):
    os.chdir(download_folder)
    if search.replace(' ', '_') not in os.listdir():
        os.mkdir('{}'.format(search.replace(' ', '_')))
    os.chdir('{}'.format(search.replace(' ', '_')))
    exceptions = []
    for n, url in enumerate(links):
        # try:
            # download_file(url, '{}'.format(SEARCH.replace(' ','_')))
        download_file(url)
        print(Fore.GREEN + '[v]' + Style.RESET_ALL +
              ' downloaded {}: {}'.format(n, url))
        # except:
        #     print(Fore.RED + '[x]' + Style.RESET_ALL +
        #           ' failed to download {}: {}'.format(n, url))
        #     exceptions.append(url + '\n')
    f = open('failed.txt', 'w')
    for element in exceptions:
        f.write(element)
    f.close()


def job(task):
    nr, url = task
    exceptions = []
    try:
        # download_file(url, '{}'.format(SEARCH.replace(' ','_')))
        download_file(url)
        print(Fore.GREEN + '[v]' + Style.RESET_ALL +
              ' downloaded {}: {}'.format(nr, url))
    except(FileNotFoundError):  # TODO Exception!
        print(Fore.RED + '[x]' + Style.RESET_ALL +
              ' failed to download {}: {}'.format(nr, url))
        exceptions.append(url)
    return exceptions


def download_multiple_links(search, links, download_folder):
    os.chdir(download_folder)
    if search.replace(' ', '_') not in os.listdir():
        os.mkdir('{}'.format(search.replace(' ', '_')))
    os.chdir('{}'.format(search.replace(' ', '_')))
    # z = zip(range(len(links)), links)
    pool = Pool()
    errors = []
    for i in pool.imap(job, enumerate(links)):
        if i:
            errors.append(i[0])
    f = open(os.path.join(WORK_DIR, SEARCH.replace(
        ' ', '_') + '_ERRORS.txt'), 'w')
    for error in errors:
        f.write(error + '\n')
    f.close()


if __name__ == '__main__':
    # driver = get_driver()
    # links = find_bing_links(SEARCH, driver)
    links = find_all_links(SEARCH)
    os.chdir(WORK_DIR)
    if TOPIC.replace(' ', '_') not in os.listdir('J:\\tf_files'):
        os.mkdir(os.path.join('J:\\tf_files', TOPIC.replace(' ', '_')))
    download_multiple_links(SEARCH, links, os.path.join(
        'J:\\tf_files', TOPIC.replace(' ', '_')))


# for l in links:
#     if not l.lower().endswith(('gif', 'jpg', 'jpeg', 'bmp', 'png')):
#         print(l[-50:])
