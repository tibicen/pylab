import os
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool
from time import sleep

import colorama
import requests
from colorama import Fore, Style
from progress.bar import Bar
from requests.utils import unquote
from selenium import webdriver

WORK_DIR = os.getcwd()
# WORK_DIR = '/home/tibicen/tf_files/star_wars'
ADRESS = 'https://www.google.pl/imghp?hl=pl'
SEARCH = 'darth vader'

colorama.init()


def getDriver():
    if os.name == 'nt':
        CHROMEDRIVER = "C:\webdriver\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = CHROMEDRIVER
        driver = webdriver.Chrome(CHROMEDRIVER)
    else:
        driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    return driver

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


def getLinks(ADRESS, SEARCH):
    driver = getDriver()
    driver.get(ADRESS)
    searchbox = driver.find_element_by_name('q')
    search = driver.find_element_by_name("btnG")
    searchbox.send_keys(SEARCH)
    search.click()
    # footer = driver.find_element_by_class_name('fbar')
    # footer.click()
    links = []
    tmpPics = []
    while True:
        more = driver.find_element_by_id('smc')
        if more.get_attribute('style') == 'display: none;':
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
        else:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            moreButton = driver.find_element_by_id('smb')
            moreButton.click()
            sleep(1)
        pics = driver.find_elements_by_class_name('rg_l')
        if len(pics) == len(tmpPics):
            print('bam')
            break
        tmpPics = pics
    links = [unquote(p.get_attribute('href'))[
        36:].split('&imgrefurl')[0] for p in pics]
    f = open(SEARCH.replace(' ', '_') + '.txt', 'w')
    for el in links:
        f.write(el + '\n')
    f.close()
    return links


def downloadLinks(links):
    os.mkdir('{}'.format(SEARCH.replace(' ', '_')))
    os.chdir('{}'.format(SEARCH.replace(' ', '_')))
    exceptions = []
    for n, url in enumerate(links):
        try:
            # downloadFile(url, '{}'.format(SEARCH.replace(' ','_')))
            downloadFile(url)
            print(Fore.GREEN + '[v]' + Style.RESET_ALL +
                  ' downloaded {}: {}'.format(n, url))
        except:
            print(Fore.RED + '[x]' + Style.RESET_ALL +
                  ' failed to download {}: {}'.format(n, url))
            exceptions.append(url + '\n')
    f = open('failed.txt', 'w')
    for el in exceptions:
        f.write(el)
    f.close()


def job(input):
    nr, url, exceptions = input
    try:
        # downloadFile(url, '{}'.format(SEARCH.replace(' ','_')))
        downloadFile(url)
        print(Fore.GREEN + '[v]' + Style.RESET_ALL +
              ' downloaded {}: {}'.format(nr, url))
    except:
        print(Fore.RED + '[x]' + Style.RESET_ALL +
              ' failed to download {}: {}'.format(nr, url))
        exceptions.append(url + '\n')


def downloadLinksMULTI(SEARCH, links, downloadFolder):
    os.chdir(downloadFolder)
    try:
        os.mkdir('{}'.format(SEARCH.replace(' ', '_')))
    except(FileExistsError):
        pass
    os.chdir('{}'.format(SEARCH.replace(' ', '_')))
    exceptions = []
    z = zip(range(len(links)), links, [exceptions for x in range(len(links))])
    pool = Pool()
    # bar = Bar('Processing', max=len(links))
    for i in pool.imap(job, z):
        # bar.next()
        pass
    # bar.finish()

os.chdir(WORK_DIR)
links = getLinks(ADRESS, SEARCH)
# with open(SEARCH.replace(' ', '_') + '.txt', 'r') as f:
#     t = f.readlines()
# links = [x.rstrip('\n') for x in t]
#
# downloadLinksMULTI(SEARCH, links, '/home/tibicen/tf_files/star_wars')
